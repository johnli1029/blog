第一章： 计算系统简介
===============================================

为什么阅读本书？

- 了解计算机的底层运作方式

- 识别、避免、处理因为不了解底层而引发的各种错误

- 利用底层设计，写出更高效的程序


1.1 信息就是位和上下文(context)
--------------------------------------------

.. code-block:: c

    // hello.c

    #include <stdio.h>

    int main()
    {
        printf("hello, world\n");
    }

以下是 ``hello.c`` 的 ASCII 文本表示：

.. image:: image/hello_c_in_ascii.png

- ``hello.c`` is a *source file* (or *source program*),
  it's a sequence of bits,
  each with a value ``0`` or ``1`` ,organized in 8-bit chucks called *bytes* ,
  each byte represents some text character in the program.

- ``hello.c`` 可以被称为源文件，或者源程序，
  它由一系列位组成，
  每个位的值可以是 ``0`` 或者 ``1`` ，
  每 8 个位组成一个块（chunk），
  每个字节都表示了源文件中的某个字符。

- most modern systems represent text characters using the ASCII standard that represents each character with a unique byte-sized integer value.

- 大多数现代系统都使用 ASCII 标识来表示字符，
  在这个标准中，
  每个字符都被表示成长度为一个字节的、不相同（unique）的整数。

- a file that consist exclusively of ASCII characters are known as *text files*,
  all other files are known as *binary files*.

- 一个只包含 ASCII 字符的文件被称为文本文件，
  而其他所有文件都被称为二进制文件。

----

- All information in a system—
  including disk files, programs stored in memory, user data stored in
  memory, and data transferred across a network—is represented as a bunch of bits.

- 系统中的所有信息 ——
  包括磁盘文件，内存中的程序，内存中的用户数据，
  通过网络传送的数据，等等，
  都是由一系列字节来表示的。

- The only thing that distinguishes different data objects is the context in which
  we view them.

- 不同数据对象的区别在于，我们在什么上下文中处理它们。

- For example, in different contexts, the same sequence of bytes
  might represent an integer, floating-point number, character string, or machine
  instruction.

- 比如说，
  在不同的上下文中，
  同样的一串字节可能会被表示为整数、浮点数、字符串、或者机器指令。



1.2 源码由程序转换为不同的格式
---------------------------------

- C program can be read and understood by human beings in high-level form.

- C 语言是高层次的，它可以被人类阅读和理解。

- However, in order to run program on the system, the individual C statements must be translated by other programs into a sequence of low-level *machine-language* instructions.

- 但是为了在系统中执行这个 C 程序，
  我们必须使用一些程序，
  将这个 C 程序转换为一串低层次 *机器语言* 指令。

- Machine-language instructions are then packaged in a form called an *executable object program* and stored as a binary disk file.

- 这些机器指令之后会被打包为一个 *可执行对象程序* ，并保存为二进制文件。

- Object programs are also referred to as *executable object files*.

- 对象程序通常也被成为 *可执行对象文件* 。

----

以下是将一个 ``hello.c`` 源程序翻译为一个可执行二进制文件 ``hello`` 的步骤：

::

    unix> gcc -o hello hello.c

以下是 gcc 翻译文件的过程，
以及翻译涉及的程序：

.. image:: image/compilation_system.png

翻译总共由四个程序执行，
它们总称为编译系统（compilation system），
分别是：
预处理器（preprocessor）、
编译器（complier）、
汇编器（assembler）、
链接器（linker）。

这四个程序进行翻译的四个阶段分别是：

- 预处理阶段：
  根据 ``#`` 命令，
  对源码进行处理（插入、替换，等等）。

- 编译阶段：
  将程序翻译成汇编语言。

- 汇编阶段：
  将汇编翻译成机器语言，
  并打包成一个可重载对象程序（relocatable object program）。

- 链接阶段：
  将预编译文件合并到可重载对象程序里面，
  并产生一个可执行对象文件（executable object file）。



1.3 理解编译系统的运行是有益的
---------------------------------

无



1.4 处理器读入并执行保存在内存里的指令
-------------------------------------------

当我们在终端中执行 ``hello`` 程序时，
将获得以下结果：

::

    unix> ./hello
    hello, world
    unix>

要理解系统如何执行这个程序，
并产生输出，
我们需要了解系统的硬件组织。


1.4.1 系统的硬件组织
^^^^^^^^^^^^^^^^^^^^^^^^^

以下是典型的系统结构组织图：

.. image:: image/1.4.png

bus （总线）
""""""""""""""""

- 连接各个部件的电子管道，负责在各个部件中传送数据。

- 通常以字（word）为单位传送数据，字通常是固定大小的。

- 现代机器的字一般是 4 字节（32 位）或 8 字节（64 位）。

I/O devices（输入/输出设备）
"""""""""""""""""""""""""""""""

- 输入/输出设备是系统连接系统和外界

- 每个 I/O 设备都通过 I/O 总线连接到一个控制器（controller）或是适配器（adapter）上面。

- 控制器和适配器之间的差别是：

  - 控制器是设备本身带有的、或是主板（motherboard）附带的芯片组。

  - 适配器则是通过主板接口插入到系统的。

  不过它们都同样用于在 I/O 总线和 I/O 设备之间传送数据。

main memory（主存）
"""""""""""""""""""""""""""""""

- 临时性的储存设备，
  持有处理器正在执行的程序的代码和数据（program and the data）。

- 物理上，由一系列动态随机存储内存（dynamic random access memory，DRAM）组成。

- 逻辑上，内存被组织为一个线性的字节数组，每个字节都带有自己的唯一（unique）地址（数组索引），索引以 ``0`` 开始。

- 一条机器指令通常涉及不定数量的字节，
  比如在 32 位 Linux 上的 C 语言中，
  ``short`` 类型数据的长度为 ``2`` 字节，
  ``int`` 、 ``float`` 和 ``long`` 都是 ``4`` 字节，
  等等。

processor（处理器）
""""""""""""""""""""""""""""""

- 中央处理器（central processing unit，CPU），
  简称处理器（processor)，
  是执行保存在主存中的命令的引擎。

- 处理器中有一个字长度（word-size）的寄存器，
  称为程序计数器（program counter， PC）：
  在任何时间中，
  PC 都指向主存中的某个地址，
  这些地址保存了某些机器语言指令。

- 从系统通电开始，
  直到停电为止，
  处理器就一直执行以下动作：

  - 执行 PC 所指向地址里保存的指令

  - 更新 PC 的地址

- 处理器要执行的指令非常简单，
  这个指令集由指令集架构（instruction set architecture）定义，
  这些操作通常都与主存、寄存器文件或是 ALU 有关。

- 处理器还包含一些寄存器文件（register file）和 ALU （算术/逻辑单元）：

  - 寄存文件由一集保存字长度数据的寄存器组成。

  - ALU 用于计算新数据，和新地址。

- 以下是几个常用的指令：

  - 载入：从内存中复制一个字节或是一个字长的数据到寄存器，覆盖寄存器原来的值。

  - 保存：将寄存器中的一个字节或是一个字长的数据复制到内存的某个位置，覆盖该位置原有的值。

  - 计算：取出两个寄存器的值，复制它们到 ALU ，然后 ALU 对这两个值进行计算，并将结果保存在某个寄存器中，覆盖该寄存器原来的值。

  - 跳转：从指令中取出一个字，并将该字放到 PC 上，覆盖 PC 原来的值。
