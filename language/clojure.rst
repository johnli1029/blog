.. highlight:: clojure

Clojure
==========


定义变量
-----------


全局变量
^^^^^^^^^^^

``def`` 特殊形式（special form）用于创建一个全局变量（global var）。

::

    user=> (def x 10086)
    #'user/x

    user=> x
    10086

还可以给全局变量添加文档：

::

    user=> (def x "just a value, nothing else." 10086)
    #'user/x

    user=> (doc x)
    -------------------------
    user/x
      just a value, nothing else.
      nil

私有变量可以通过元数据的 ``private`` 关键字来声明：

::

    user=> (def ^{:private true} v 123)
    #'user/v

    user=> (meta #'v)   ; 查看变量的私有变量
    {:ns #<Namespace user>, :name v, :private true, :line 36, :file "NO_SOURCE_PATH"}

如果一个变量是私有的，那么其他命名空间就不可以在外部中引用它。


局部变量
^^^^^^^^^^^^

局部变量由 ``let`` 创建：

::

    user=> (let [v 123]
             v)
    123

``let`` 中的多个声明按从先到后的顺序求值，因此，靠后的声明可以引用前面的声明：

::

    user=> (let [a 1            ; 1
                 b (+ a 1)      ; 2
                 c (+ a b)]     ; 3
             c)
    3


动态变量
^^^^^^^^^^^

一般情况下，Clojure 使用静态作用域来处理变量，使用 ``dynamic`` 元数据关键字，以及 ``binding`` 宏，可以将变量改为动态作用域：

::

    user=> (def ^:dynamic x 1)
    #'user/x

    user=> (def ^:dynamic y 2)
    #'user/y

    user=> (+ x y)
    3

    user=> (binding [x 123 y 123]   ; 使用动态绑定覆盖原来的绑定
             (+ x y))
             246

    user=> (+ x y)
    3


定义函数
----------


匿名函数
^^^^^^^^^^^^

Clojure 使用 ``fn`` 来创建匿名函数：

::

    user=> (fn [] "hello moto")                         ; 无参数匿名函数
    #<user$eval53$fn__54 user$eval53$fn__54@81876b>

    user=> ((fn [] "hello moto"))                       ; 执行匿名函数
    "hello moto"

    user=> (fn [name] (str "hello " name))              ; 一个接受单个参数的匿名函数
    #<user$eval72$fn__73 user$eval72$fn__73@1dafee2>

    user=> ((fn [name] (str "hello " name)) "moto")     ; 使用 "moto" 作为参数调用匿名函数
    "hello moto"


具名函数
^^^^^^^^^^

使用 ``def`` 可以为函数绑定一个名字：

::

    user=> (def msg (fn [] "hello moto"))
    #'user/msg

    user=> (msg)
    "hello moto"

创建具名函数的更简便方式是使用 ``defn`` 宏：

::

    user=> (defn msg [] "hello moto")
    #'user/msg

    user=> (msg)
    "hello moto"


多种参数函数(arity)
^^^^^^^^^^^^^^^^^^^^^^^

一个函数可以接受多种参数作为函数：

::

    (defn msg
      ([] "hello moto")
      ([name] (str "hello " name))
    )

上面定义的 ``msg`` 函数接受两种参数，如果不给定参数调用 ``msg`` ，那么函数返回 ``hello moto`` ；如果给定 ``name`` 参数，那么函数根据 ``name`` 变量返回问候语：

::

    user=> (msg)
    "hello moto"

    user=> (msg "moto")
    "hello moto"

    user=> (msg "huangz")
    "hello huangz"


函数的前置和后置条件
^^^^^^^^^^^^^^^^^^^^^^^

在定义函数时，可以为函数的参数设置前置条件，为函数的返回值设置后置条件，如果前置条件或者后置条件任意一个为假，那么函数会抛出 ``AssertionError`` ：

::

    (defn msg [name]
        {
         :pre [(< (count name) 10)          ; name 长度小于 10
               (> (count name) 3)]          ; name 长度大于 3
         :post [(not (= % "hello moto"))]   ; 返回值不能是 "hello moto"
        }   
        (str "hello " name)
    )

测试：

::

    user=> (msg "huangz")
    "hello huangz"

    user=> (msg "longgggggggggggggggggggggggggggggggg")
    AssertionError Assert failed: (< (count name) 10)  user/msg (t.clj:1)

    user=> (msg "s")
    AssertionError Assert failed: (> (count name) 3)  user/msg (t.clj:1)

    user=> (msg "moto")
    AssertionError Assert failed: (not (= % "hello moto"))  user/msg (t.clj:1)

对于多种参数函数，每个函数都要根据各自的参数设置自己的前置和后置条件：

::

    (defn f 
        ([arg] 
            {:pre [] :post []} 
            ;...
        )
        ([arg1 arg2]
            {:pre [] :post []}
            ;...
        )
    )


使用 reader 宏创建匿名函数
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reader 宏 ``#`` 根据公式 ``#(...) => (fn [args] (...))`` 来生成函数。

::

    (def msg #(str "hello " %))


以上定义等同于：

::

    (def msg 
        (fn [name]
            (str "hello " %)
        )
    )

宏中的参数用 ``%`` 来表示， ``%`` 或者 ``%1`` 表示第一个参数， ``%2`` 表示第二个参数，以此类推。

这种宏一般用于生成高阶函数所使用的匿名函数，非常简单且紧凑：

::

    user=> (filter #(and (even? %) (< % 10)) (range 100))
    (0 2 4 6 8)

以上代码只保留 0 至 99 数值序列中为偶数且小于 10 的数值。


使用 letfn 定义临时函数
^^^^^^^^^^^^^^^^^^^^^^^^

``letfn`` 用于创建局部的、具名函数，这些函数的作用域被限制在 ``letfn`` 体内，通常作为临时函数使用。

::

    user=> (letfn [(twice [x] (* x 2))
                   (six-times [y] (* 3 (twice y)))]
             (println "Twice 15 = " (twice 15))
             (println "Six times 15 = " (six-times 15)))
    Twice 15 = 30
    Six times 15 = 90
    nil

    ;; 名字 twice 和 six-times 在离开 letfn 之后不可用

    user=> (twice 15)
    CompilerException java.lang.RuntimeException: Unable to resolve symbol: twice in this context, compiling:(NO_SOURCE_PATH:7)

    user=> (six-times 15)
    CompilerException java.lang.RuntimeException: Unable to resolve symbol: six-times in this context, compiling:(NO_SOURCE_PATH:8)


私有函数
^^^^^^^^^^^

私有函数可以使用 ``defn-`` 宏来定义，除了生成的函数是私有的之外，它的其他属性和选项跟 ``defn`` 创建的函数没什么不同。

::

    user=> (defn- msg [] "hello moto")
    #'user/msg

    user=> (msg)
    "hello moto"

    user=> (meta #'msg)
    {:arglists ([]), :ns #<Namespace user>, :name msg, :private true, :line 1, :file "NO_SOURCE_PATH"}


条件求值
---------------


if
^^^^^

``if`` 接受三个单行表达式， ``test`` 、 ``then`` 和 ``else`` 。

如果 ``test`` 部分为真，那么就执行 ``then`` 部分；如果 ``test`` 部分为假，那么执行 ``else`` 部分。

::

    user=> (if true   
             "is true"
             "is false")
    "is true"

    user=> (if false 
             "is true"
             "is false")
    "is false"

``else`` 部分并不是必须的，如果省略 ``else`` 部分，那么条件为假时返回 ``nil`` 。

::

    user=> (if true "is true")
    "is true"

    user=> (if false "is true")
    nil


do
^^^^^

``do`` 可以包围任意数量的表达式，并按顺序求值这些表达式，然后返回最后一个表达式的值作为 ``do`` 的返回值，如果 ``do`` 里面没有表达式，那么返回 ``nil`` 。

::

    user=> (do 
             (prn "hello")
             (prn "moto"))
    "hello"
    "moto"
    nil

利用 ``do`` ，我们可以让 ``if`` 也能处理多条语句：

::

    user=> (if true
             (do
                (prn "hello")
                (prn "moto")))
    "hello"
    "moto"
    nil


when
^^^^^^

``when`` 和 ``if`` 不同，它只处理条件部分为真时的情况，而且 ``when`` 的体内可以包括多条语句，而不是像 ``if`` 那样，只能处理单条语句：

::

    user=> (when true
             (prn "hello")
             (prn "moto"))
    "hello"
    "moto"
    nil

当条件部分为假时， ``when`` 只是简单地返回 ``nil`` ：

::

    user=> (when false
             (prn "hello")
             (prn "moto"))
    nil

正如你所想象的， ``when`` 实际上就是 ``if`` 和 ``cond`` 组合构成得出的。   


cond
^^^^^^

``cond`` 接受任意数量的 ``test`` - ``exp`` 对，按顺序对各个 ``test`` 进行测试，并求值第一个为真 ``test`` 所对应的 ``exp`` 表达式；如果没有任何 ``test`` 为真，那么返回 ``nil`` 。

::

    (cond true "moto")  ; => "moto"

    (cond false "hello"
          true "moto")  ; => "moto"

    (cond false "hello"
          true "moto"
          true "google")    ; => "moto"

    (cond false "hello")    ; => nil


if-not 、 when-not
^^^^^^^^^^^^^^^^^^^^

``if-not`` 和 ``when-not`` 处理跟 ``if`` 和 ``when`` 相反的情况，它们只是 ``(if (not ...))`` 和 ``(when (not ...))`` 的一个快捷方式。

::

    user=> (if-not false "moto")
    "moto"

    user=> (when-not false "hello")
    "hello"


if-let 、 when-let
^^^^^^^^^^^^^^^^^^^^

``if-let`` 和 ``when-let`` 处理在条件判断前，先要创建局部变量的情况；它们分别是 ``(if (let ...))`` 和 ``(when (let ...))`` 的快捷方式：

::

    (if-let [test true]        
        "is true"
        "is false"
    )

    ; => "is true"

    (when-let [test true]
        "is true"
    )
    ; => "is true"

要注意的一点是， ``if-let`` 允许创建多个局部变量，而 ``when-let`` 只能创建一个局部变量（这是由 ``when`` 的性质决定的）。

.. for

.. recur

.. loop

.. while
