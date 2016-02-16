《The Go Programming Language》第 1 章笔记
=================================================

.. highlight:: go

安装 Go ：

::

    $ brew install go

查看版本：

::

    $ go version
    go version go1.5.3 darwin/amd64



1.1 节
----------

源码
^^^^^^^^

编写 Hello World ：

.. literalinclude:: code/chp1/helloworld.go

``package`` 用于声明文件所属的包，
其中特殊的 ``main`` 包用于定义一个独立可执行程序（standalone executable program）。

``import`` 用于引入程序需要使用的包，
引入语句需要放在 ``package`` 之后。

``func`` 关键字用于定义函数，
其中特殊的 ``main`` 函数定义了程序开始执行的位置。

Go 不需要在句子之后加分号，
某些 token 之后的新行（newline）会被当作是分号，
因此新行的摆放位置会影响到 Go 的编译。

编译和执行
^^^^^^^^^^^^^^

编译并执行：

::

    $ go run helloworld.go 
    Hello, 世界

编译一个可执行文件，
然后执行该文件：

::

    $ ls
    helloworld.go

    $ go build helloworld.go 

    $ ls
    helloworld    helloworld.go

    $ ./helloworld 
    Hello, 世界

代码格式化
^^^^^^^^^^^^^^^

Go 非常注重源码的格式化。

使用 ``gofmt`` 命令可以将重新格式化之后的代码输出到标准输出：

::

    $ gofmt helloworld.go 
    package main

    import "fmt"

    func main() {
            fmt.Println("Hello, 世界")
    }

使用 ``go fmt`` 命令可以对文件夹内的所有 Go 源代码进行格式化：

::

    $ go fmt


1.2 节
-------------

Slice
^^^^^^^^^^^^^^^^^^

Slice，大小可以动态变化的序列。

Slice 的索引从 ``0`` 开始，
使用 ``s[i]`` 可以取出 Slice 中索引为 ``i`` 的元素；
使用 ``s[m:n]`` 可以取出索引从 ``m`` 直到 ``n-1`` 的元素（半开区间）；
使用 ``s[begin:]`` 可以取出索引从 ``begin`` 开始，
直到 Slice 结尾的所有元素，
相当于执行 ``s[begin:len(s)]`` 。

一个打印所有输入参数的程序
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

以下是一个能够打印出用户输入的所有参数的程序：

.. literalinclude:: code/chp1/echo1.go

程序开始时的 ``//`` 是程序的行注释。

``import`` 语句使用括号包围了被引入的两个包 ``"fmt"`` 和 ``"os"`` ，
使用括号包围多个包名的做法在需要引入多个包时非常方便。

``os`` 包提供了一些与操作系统执行操作所需的函数和值。

``var s, sep string`` 这个语句定义了两个变量 ``s`` 和 ``sep`` ，
它们的类型为字符串类型 ``string`` 。
如果用户在定义变量的时候没有为变量设置初始值，
那么 Go 将把这些变量的值设置为该类型对应的“零值”（zero value），
比如字符串的零值就是空字符串 ``""`` 。

``i := 1;`` 语句定义了一个临时变量 ``i`` ，
它的值为 ``1`` ，
类型为整数。
``:=`` 是 Go 语言用于声明临时变量的语法，
它可以根据变量的初始值，
自动为变量设置相应的类型。

执行示例：

::

    $ go build echo1.go 

    $ ./echo1 hello world in args
    hello world in args

为了提高效率，
我们可以使用 ``strings`` 包中的 ``Join`` 函数来完成字符串的拼接工作，
就像这样：

::

    func main() {
        fmt.Println(strings.Join(os.Args[1:], " "))
    }

``for`` 语句
^^^^^^^^^^^^^^^^^^^^^

``for`` 语句是 Go 中唯一的循环语句，
它有三种形态：

1. 普通的 ``for`` ，
   这种 ``for`` 带有完整的初始化部分、条件部分和递进部分，
   就像这样：

   ::

       for init; condition; step {
           // statements
       }

2. ``while`` 形式的 ``for`` ，
   这种 ``for`` 只有条件部分，
   初始部分通常出现在 ``for`` 之前，
   而递进部分则出现在 ``for`` 内部：

   ::

       for condition {
           // statements
       }

3. 无限循环形式的 ``for`` ，
   这种 ``for`` 通常会在内部设置一个跳出条件：

   ::

       for {
           // statements
       }

除此之外，
``for`` 还可以对字符串或者 slice 这样的数据类型进行范围遍历（iterates over a range of values）。

以下这个程序会使用 ``range`` 产生一组序列，
序列中的每个值都由一个索引以及索引对应的元素组成，
通过 ``for`` 语句可以分别取出它的索引和元素：

.. literalinclude:: code/chp1/test_for_range.go

执行示例：

::

    $ ./test_for_range hello world in args
    0
    hello
    1
    world
    2
    in
    3
    args

空白标识符
^^^^^^^^^^^^^^^^

当我们想要使用 ``for`` 和 ``range`` 对序列进行遍历，
但是又不需要元素的索引时，
可以把索引的变量设置为下划线 ``_`` ，
这样即使这个变量不被使用，
编译器也不会报错：

.. literalinclude:: code/chp1/test_blank_identifier.go

具有这样特殊作用的值 ``_`` 被称为空白标识符（blank identifier）。

执行示例：

::

    $ ./test_blank_identifier hello world in args
    hello
    world
    in
    args

