.. highlight:: clojure

序列
=====

序列是一个逻辑列表， Clojure 通过底层的 ``ISeq`` 接口来对序列进行支持，允许其他容器创建遍历自身元素的序列。每种 Clojure 容器都至少提供一种或以上的序列对象。

可以将序列看作是没有带状态指针、持久化和不可改版本的迭代器或枚举器。


序列接口
----------

要使得容器支持序列操作，最起码要实现以下三个 API ，它们分别是 ``cons`` 、 ``first`` 和 ``rest`` 。

``(cons item seq)`` 创建一个包含新元素的序列：

::

    user=> (cons 1 '())
    (1)

    user=> (cons 1 '(2 3))
    (1 2 3)

    user=> (cons 1 '())          
    (1)

    user=> (cons 1 (cons 2 (cons 3 '())))
    (1 2 3)

``(first coll)`` 返回序列中的第一个元素，如果传入序列为空，那么返回 ``nil`` ：

::

    user=> (first '())
    nil

    user=> (first '(1))
    1

    user=> (first '(1 2))
    1

``(rest coll)`` 返回序列中除第一个元素之外的其他元素，如果传入序列为空，那么返回空序列 ``'()`` ：

::

    user=> (rest '())
    ()

    user=> (rest '(1))
    ()

    user=> (rest '(1 2))
    (2)

    user=> (rest '(1 2 3))
    (2 3)


创建序列对象
--------------

使用 ``seq`` 函数是创建序列对象最常用的方式，传入的参数可以是任何 Clojure 容器类型，或者是实现了 ``Iterable`` 接口的 JAVA 对象：

::

    user=> (seq "hello moto")
    (\h \e \l \l \o \space \m \o \t \o)

    user=> (seq (list 1 2 3))
    (1 2 3)

    user=> (seq [1 2 3])
    (1 2 3)

    user=> (seq {:clojure ".clj" :haskell ".hs" :scheme ".scm"})
    ([:scheme ".scm"] [:clojure ".clj"] [:haskell ".hs"])

    user=> (seq #{1 2 3})
    (1 2 3)

还有一些其他创建列表对象的方法，比如 ``keys`` 和 ``vals`` ，以及 ``rseq`` ，诸如此类。


处理序列
----------

Clojure 提供了一集非常丰富的函数来对序列进行操作，比如常见的 ``map`` 、 ``filter`` 、 ``reduce`` 等等，在\ `Sequence 的文档页面 <http://clojure.org/sequences>`_\ 详细地列出了这些 API 。
