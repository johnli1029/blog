《Go实战》第 1 章：入门知识
======================================

1.1.2 并发
^^^^^^^^^^^^^^^^^^

编写出能够高效地利用硬件可用资源的程序，
一直是程序员最困难的任务之一。
尽管现代的计算机都具有多个核心，
但是大多数编程语言却仍然缺少有效的工具，
无法轻而易举地利用这些额外的计算资源。
这些语言通常会用到大量的线程同步代码，
而这些代码可能隐藏着错误。

对并发的支持是 Go 最强有力的特性之一。
goroutine 类似于线程，
但使用 goroutine 所需的内存和代码都比线程要少得多。
此外，
channel 数据结构允许我们通过内置的同步机制，
在多个 goroutine 之间发送带类型的消息（typed messages），
这有助于我们构建起一种在多个 goroutine 之间发送数据的编程模型，
而不必让多个 goroutine 去争抢同一数据的使用权。
接下来，
就让我们进一步地了解以上提到的这两个特性。

goroutine
"""""""""""""""""

goroutine 是一种能够与其他 goroutine 并发运行的函数，
Go 程序的入口（entry point）也是一个 goroutine 。
在其他编程语言里面，
我们通常需要使用多个线程才能做到并发运行，
但是在 Go 语言里面，
多个 goroutine 可以运行在单个线程之上。

举个例子，
假如我们想要用 C 或者 JAVA 编写一个能够同时处理多个不同 web 请求的 web 服务器，
那么为了使用多个线程，
我们就不得不编写大量额外的代码。
与此相反，
Go 语言的 ``net/http`` 函数库已经通过 goroutine 实现了内置的并发特性。
每个到达的请求都会自动地运行在它们各自的 goroutine 之上。

goroutine 不仅使用的内存比线程少，
并且 Go 的运行时环境（runtime）还会自动地对 goroutine 进行调度，
让 goroutine 可以运行在一组配置好（configured）的逻辑处理器之上，
而每个逻辑处理器都与一个操作系统线程绑定。
goroutine 使得我们的应用程序可以更加高效地运行，
并且显著地减少开发应用程序所需要做的工作。

----

.. image:: image/figure-1-2.png

图 1-2 一个操作系统线程之上可以运行多个 goroutine

----

如果我们希望程序在继续完成其他任务的同时，
并发地执行某些代码，
那么 goroutine 就是完成这一目的的最佳工具。
以下是一个使用 goroutine 的简单例子：

.. code-block:: go

    func log(msg string){
            ... some logging code here
    }

    // Elsewhere in our code after we've discovered an error.
    go log("something dire happened")

``go`` 关键字使得 ``log`` 函数能够被调度为 goroutine ，
并与其他 goroutine 一起并发地执行。
这意味着我们可以在并发地执行日志操作的同时，
继续执行程序的后续部分，
从而给终端用户带来更好的性能体验。
正如之前所说，
goroutine 带来的性能损耗（overhead）非常非常少，
因此并发地使用数万个 goroutine 的情形并不少见。
本书的第 6 章将更深入地介绍 goroutine 和并发。

channel
""""""""""""

channel 是一种能够在多个 goroutine 之间提供安全的数据通信的数据结构，
它可以帮助我们避免那些在允许共享内存访问的编程语言里面经常会出现的问题。

并发最困难的部分，
就是防止数据被其他并发运行的进程、线程或者 goroutine 意外地修改了。
当多个线程在没有锁或者未经同步的情况下对相同的数据进行修改时，
令人头疼的问题就会接踵而来。
在具有全局变量和共享内存特性的编程语言中，
我们只能够通过复杂的加锁机制来防止对相同的变量进行未经同步的修改。

channel 通过提供一种能够在并发修改时保证数据安全的模式来帮助解决这个问题，
它有助于确保“在任意时刻，应该只有一个 goroutine 对数据进行修改”这一模式的实施。
图 1-3 展示了这种修改流程的一个示例，
在这个示例里面，
channel 被用于在多个运行中的 goroutine 中发送数据。
假如在一个程序里面，
有多个不同的进程需要按次序地读取或者修改数据，
那么我们可以通过 goroutine 和 channel 来安全地实现这一过程。

----

.. image:: image/figure-1-3.png

图 1-3 使用频道，在 goroutine 之间安全地传递数据

----

图 1-3 展示了三个 goroutine 以及两个无缓存（unbuffered） channel 。
其中，
第一个 goroutine 会通过 channel 向正在等待的第二个 goroutine 传递一个数据值。
这一数据交换操作对于两个 goroutine 来说都是同步的，
并且当数据的推送工作进行完毕时，
两个 goroutine 都会知道数据交换已经成功。
当第二个 goroutine 完成了它对数据需要执行的任务之后，
它就会把数据传递给正在等待的第三个 goroutine 。
跟之前一样，
数据的交换操作是同步地进行的，
并且两个 goroutine 都会保证数据的交换操作顺利地完成。
goroutine 之间的这种安全的数据交换不需要用到其他加锁或者同步机制。

需要注意的一点是，
channel 并没有为 goroutine 之间的数据访问提供任何保护。
如果通过 channel 交换的是数据的拷贝（copy），
那么每个 goroutine 都会拥有它们自己的拷贝，
并且可以安全地对各自的拷贝进行任意修改。
但如果 channel 交换的是数据的指针（pointer），
并且这些数据将被不同的 goroutine 读取和写入，
那么读写这些数据的每个 goroutine 仍然需要进行同步。
