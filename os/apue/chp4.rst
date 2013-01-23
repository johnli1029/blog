.. highlight:: c

第 4 章：文件和目录
=========================


获取文件信息
---------------

使用以下函数可以获取一个指定文件的相关信息：

::

    #include <sys/types.h>
    #include <sys/stat.h>
    #include <unistd.h>

    int stat(const char *path, struct stat *buf);
    int fstat(int fd, struct stat *buf);
    int lstat(const char *path, struct stat *buf);

``stat`` 取出 ``path`` 文件的相关信息，并将它保存到 ``buf`` 中。

``lstat`` 和 ``stat`` 类似，唯一的不同是，如果 ``path`` 是一个符号链接（symbolic link），
那么 ``lstat`` 返回的是链接文件的信息，而不是链接所指向的文件的信息。

``fstat`` 和 ``stat`` 类似，唯一的不同是， ``fstat`` 接受的参数是文件描述符 ``fd`` ，而不是文件的路径。

以上三个函数在执行成功时，返回 ``0`` ，失败时，返回 ``-1`` ，并将错误原因设置到 ``errno`` 。


获取文件信息所需的权限
--------------------------

除了使用 ``stat`` 和 ``lstat`` 对文件进行查看时，需要对路径上的所有文件夹有执行（查找）权限之外，
调用这些函数无须任何其他权限。

举个例子，要成功调用 ``stat("/foo/bar/spam", buf);`` ，必须对 ``foo`` 和 ``bar`` 文件夹都拥有执行权限。


文件信息
---------------

``stat`` 等三个函数将文件的信息保存到一个 ``struct stat`` 类型的结构中，这个结构包含以下域：

::

    struct stat {
        dev_t     st_dev;     // 包含文件的设备的 ID
        ino_t     st_ino;     // i-node 号码 
        mode_t    st_mode;    // 文件的访问权限、以及文件的类型
        nlink_t   st_nlink;   // 硬链接（hard links）的数量
        uid_t     st_uid;     // 拥有者的用户 ID
        gid_t     st_gid;     // 拥有者的组 ID
        dev_t     st_rdev;    // 设备 ID （只在文件是特殊文件时使用）
        off_t     st_size;    // 文件的大小（以字节计算）
        blksize_t st_blksize; // 推荐 I/O 操作对文件使用的块大小
        blkcnt_t  st_blocks;  // 文件占用的块数量（每块 512 字节）
        time_t    st_atime;   // 文件数据最后访问时间（例如 read）
        time_t    st_mtime;   // 文件数据最后修改时间（例如 write）
        time_t    st_ctime;   // 文件的 i 节点最后一次被修改的时间（例如 chmod）
    };

以下分多个小节介绍各个域的相关信息。


文件类型
--------------

``stat.st_mode`` 属性包含了文件的访问权限，以及文件的类型。

文件的类型可以是：

1) **普通文件**\ （regular file）：包含了某种形式的数据。这种数据是文本还是二进制数据对于内核而言并无区别，因为对普通文件内容的解释是由处理该文件的应用程序执行的。

2) **目录文件**\ （directory file）：包含了目录中所有文件的名字，以及指向文件相关信息的指针。

3) **块特殊文件**\ （block special file）：对设备（比如磁盘）提供带缓冲的访问，每次访问以固定长度为单位进行。

4) **字符特殊文件**\ （character special file）：对设备提供不带缓冲的访问，每次访问长度可变。系统中的设备要么是字符串特殊文件，要么是块特殊文件。

5) **先进先出队列**\ （FIFO）：用于进程间通信，有时也将其称为命名管道（named pipe）。

6) **套接字**\ （socket）：用于进程间的网络通信，也可以在同一台主机的进程上进行非网络通信。

7) **符号链接**\ （symbolic link）：指向另一个文件。

``sys/stat.h`` 文件提供了一组宏，通过它们对 ``stat.st_mode`` 的值进行判断，可以获得文件的类型：

===================   =======================
宏                      进行的检查
===================   =======================
``S_ISREG(m)``          普通文件？
``S_ISDIR(m)``          目录？
``S_ISBLK(m)``          块设备？
``S_ISCHR(m)``          字符串设备？
``S_ISFIFO(m)``         FIFO 设备？
``S_ISSOCK(m)``         套接字？
``S_ISLNK(m)``          符号链接？
===================   =======================

以下程序读入一个文件路径，并打印该文件的类型：

.. literalinclude:: code/4-print-type.c

执行结果：

::

    $ ./4-print-type.out /dev/null 
    character device

    $ ./4-print-type.out /dev/sda
    block device

    $ ./4-print-type.out /
    directory

    $ ./4-print-type.out 4-print-type.c       // 纯文本
    regular

    $ ./4-print-type.out 4-print-type.out     // 二进制
    regular

除了使用 ``S_ISXXX`` 宏之外，还可以用 ``st_mode`` 属性和 ``S_IFMT`` 屏蔽位做二进制求并计算，
然后通过计算结果判断文件的类型。

以下是使用这一判断方式的程序：

.. literalinclude:: code/4-print-type-2.c

执行结果：

::

    $ ./4-print-type-2.out /dev/sda
    block device

    $ ./4-print-type-2.out /dev/null 
    character device

    $ ./4-print-type-2.out /
    directory

    $ ./4-print-type-2.out 4-print-type-2.out 
    regular

    $ ./4-print-type-2.out 4-print-type-2.c
    regular

