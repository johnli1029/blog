.. highlight:: clojure

Clojure 列表常用函数简介
===============================

这篇文章列出了 Clojure 列表类型的一些常用函数，
并简单介绍了它们的使用方法。

创建列表
-----------------------

``()``
^^^^^^^^^^^^^^^^

通过使用 ``()`` 包围多个元素可以创建出一个列表：

::

    user=> '()
    ()

    user=> '(1 2 3)
    (1 2 3)

    user=> (type '())
    clojure.lang.PersistentList$EmptyList

    user=> (type '(1 2 3))
    clojure.lang.PersistentList


``list``
^^^^^^^^^^^^^^^^

::

    (list & items)

创建一个包含给定元素的列表。

::

    user=> (list)
    ()

    user=> (list 1 2 3)
    (1 2 3)


``list*``
^^^^^^^^^^^^^^^^

::

    (list* args)

    (list* a args)

    (list* a b args)

    (list* a b c args)

    (list* a b c d & more)

通过将多个元素添加到指定序列的前面来创建出一个新的列表。

::

    user=> (list* 1 [2 3 4])
    (1 2 3 4)

    user=> (list* 1 2 3 [4 5 6]) 
    (1 2 3 4 5 6)

    user=> (list* 1 2 (list 3 4))
    (1 2 3 4)


查看列表元素
-----------------------

``first``
^^^^^^^^^^^^^^^^

::

    (first coll)

对给定收集器调用 ``seq`` 函数，
然后返回这个收集器的第一个元素。
如果收集器为 ``nil`` ，
那么返回 ``nil`` 。

::

    user=> (first nil)
    nil

    user=> (first (list 1 2 3))
    1

    user=> (first [1 2 3])
    1


``nth``
^^^^^^^^^^^^^^^^

::

    (nth coll index)

    (nth coll index not-found)

返回收集器在给定索引上面的值。
``get`` 函数在索引超出范围的时候会返回 ``nil`` ，
但是这个函数在超出范围并且没有给定 ``not-found`` 的情况下则会抛出一个异常。

除了收集器之外，
``nth`` 还可以用于字符串、Java 数组、正则表达式匹配器、列表，
或者以 O(N) 复杂度处理序列。

::

    user=> (nth (list "hello" "world" "again") 2)
    "again"

    user=> (nth [:a :b :c :d] 1)
    :b

    user=> (nth [:a :b] 100 "not-found-index-100")
    "not-found-index-100"

    user=> (nth "hello world" 0)
    \h

    user=> (nth "hello world" 4)
    \o


``peek``
^^^^^^^^^^^^^^^^

::

    (peek coll)

对于列表或者队列来讲，
这个函数的作用和 ``first`` 一样；
对于向量，
这个函数的作用和 ``last`` 函数一样，
但这个函数更加高效。

如果序列为空，
那么返回 ``nil`` 。

::

    user=> (def large-vector (vec (range 0 10000)))  
    #'user/large-vector

    user=> (time (last large-vector))
    "Elapsed time: 12.386063 msecs"

    9999
    user=> (time (peek large-vector))
    "Elapsed time: 0.110279 msecs"
    9999

    user=> (first (list 1 2 3))
    1

    user=> (peek (list 1 2 3))
    1


``.indexOf``
^^^^^^^^^^^^^^^^

::

    (.indexOf coll item)

在收集器里面进行搜索，
查找 ``item`` 元素第一次出现时的索引，
在没有找到给定元素的情况下，
返回 ``-1`` 。

..  TODO 不能给定 index 参数？

    (.indexOf coll item index)

    在收集器里面进行搜索，
    查找 ``item`` 元素第一次出现时的索引，
    如果给定了可选的 ``index`` 参数，
    那么从给定的索引开始进行搜索。
    在没有找到给定元素的情况下，
    返回 ``-1`` 。

::

    user=> (.indexOf [:a :b :c] :b)
    1


``.lastIndexOf``
^^^^^^^^^^^^^^^^^^^^^^

::

    (.lastIndexOf coll item)

在收集器里面进行搜索，
查找 ``item`` 元素最后一次出现时的索引；
在没有找到给定元素的情况下，
返回 ``-1`` 。

::

    user=> (.lastIndexOf [:a :b :c :d :a :b] :a)
    4


对列表进行“修改”
-----------------------

``cons``
^^^^^^^^^^^^^^^^^^^^

::

    (cons x seq)

返回一个新的序列，
这个序列的第一个元素为 ``x`` ，
之后的元素为 ``seq`` 中包含的元素。

::

    user=> (cons "hello" (list "world" "again"))
    ("hello" "world" "again")

    user=> (cons 1 [2 3 4])
    (1 2 3 4)


``conj``
^^^^^^^^^^^^^^^^^^^^

::

    (conj coll x)

    (conj coll x & xs)

返回将一个或多个新元素添加到给定收集器之后产生的新序列。
根据收集器类型的不同，
新元素可能会被添加到收集器的不同位置。

::

    user=> (conj (list 2 3 4) 1)
    (1 2 3 4)

    user=> (conj [2 3 4] 1)
    [2 3 4 1]

    user=> (conj {:redis "Redis.io" :mongodb "MongoDB.com"} {:mysql "MySQL.com"})
    {:redis "Redis.io", :mongodb "MongoDB.com", :mysql "MySQL.com"}


``rest``
^^^^^^^^^^^^^^^^^^^^

::

    (rest coll)

返回序列里面，
除第一个元素之外的其他所有元素；
如果序列没有除第一个元素之外的其他元素，
那么函数返回 ``nil`` 。

``rest`` 函数会对传入的值调用 ``seq`` 函数。

::

    user=> (rest '())
    ()

    user=> (rest nil)
    ()

    user=> (rest '(1))
    ()

    user=> (rest '(1 2 3))
    (2 3)

    user=> (rest [1 2 3 4])
    (2 3 4)


``pop``
^^^^^^^^^^^^^^^^^^^^

::

    (pop coll)

对于传入的列表或者队列，
这个函数返回一个不包含传入列表/队列第一个元素的新列表/队列。
如果传入的收集器为空，
那么函数抛出一个异常。

注意这个函数和 ``next`` 或者 ``butlast`` 之间并不相同。

::

    user=> (pop '(1 2 3))
    (2 3)

    user=> (pop [:a :b :c :d])
    [:a :b :c]

    user=> (pop nil)
    nil

    user=> (pop '())
    IllegalStateException Can't pop empty list  clojure.lang.PersistentList$EmptyList.pop (PersistentList.java:181)
