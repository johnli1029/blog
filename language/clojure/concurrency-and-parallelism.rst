.. highlight:: clojure

并发与并行
=============


延时计算
-------------

使用 ``delay`` 包裹一个给定的表达式，并产生一个延时对象。

当使用 ``deref`` 或者 ``@`` 对这个延时对象进行解引用时，被包裹的表达式才会被求值：

::

    user=> (def d (delay (println "Running...") :done!))
    #'user/d

    user=> d                    ; 未求值的 delay
    #<Delay@4f6e03: :pending>

    user=> @d                   ; 解引用，等同于调用 (deref d)
    Running...              
    :done!

    user=> @d                   ; 值被求值一次之后就会被缓存
    :done!

因为并不对被包裹的表达式进行求值，所以对 ``delay`` 语句的调用总是立即被返回。

使用 ``realized?`` 可以检查一个 ``delay`` 是否已经被解引用过：

::

    user=> (def dd (delay :done!))
    #'user/dd

    user=> (realized? dd)
    false

    user=> @dd 
    :done!

    user=> (realized? dd)
    true


并发线程
--------------

``future`` 将给定的表达式放到一个线程里执行，执行的结果使用解引用取出：

::

    user=> (def f (future 10086))            
    #'user/f

    user=> f
    #<core$future_call$reify__6110@4d6d4e: 10086>

    user=> @f
    10086

解引用是否阻塞，取决于所给定的表达式在新线程里是否已经运行完毕。

比如以下代码就会阻塞几秒钟，因为它创建了一个会阻塞的表达式，并且\ **立即**\ 对它进行解引用：

::

    user=> @(future (Thread/sleep 5000) 10086)  ; ... 需要等待 5 秒
    10086

不论被包裹表达式是否阻塞，对 ``future`` 的调用总是立即返回的，调用者的线程并不会因为 ``future`` 所包裹的表达式而阻塞。

.. note::

    为了进一步优化效率，被 ``future`` 包裹的表达式会被放到一个线程池里执行，而不是直接创建新线程。


数据流变量
------------

``promise`` 声明某个变量为一个数据流变量，表示这个变量『会在将来的某个时候拥有一个值』。

带 ``promise`` 的变量的值通过 ``deliver`` 来设置。

::

    user=> (def p (promise))
    #'user/p

    user=> p
    #<core$promise$reify__6153@638273: :pending>

    user=> (deliver p 10086)
    #<core$promise$reify__6153@638273: 10086>

    user=> @p
    10086

当对一个未有值的 ``promise`` 变量进行求值时，当前线程会被阻塞，直到有其他线程对这个变量进行 ``deliver`` 为止。
