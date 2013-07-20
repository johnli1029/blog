.. highlight:: c

复制（replication）
=====================

因为时间关系，这里先贴出代码注释，代码分析如果将来有时间再补上。

首先是服务器状态中，和复制功能有关的属性：

::

    struct redisServer {

        // 其他属性 ...

        /* Replication (master) */

        int slaveseldb;                 /* Last SELECTed DB in replication output */
        // 全局复制偏移量（一个累计值）
        long long master_repl_offset;   /* Global replication offset */
        // 主服务器发送 PING 的频率
        int repl_ping_slave_period;     /* Master pings the slave every N seconds */
        char *repl_backlog;             /* Replication backlog for partial syncs */
        // backlog 的长度
        long long repl_backlog_size;    /* Backlog circular buffer size */
        // backlog 中数据的长度
        long long repl_backlog_histlen; /* Backlog actual data length */
        // 数据的当前起始偏移量， 
        // repl_backlog[idx] 至 repl_backlog[idx+histlen] 
        // 就是 backlog 中当前保存的所有数据
        long long repl_backlog_idx;     /* Backlog circular buffer current offset */
        // backlog 中可以被还原的第一个字节的偏移量
        long long repl_backlog_off;     /* Replication offset of first byte in the
                                           backlog buffer. */
        time_t repl_backlog_time_limit; /* Time without slaves after the backlog
                                           gets released. */
        time_t repl_no_slaves_since;    /* We have no slaves since that time.
                                           Only valid if server.slaves len is 0. */
        // 是否开启最小数量从服务器写入功能
        int repl_min_slaves_to_write;   /* Min number of slaves to write. */
        // 定义最小数量从服务器的最大延迟值
        int repl_min_slaves_max_lag;    /* Max lag of <count> slaves to write. */
        // 延迟良好的从服务器的数量
        int repl_good_slaves_count;     /* Number of slaves with lag <= max_lag. */

        /* Replication (slave) */
        // 主服务器的验证密码
        char *masterauth;               /* AUTH with this password with master */
        // 主服务器的地址
        char *masterhost;               /* Hostname of master */
        // 主服务器的端口
        int masterport;                 /* Port of master */
        // 超时时间
        int repl_timeout;               /* Timeout after N seconds of master idle */
        // 主服务器所对应的客户端
        redisClient *master;     /* Client that is master for this slave */
        // 被缓存的主服务器，PSYNC 时使用
        redisClient *cached_master; /* Cached master to be reused for PSYNC. */
        int repl_syncio_timeout; /* Timeout for synchronous I/O calls */
        // 复制的状态
        int repl_state;          /* Replication status if the instance is a slave */
        // RDB 文件的大小
        off_t repl_transfer_size; /* Size of RDB to read from master during sync. */
        // 已读 RDB 文件内容的字节数
        off_t repl_transfer_read; /* Amount of RDB read from master during sync. */
        // 最近一次执行 fsync 时的偏移量
        // 用于 sync_file_range 函数
        off_t repl_transfer_last_fsync_off; /* Offset when we fsync-ed last time. */
        // 主服务器的套接字
        int repl_transfer_s;     /* Slave -> Master SYNC socket */
        // 保存 RDB 文件的临时文件的描述符
        int repl_transfer_fd;    /* Slave -> Master SYNC temp file descriptor */
        // 保存 RDB 文件的临时文件名字
        char *repl_transfer_tmpfile; /* Slave-> master SYNC temp file name */
        // 最近一次读入 RDB 内容的时间
        time_t repl_transfer_lastio; /* Unix time of the latest read, for timeout */
        int repl_serve_stale_data; /* Serve stale data when link is down? */
        // 是否只读从服务器？
        int repl_slave_ro;          /* Slave is read only? */
        time_t repl_down_since; /* Unix time at which link with master went down */
        int repl_disable_tcp_nodelay;   /* Disable TCP_NODELAY after SYNC? */
        int slave_priority;             /* Reported in INFO and used by Sentinel. */
        // 主服务器 RUN ID
        char repl_master_runid[REDIS_RUN_ID_SIZE+1];  /* Master run id for PSYNC. */
        // 初始化偏移量
        long long repl_master_initial_offset;         /* Master PSYNC offset. */
        /* Replication script cache. */
        // 复制脚本缓存
        // 字典
        dict *repl_scriptcache_dict;        /* SHA1 all slaves are aware of. */
        // FIFO 队列
        list *repl_scriptcache_fifo;        /* First in, first out LRU eviction. */
        int repl_scriptcache_size;          /* Max number of elements. */

        // 其他属性 ...
    };

以下是 ``replication.c`` 文件的完整代码：

.. literalinclude:: replication/replication.c
