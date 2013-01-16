.. highlight:: c

第 8 章：进程控制
=========================

进程标识符
----------------

每个进程都拥有一个非负整数表示的唯一进程 ID ，
这个 ID 可以用 ``getpid`` 函数查看：

::

    #include <unistd.h>

    pid_t getpid(void);

示例：

.. literalinclude:: code/8-getpid.c

执行：

::

    $ ./8-getpid.out 
    Process id = 6754

除了 ``getpid`` 以外，其他一些函数也可以返回进程相关的其他 ID ：

::

    #include <unistd.h>

    // 返回调用进程的父进程 ID
    pid_t getppid(void);    

    // 调用进程的实际用户 ID
    pid_t getuid(void);     

    // 调用进程的有效用户 ID
    pid_t geteuid(void);    

    // 调用进程的实际组 ID
    gid_t getgid(void);     

    // 调用进程的有效组 ID
    gid_t getegid(void);    

示例：

.. literalinclude:: code/8-ids.c

执行：

::

    $ ./8-ids.o 
    Parent pid = 6738
    Uid = 1000
    Euid = 1000
    Gid = 1000
    Egid = 1000


创建进程
-----------

一个进程可以通过调用 ``fork`` 函数来创建另一个进程，
调用 ``fork`` 的函数被称为父进程（parent process），
而被创建的进程则称为子进程（child process）：

::

    #include <unistd.h>

    pid_t fork(void);

``fork`` 函数调用一次却返回两次，
子进程返回 ``0`` ，而父进程返回子进程的 ID 。

父子进程继续执行 ``fork`` 调用之后的指令。

子进程是父进程的副本，它拥有父进程数据空间、堆和栈的副本。
两个进程之间的副本是不共享的，它们只是数据一样，但父子进程共享程序的正文段。

示例：

.. literalinclude:: code/8-fork.c

执行：

::

    $ ./8-fork.out 
    Parent process running, id = 7549
    Child process running, id = 7550
    Child process's parent id = 7549

一般来说，父子进程执行的先后顺序是不确定的，
进程间的同步需要某种形式的进程间通讯才能实现，
所以编程多进程程序时，要小心，不要写出依赖某种执行顺序的程序。


fork 的用法
--------------

``fork`` 的常见用法有两种：

1. 创建父进程的副本，子进程和父进程执行不同的代码段 —— 常用于网络程序

2. 调用 ``exec`` 或其变种，执行另一个程序 —— 常用于 shell


父子进程间的数据副本
------------------------

在前面说到，子进程会复制父进程数据的副本，以下示例程序展示了这一情况：

.. literalinclude:: code/8-data-duplicate.c

执行：

::

    $ ./8-data-duplicate.out 
    init global = 0 , local = 0
    child running, global = 1 , local = 1
    parent running, global = 1 , local = 1

可以看到，无论是子进程也好，父进程也好，
它们对全局变量 ``global`` 和局部变量 ``local`` 的修改都只限于它们自己的内存空间中。

如果进程之间是共享数据的话，
那么不管父子进程的执行顺序如何，
对 ``global`` 和 ``local`` 的两次输出中都会有一次它们的值都变为 ``2`` 。


父子进程间的文件描述符副本
----------------------------

父进程打开的所有文件描述符，
都会被复制到子进程当中，
父子进程的每个相同的打开描述符共享一个文件表项：

.. image:: image/8-share-file.png

以下示例程序演示了父子进程如何写入内容到同一个文件，
其中文件由父进程打开，
而子进程继承了父进程的 ``FILE`` 结构（以及它的文件描述符）：

.. literalinclude:: code/8-share-file.c

执行：

::

    $ ./8-share-file.out 
    $ cat 8-share-file-text 
    child write
    parent write


父子进程的属性
-------------------

除了打开文件之外，父进程的很多其他属性也由子进程继承，包括：

- 实际用户 ID 、实际组 ID 、有效用户 ID 、有效组 ID

- 附加组 ID

- 进程组 ID

- 会话 ID

- 控制终端

- 设置用户 ID 标识和设置组 ID 标识

- 当前工作目录（CWD）

- 根目录

- 文件模式创建屏蔽字

- 信号屏蔽和安排

- 针对任意打开文件描述符的在执行时关闭（close-on-exec）标识

- 环境

- 链接的共享存储段

- 存储映射

- 资源限制

父子进程之间的区别是：

- ``fork`` 的返回值

- 进程 ID 不同

- 两个进程具有不同的父进程 ID 

- 子进程的 ``tms_utime`` 、 ``tms_stime`` 、 ``tms_cutime`` 以及 ``tms_ustime`` 均被设置为 ``0`` 

- 父进程的文件所不会被子进程继承

- 子进程的未处理闹钟（alarm）被清除

- 子进程的未处理信号集为空集


