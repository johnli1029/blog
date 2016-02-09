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
