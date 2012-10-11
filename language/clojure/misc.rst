.. highlight:: clojure

杂项
=========


文件载入
----------

对一些小程序进行原型测试的时候，通常要在 REPL 中进行一些重复的输入，一个更好的办法是将程序保存进某个文件，然后在 REPL 中通过载入文件来避免重复输入。

``load-file`` 函数读入并求值指定文件。

假如现在有文件 ``greet.clj`` ，内容如下：

::

    ;;; greet.clj

    (defn greeting []
        (str "hello"))

    (greeting)

之后可以使用 ``load-file`` 对它进行读入和求值：

::

    user=> (load-file "greet.clj")
    "hello"


延迟求值
----------

Clojure 提供了一组原语，用于实现延迟求值。

``delay`` 延缓对一个表达式的求值，直到对它调用 ``force`` 为止:

::

    user=> (def d (delay (+ 1 1)))
    #'user/d

    user=> d
    #<Delay@14fa3ef: :pending>

    user=> (class d)
    clojure.lang.Delay

    user=> (force d)
    2

    user=> d
    #<Delay@14fa3ef: 2>

    user=> (class d)
    clojure.lang.Delay
