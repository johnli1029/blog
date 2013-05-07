Chp1. A Tour of Computer Systems
====================================

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

