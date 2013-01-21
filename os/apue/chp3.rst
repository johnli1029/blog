.. highlight:: c

第 3 章：文件 I/O
========================

本章先讨论 ``open`` 、 ``read`` 、 ``write`` 、 ``lseek`` 和 ``close`` 五个函数，
再介绍 ``dup`` 、 ``fcntl`` 、 ``sync`` 、 ``fsync`` 和 ``ioctl`` 函数。

其中，
``write`` 和 ``read`` 被称为不带缓冲的 I/O （unbuffered I/O），
因为每次执行这两个函数，都需要调用内核中的一个系统调用。


文件描述符
------------

对于内核而言，所有打开的文件都通过文件描述符引用。

文件描述符是一个非符整数。
当打开一个现有文件或者创建一个新文件时，内核向进程返回一个文件描述符。
当读或写一个文件时，使用 ``open`` 或 ``creat`` 返回的文件描述符标识该文件，并将其作为参数传送给 ``read`` 或者 ``write`` 函数。

按照惯例，UNIX 系统 SHELL 将描述符 ``0`` 、 ``1`` 、 ``2`` 分别和标准输入、标准输出和标准错误输出相关联。
在遵循 POSIX 规范的程序中，它们分别被定义于 ``unistd.h`` 中的常量 ``STDIN_FILENO`` 、 ``STDOUT_FILENO`` 和 ``STDERR_FILENO`` 所代替。


打开文件
-----------

函数 ``open`` 用于打开或创建一个文件：

::

    #include <sys/types.h>
    #include <sys/stat.h>
    #include <fcntl.h>

    int open(const char *pathname, int flags);
    int open(const char *pathname, int flags, mode_t mode);

``flags`` 参数的值可以是多个 ``fcntl.h`` 所定义的常量的二进制或。

以下三个参数的其中一个是必须的：

===============  ====================================
常量                作用
===============  ====================================
``O_RDONLY``        只读打开
``O_WRONLY``        只写打开
``O_RDWR``          读、写打开
===============  ====================================

以下这些参数则是可选的：

===============   ========================================================================================================
常量                作用
===============   ========================================================================================================
``O_APPEND``        每次写时都将内容追加到文件的尾端。

``O_CREAT``         如果指定文件不存在，那么创建并打开它。当使用这个参数时，需要指定 ``mode`` 参数的值（见下文）。

``O_EXCL``          在和 ``O_CREAT`` 一起使用时，确保文件是由本次调用所新创建的，如果文件已存在， ``open`` 执行失败。

``O_TRUNC``         如果打开目标是一个文件，并且允许进行写入，那么清除文件内原有的所有内容。

``O_SYNC``          当对文件进行写入时，阻塞直到写入内容已经被物理地保存到硬件为止。
===============   ========================================================================================================

更多可选参数请参考 ``open`` 命令的文档。

当 ``open`` 用于创建新文件时，文件的权限由 ``mode & ~umask`` 计算得出， ``mode`` 参数的值可以是以下多个常量的二进制或（定义于 ``sys/stat.h`` ）：

==========    =============================================================================
常量            意义
==========    =============================================================================
S_IRWXU         00700 user (file owner) has  read,  write  and  execute permission

S_IRUSR         00400 user has read permission

S_IWUSR         00200 user has write permission

S_IXUSR         00100 user has execute permission

S_IRWXG         00070 group has read, write and execute permission

S_IRGRP         00040 group has read permission

S_IWGRP         00020 group has write permission

S_IXGRP         00010 group has execute permission

S_IRWXO         00007 others have read, write and execute permission

S_IROTH         00004 others have read permission

S_IWOTH         00002 others have write permission

S_IXOTH         00001 others have execute permission
==========    =============================================================================


open 函数的 O_CREAT 和 O_EXCL 参数
---------------------------------------

设置了 ``O_CREAT`` 和 ``O_EXCL`` 参数的 ``open`` 函数都可以在文件不存在时创建并打开新文件，它们之间的区别在于：
如果文件已经存在， ``O_CREAT`` 直接打开（而不创建）文件， 而 ``O_CREAT | O_EXCL`` 则会报告错误。

以下是一个使用 ``O_CREAT`` 参数的 ``open`` 函数：

.. literalinclude:: code/3-open-create-file.c

当这个程序第一次调用时，它会创建并打开 ``test-3-open-create-file.txt`` 文件，
当程序第二次执行时，它只打开已存在的文件：

::

    $ ./3-open-create-file.out 

    $ ls -l test-3-open-create-file.txt 
    -rw-r--r-- 1 huangz huangz 0  1月 21 11:41 test-3-open-create-file.txt

    $ ./3-open-create-file.out 

    $ ls -l test-3-open-create-file.txt 
    -rw-r--r-- 1 huangz huangz 0  1月 21 11:41 test-3-open-create-file.txt

以下是一个使用 ``O_CREAT | O_EXCL`` 参数的 ``open`` 函数：

.. literalinclude:: code/3-open-create-with-excl.c

当这个程序第一次调用时，它会创建并打开 ``test-3-open-create-with-excl.txt`` 文件，
当第二次调用时， ``open`` 会返回一个错误，显示文件已存在：

::

    $ ./3-open-create-with-excl.out 

    $ ls -l test-3-open-create-with-excl.txt 
    -rw-r--r-- 1 huangz huangz 0  1月 21 12:10 test-3-open-create-with-excl.txt

    $ ./3-open-create-with-excl.out 
    open fail cause file already exists.


open 的返回值
------------------

当 ``open`` 成功打开文件时，
它的返回值总是当前最小的未使用描述符值。

比如说，如果标准输入、输出和出错占用了 ``0`` 、 ``1`` 和 ``2`` 三个描述符，
那么进程第一个打开的文件的描述符必定是 ``3`` 。

以下程序打印进程首个文件描述符的值：

.. literalinclude:: code/3-print-file-descriptor.c

执行结果：

::

    $ ./3-print-file-descriptor.out 
    fd = 3


用 creat 函数创建文件
--------------------------

``creat`` 函数提供了一种创建新的空白文件的快捷方式，
它等效于调用 ``open(pathname, O_WRONLY | O_CREAT | O_TRUNC, mode)`` ：

::

    #include <sys/types.h>
    #include <sys/stat.h>
    #include <fcntl.h>

    int creat(const char *pathname, mode_t mode);

以下代码展示了 ``creat`` 的用法，它创建一个空白的 ``test-3-creat`` 文件：

.. literalinclude:: code/3-creat.c

执行结果：

::

    $ ./3-creat.out 
    creat file OK

    $ ls -l test-3-creat 
    -rw-r--r-- 1 huangz huangz 0  1月 21 15:29 test-3-creat

``creat`` 的一个缺点是，它以只写方式打开所创建的问题，
如果需要既创建文件，又读写文件，最好还是用 ``open`` 函数。

以下代码的执行效果类似于 ``creat`` ，但是打开的文件可以同时用于读和写： 
``open(pathname, O_RDWR | O_CREAT | O_TRUNC, mode);`` 。


关闭文件
-----------

调用 ``close`` 可以显式地关闭一个文件描述符：

::

    #include <unistd.h>

    int close(int fd);

当一个文件描述符被关闭时，和它相关联的所有记录锁都会被移除。

如果 ``fd`` 是指向一个底层打开文件描述（underlying open file description）的最后一个文件描述符，
那么和文件描述相关的资源会被释放。

如果一个文件被 ``unlink(2)`` 函数移除过，
并且 ``fd`` 是指向这个文件的最后一个引用，
那么这个文件会被删除。

和 ``write(2)`` 函数类似，
当一个文件描述符被关闭时，系统并不保证缓存中的文件内容会被保存到物理硬件中，
如果要保证这一点，请使用 ``fsnyc(2)`` 函数。

忘记检查 ``close`` 的返回值是一种常见的编程错误。

当一个进程终止时，内核会自动关闭进程打开的所有文件，很多程序都利用了这一功能而不显式地调用 ``close`` 。

以下示例代码打开并关闭一个文件：

.. literalinclude:: code/3-close.c

执行结果：

::

    $ ./3-close.out 
    creat file OK
    close file OK


文件写入
------------

要向一个打开的文件描述符写入内容，可以使用 ``write`` 函数：

::

    #include <unistd.h>

    ssize_t write(int fd, const void *buf, size_t count);

``write`` 将 ``buf`` 中的内容写入 ``count`` 字节到 ``fd`` 所指向的文件。

``ssize_t`` 类型的返回值说明成功写入了多少字节，这个值可能出现三种情况：

1) 返回值和 ``count`` 相等，写入成功。

2) 返回值小于 ``count`` ，写入部分成功，但还有一部分内容未写入：当写入中途程序发现底层空间不足，或者写入被信号打断时，就会出现这种情况。

3) 返回值等于 ``-1`` ，写入出错，没有任何内容被写入：当 ``fd`` 不合法或者 ``buf`` 不合法时，就会出现这种情况。具体的错误保存在 ``errno`` 变量中。

对于普通文件，写操作从当前偏移量开始，
如果文件是以 ``O_APPEND`` 模式打开，那么在每次写入之前，都会原子性执行以下两个步骤：

1. 将文件的偏移量设置为文件的末尾

2. 执行写操作

在一次成功写之后，成功写入的字节数量就是文件大小增加的字节数量。

.. note:: ``write`` 执行成功并不保证数据已经被保存到磁盘，如果要保证这一点，需要执行 ``fsync`` 。

以下代码展示了 ``write`` 的用法，它创建/打开一个文件，将一个字符串写入到文件，最后关闭文件：

.. literalinclude:: code/3-write.c

执行结果：

::

    $ ./3-write.out 

    $ cat test-3-write 
    hello moto


读文件
----------

``read`` 函数用于读取文件的内容：

::

    #include <unistd.h>

    ssize_t read(int fd, void *buf, size_t count);

``read`` 从 ``fd`` 指向的文件中读取 ``count`` 字节，并将内容保存到 ``buf`` 中。 
如果 ``count`` 大于 ``SSIZE_MAX`` ，那么结果将是未定义的。

``read`` 的返回值可能是以下三种情况：

1) 返回值等于 ``count`` ：读取成功。

2) 返回值小于 ``count`` ：读取部分成功，可能读取已经到遇到文件的末尾（EOF），或者读取被信号中断 —— 前一种情况可以通过再次调用 ``read`` ，然后检查返回值是否为 ``0`` 来判断；而后一种情况则可以通过检查 ``errno`` 是否为 ``EINTR`` 来判断。

3) 返回值为 ``-1`` ：读取出错，错误值保存在 ``errno`` 。

读取操作从文件的当前偏移量开始，在成功返回之后，文件的偏移量会加上实际读到的字节数。

以下代码打开一个新的空白文件，往里写入一段文字，然后重新打开并读取和打印文件的内容：

.. literalinclude:: code/3-read.c

执行结果：

::

    $ ./3-read.out 
    file content: hello moto


文件偏移量
----------------

每个打开的文件都有一个与之相关联的“当前文件偏移量”（current file offset）。
它通常是一个非负整数，用以度量从文件开始处计算的字节数。

当读、写操作进行时，它们从当前文件偏移量开始，并使偏移量增加所读/写的字节数。

当打开一个文件时，除非指定 ``O_APPEND`` 选项，否则偏移量被初始化为 ``0`` ，也就是文件第一个字节所在的位置。


设置文件偏移量
-----------------

除了根据读写操作进行移动外，偏移量还可以通过 ``lseek`` 函数显示地设定：

::

    #include <sys/types.h>
    #include <unistd.h>

    off_t lseek(int fd, off_t offset, int whence);

参数 ``offset`` 的解释与参数 ``whence`` 的值有关：

- 若 ``whence`` 是 ``SEEK_SET`` ，则将该文件的偏移量设置为距文件开始处 ``offset`` 个字节。也即是，以文件头为开始，设置绝对偏移量。

- 若 ``whence`` 是 ``SEEK_CUR`` ，则将该文件的偏移量加上 ``offset`` 的值， ``offset`` 可以是正数或负数。也即是，以当前偏移量为开始，设置相对偏移量。

- 若 ``whence`` 是 ``SEEK_END`` ，则将该文件的偏移量设置为文件的长度加上 ``offset`` 的值， ``offset`` 可以是正数或负数。也即是，以文件末尾为开始，设置绝对偏移量。

``lseek`` 成功执行时返回新的文件偏移量，设置失败则返回 ``-1`` ，并将错误信息保存到 ``errno`` 。

在前面演示 ``read`` 函数的时候，程序使用了先关闭、再打开文件的办法来将文件的偏移量重置为 ``0`` ，有了 ``lseek`` 函数，这个重新打开的步骤就没有必要了：

.. literalinclude:: code/3-lseek.c

执行结果：

::

    $ ./3-lseek.out 
    file conent: hello moto
