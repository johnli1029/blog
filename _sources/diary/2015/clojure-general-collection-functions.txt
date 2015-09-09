.. highlight:: clojure

Clojure 收集器通用操作函数简介
====================================


一般操作
-------------------

``count``
^^^^^^^^^^^^^^^^^^

::

    (count coll)

返回收集器包含的元素数量。
``(count nil)`` 将返回 ``0`` 。
这个函数也适用于字符串、数组、Java 收集器以及映射。

::

    user=> (count nil)
    0

    user=> (count [])
    0

    user=> (count [1 2 3])
    3

    user=> (count {:one 1 :two 2})
    2


``empty``
^^^^^^^^^^^^^^^^^^^

::

    (empty coll)

返回一个与给定收集器类型相同的空收集器，
当给定值不是收集器或者未被支持时，
返回一个 ``nil`` 。

::

    user=> (empty (list 1 2 3))
    ()

    user=> (empty {:a 1 :b 2})
    {}

    user=> (empty [1 2 3])
    []

    user=> (empty "hello world")
    nil

    user=> (empty 123)
    nil

    user=> (empty 10086)
    nil


``not-empty``
^^^^^^^^^^^^^^^^^^^

::

    (not-empty coll)

``not-empty`` 函数在给定的收集器为空时返回 ``nil`` ，
非空时返回收集器本身。        

::

    user=> (not-empty [])
    nil

    user=> (not-empty [1 2 3])
    [1 2 3]


``into``
^^^^^^^^^^^^^^^^^^^

::

    (into target source)

    (into target x-source source)

将给定的源收集器与目标收集器进行合并，
然后返回合并后的收集器。
新收集器的类型由目标收集器决定。

::

    user=> (into [1 2 3] [4 5 6])
    [1 2 3 4 5 6]

    user=> (into (sorted-map) {:b 2 :c 3 :a 1})
    {:a 1, :b 2, :c 3}

.. TODO 添加 (into target x-source source) 格式的示例


``conj``
^^^^^^^^^^^^^^^^^^^

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


..
    ``walk``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    ``prewalk``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    ``prewalk-demo``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    ``prewalk-replace``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    ``postwalk``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    ``postwalk-demo``
    ^^^^^^^^^^^^^^^^^^^^^^^^^

    ``postwalk-replace``
    ^^^^^^^^^^^^^^^^^^^^^^^^^


内容测试
-------------------


``distinct?``
^^^^^^^^^^^^^^^^^^^

::

    (distinct? x)

    (distinct? x y)

    (distinct? x y & more)

如果输入的元素各不相同，
那么返回真；
否则返回假。

::

    user=> (distinct? :a)
    true

    user=> (distinct? :a :a :a)
    false

    user=> (distinct? :a :b :c)
    true
        

``empty?``
^^^^^^^^^^^^^^^^^^^

::

    (empty? coll)

如果给定的收集器不包含任何元素，
那么返回真；
否则返回假。
``(empty? coll)`` 等价于 ``(not (seq coll))`` 。

::

    user=> (empty? [])
    true

    user=> (empty? [1 2 3])
    false


``every?``
^^^^^^^^^^^^^^^^^^^

::

    (every? pred coll)

如果收集器里面的所有元素对于给定的条件都返回真，
那么这个函数返回真；
否则返回假。

::

    user=> (every? even? [1 2 3 4])
    false

    user=> (every? even? [2 4 6 8])
    true


``not-every?``
^^^^^^^^^^^^^^^^^^^

::

    (not-every? pred coll)

如果收集器里面有至少一个元素对于给定的条件返回假，
那么这个函数返回真；
否则返回假。

::

    user=> (not-every? even? [1 2 3 4]) 
    true

    user=> (not-every? even? [2 4 6 8])
    false


``some``
^^^^^^^^^^^^^^^^^^^

::

    (some pred coll)

如果收集器里面有至少一个元素符合给定的条件，
那么返回真；
如果所有元素都不符合给定的条件，
那么返回 ``nil`` 。

::

    user=> (some even? [1 2 3])
    true

    user=> (some even? [1 3 5 7])
    nil


``not-any?``
^^^^^^^^^^^^^^^^^^^

::

    (not-any? pred coll)

如果收集器里面的所有元素都不符合给定的条件，
那么返回真；
否则返回假。

::

    user=> (not-any? even? [1 3 5 7])
    true

    user=> (not-any? even? [1 2 3 4])
    false


能力测试
-------------------

``sequential?``
^^^^^^^^^^^^^^^^^^^^^

::

    (sequential? coll)

如果给定的收集器实现了 ``Sequential`` 协议，
那么返回真；
否则返回假。

::

    user=> (sequential? [1 2 3])
    true

    user=> (sequential? #{:a :b :c})
    false

    user=> (sequential? "hello world")
    false


``associative?``
^^^^^^^^^^^^^^^^^^^^^^^^^

::

    (associative? coll)

如果给定的收集器实现了 ``Associative`` 协议，
那么返回真；
否则返回假。

::

    user=> (associative? [1 2 3])
    true

    user=> (associative? {:number 10086 :msg "hello world"})
    true

    user=> (associative? #{:a :b :c})
    false


``sorted?``
^^^^^^^^^^^^^^^^

::

    (sorted? coll)

如果给定的收集器实现了 ``Sorted`` 协议，
那么返回真；
否则返回假。

::

    user=> (sorted? [1 2 3])
    false

    user=> (sorted? (sorted-set [1 2 3]))
    true


``counted?``
^^^^^^^^^^^^^^^^^

::

    (counted? coll)

如果给定的收集器实现了常数复杂度的长度获取功能，
那么返回真；
否则返回假。

::

    user=> (counted? [1 2 3])
    true

    user=> (counted? (list 1 2 3))
    true

    user=> (counted? "hello world")
    false


``reversible?``
^^^^^^^^^^^^^^^^^^^^^^^^

::

    (reversible? coll)

如果给定的收集器实现了 ``Reversible`` 协议，
那么返回真；
否则返回假。

::

    user=> (reversible? "hello world")
    false

    user=> (reversible? [1 2 3])
    true

    user=> (reversible? (list 1 2 3))
    false


类型测试
-------------------

``coll?``
^^^^^^^^^^^^^^^^^^^^^^^^

::

    (coll? x)

如果给定的值实现了 ``IPersistentCollection`` 协议，
那么返回真；
否则返回假。

::

    user=> (coll? #{:a :b :c})
    true

    user=> (coll? [1 2 3])
    true

    user=> (coll? "hello world")
    false

``list?``
^^^^^^^^^^^^^^^^^^^^^^^

::

    (list? x)

如果给定的值实现了 ``IPersistentList`` 协议，
那么返回真；
否则返回假。

::

    user=> (list? [1 2 3])
    false

    user=> (list? (list 1 2 3))
    true

    user=> (list? nil)
    false

``vector?``
^^^^^^^^^^^^^^^^^^^

::

    (vector? x)

如果给定的值实现了 ``IPersistentVector`` 协议，
那么返回真；
否则返回假。

::

    user=> (vector? [1 2 3])
    true

    user=> (vector? {:number 10086 :msg "hello world"})
    false

``set?``
^^^^^^^^^^^^^^^^^^

::

    (set? x)

如果给定的值实现了 ``IPersistentSet`` 协议，
那么返回真；
否则返回假。

::

    user=> (set? #{:a :b :c})
    true

    user=> (set? (sorted-set [:c :b :a]))
    true

    user=> (set? [1 2 3])
    false

``map?``
^^^^^^^^^^^^^^^^

::

    (map? x)

如果给定的值实现了 ``IPersistentMap`` 协议，
那么返回真；
否则返回假。

::

    user=> (map? [1 2 3])
    false

    user=> (map? {:number 10086 :msg "hello"})
    true

``seq?``
^^^^^^^^^^^^^^^

::

    (seq? x)

如果给定的值实现了 ``ISeq`` 协议，
那么返回真；
否则返回假。

::

    user=> (seq? 123)
    false

    user=> (seq? [1 2 3])
    false

    user=> (seq? (seq [1 2 3]))
    true

``record?``
^^^^^^^^^^^^^^^^^^^^^^^^^

::

    (record? x)

如果给定值是一个记录（record），
那么返回真；
否则返回假。

::

    user=> (record? "hello")
    false

    user=> (defrecord DummyRecord [value])
    user.DummyRecord

    user=> (def tmp (->DummyRecord "hello"))
    #'user/tmp

    user=> (record? tmp)
    true

