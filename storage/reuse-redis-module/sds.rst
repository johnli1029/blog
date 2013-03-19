.. highlight:: c

Sds 模块
=============


适用范围
-----------------

``sds`` 模块构建了一个字符串对象抽象，
这个抽象字符串具有以下特性：

1. 内容可以是二进制安全的

2. 可以在 :math:`O(1)` 复杂度内取出字符串的长度

3. 通过预分配内存来减少连续追加（append）操作所需的内存重分配次数

如果你的程序需要以上这些特性，
那么可以考虑重用 Redis 的这个 ``sds`` 模块。

.. seealso:: 如果不熟悉 ``sds`` 模块的话，可以参考 http://www.redisbook.com 中和 sds 有关的章节。


准备步骤
-----------------

1. 从 Redis 源代码中复制 ``sds.h`` 、 ``sds.c`` 、 ``zmalloc.h`` 和 ``zmalloc.c`` 四个文件到新建文件夹。

2. 添加 ``#include <stddef.h>`` 到 ``zamlloc.h`` ，解决 ``size_t`` 未定义的问题。

3. 从 ``zamlloc.c`` 中移除 ``#include "config.h"`` ，因为现在已经不需要配置文件了。


测试驱动程序
-----------------

以下驱动程序展示了如何使用 ``sds`` 模块，
并测试了其中的 ``sdsnew`` 、 ``sdslen`` 、 ``sdsavail`` 、 ``sdsdup`` 和 ``sdscat`` 等函数。

.. literalinclude:: code/sds/main.c


完整源码
-----------------

重用程序的完整代码可以在 https://github.com/huangz1990/blog/tree/master/storage/reuse-redis-module/code 的 ``sds`` 文件夹中找到。
