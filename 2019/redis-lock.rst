使用 Redis 实现锁
===========================

.. note::

    本文摘录自即将出版的《Redis使用手册》，
    详情请见： `RedisGuide.com <http://RedisGuide.com>`_ 。

锁是一种同步机制，
它可以保证一项资源在任何时候只能被一个进程使用，
如果有其他进程想要使用相同的资源，
那么它们就必须等待，
直到正在使用资源的进程放弃使用权为止。

一个锁实现通常会有获取（acquire）和释放（release）这两种操作：

- 获取操作用于取得资源的独占使用权。
  在任何时候，
  最多只能有一个进程取得锁，
  我们把成功取得锁的这个进程称之为锁的持有者。
  在锁已经被持有的情况下，
  所有尝试再次获取锁的操作都会失败。

- 释放操作用于放弃资源的独占使用权，
  一般由锁的持有者调用。
  在锁被释放之后，
  其他进程就可以再次尝试获取这个锁了。

代码清单 2-2 展示了一个使用字符串键实现的锁程序，
这个程序会根据给定的字符串键是否有值来判断锁是否已经被获取，
而针对锁的获取操作和释放操作则是分别通过设置字符串键和删除字符串键来完成的。

----

代码清单 2-2 使用字符串键实现的锁程序：\ ``/string/lock.py``

.. literalinclude:: code/lock.py

----

获取操作 ``acquire()`` 方法是通过执行带有 ``NX`` 选项的 ``SET`` 命令来实现的：

::

    result = self.client.set(self.key, VALUE_OF_LOCK, nx=True)

``NX`` 选项的效果确保了代表锁的字符串键只会在没有值的情况下被设置：

- 如果给定的字符串键没有值，
  那么说明锁尚未被获取，
  ``SET`` 命令将执行设置操作，
  并将 ``result`` 变量的值设置为 ``True`` ；

- 与此相反，
  如果给定的字符串键已经有值了，
  那么说明锁已经被获取，
  ``SET`` 命令将放弃执行设置操作，
  并将 ``result`` 变量的值将为 ``None`` ；

``acquire()`` 方法最后会通过检查 ``result`` 变量的值是否为 ``True`` 来判断自己是否成功取得了锁。

释放操作 ``release()`` 方法使用了本书之前没有介绍过的 ``DEL`` 命令，
这个命令接受一个或多个数据库键作为参数，
尝试删除这些键以及与之相关联的值，
并返回被成功删除的键数量作为结果：

::

    DEL key [key ...]

因为 Redis 的 ``DEL`` 命令和 Python 的 ``del`` 关键字重名，
所以在 redis-py 客户端中，
执行 ``DEL`` 命令实际上是通过调用 ``delete()`` 方法来完成的：

::

    self.client.delete(self.key) == 1

``release()`` 方法通过检查 ``delete()`` 方法的返回值是否为 ``1`` 来判断删除操作是否执行成功：
如果用户尝试对一个尚未被获取的锁执行 ``release()`` 方法，
那么方法将返回 ``false`` ，
表示没有锁被释放。

在使用 ``DEL`` 命令删除代表锁的字符串键之后，
字符串键将重新回到没有值的状态，
这时用户就可以再次调用 ``acquire()`` 方法去获取锁了。

以下代码演示了这个锁的使用方法：

::

    >>> from redis import Redis
    >>> from lock import Lock
    >>> client = Redis(decode_responses=True)
    >>> lock = Lock(client, 'test-lock')
    >>> lock.acquire()  # 成功获取锁
    True
    >>> lock.acquire()  # 锁已被获取，无法再次获取
    False
    >>> lock.release()  # 释放锁
    True
    >>> lock.acquire()  # 锁释放之后可以再次被获取
    True

虽然代码清单 2-2 中展示的锁实现了基本的获取和释放功能，
但它并不完美：

1. 因为这个锁的释放操作无法验证进程的身份，
   所以无论执行释放操作的进程是否就是锁的持有者，
   锁都会被释放。
   如果锁被持有者以外的其他进程释放了的话，
   那么系统中可能就会同时出现多个锁，
   导致锁的唯一性被破坏。

2. 这个锁的获取操作不能设置最大加锁时间，
   它无法让锁在超过给定的时限之后自动释放。
   因此，
   如果持有锁的进程因为故障或者编程错误而没有在退出之前主动释放锁，
   那么锁就会一直处于已被获取的状态，
   导致其他进程永远无法取得锁。

本书后续将继续改进这个锁实现，
使得它可以解决这两个问题。



