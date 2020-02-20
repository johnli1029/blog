在 Manjaro Linux 系统使用 Docker
======================================

.. image:: image/docker_logo.png


安装并启动
-------------------

安装 Docker ：

::

    $ sudo pacman -S docker
    正在解析依赖关系...
    正在查找软件包冲突...

    软件包 (1) docker-1:19.03.5-1

    全部安装大小：  181.99 MiB

    :: 进行安装吗？ [Y/n] Y
    (1/1) 正在检查密钥环里的密钥                                       [####################################] 100%
    (1/1) 正在检查软件包完整性                                         [####################################] 100%
    (1/1) 正在加载软件包文件                                           [####################################] 100%
    (1/1) 正在检查文件冲突                                             [####################################] 100%
    (1/1) 正在检查可用存储空间                                         [####################################] 100%
    :: 正在处理软件包的变化...
    (1/1) 正在安装 docker                                              [####################################] 100%
    docker 的可选依赖
        btrfs-progs: btrfs backend support [已安装]
        pigz: parallel gzip compressor support
    :: 正在运行事务后钩子函数...
    (1/4) Creating system user accounts...
    (2/4) Reloading system manager configuration...
    (3/4) Reloading device manager configuration...
    (4/4) Arming ConditionNeedsUpdate...

启动 Docker 服务：

::

    $ sudo systemctl start docker.service

如果有需要的话还可以把 Docker 添加到启动项，
让 Docker 在每次系统启动时自动运行：

::

    $ sudo systemctl enable docker.service
    Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.


将用户添加到 Docker 组中
-----------------------------------

Docker 默认只能通过 root 权限执行操作，
但通过将用户添加到 ``docker`` 用户组可以规避这一点：

::

    sudo usermod -aG docker huangz

注销然后重新登录之后就可以直接执行 Docker 命令了。


使用国内镜像
--------------------

Docker 默认使用的是外国源，
访问速度很慢而且很容易断线，
为此我们可以使用国内的镜像来代替默认的源。

打开或创建 ``/etc/docker/daemon.json`` 文件，
将选中的镜像地址添加到 ``registry-mirrors`` 数组里面（可同时填入多个镜像）：

::

    {
        "registry-mirrors": [
            "https://registry.docker-cn.com"
        ]
    }

这里的 ``registry.docker-cn.com`` 是 Docker 的官方中国镜像，
除此之外还有其他一些第三方镜像可选：

==============  ===========================================================
镜像            地址
==============  ===========================================================
Azure 中国      ``https://dockerhub.azk8s.cn``
中科大          ``https://docker.mirrors.ustc.edu.cn``
七牛云          ``https://reg-mirror.qiniu.com``
网易云          ``https://hub-mirror.c.163.com``
腾讯云          ``https://mirror.ccs.tencentyun.com``
==============  ===========================================================

保存文件之后重启一下 Docker 服务：

::

    sudo systemctl daemon-reload
    sudo systemctl restart docker

之后再次拉取应该就能够享受到镜像的加速效果了。


搜索和拉取映像（image）
--------------------------

查找“redis”相关的映像：

::

    $ docker search redis
    NAME                             DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
    redis                            Redis is an open source key-value store that…   7827                [OK]
    bitnami/redis                    Bitnami Redis Docker Image                      136                                     [OK]
    sameersbn/redis                                                                  79                                      [OK]
    grokzen/redis-cluster            Redis cluster 3.0, 3.2, 4.0 & 5.0               63
    rediscommander/redis-commander   Alpine image for redis-commander - Redis man…   34                                      [OK]
    kubeguide/redis-master           redis-master with "Hello World!"                31
    redislabs/redis                  Clustered in-memory database engine compatib…   24
    redislabs/redisearch             Redis With the RedisSearch module pre-loaded…   20
    arm32v7/redis                    Redis is an open source key-value store that…   20
    oliver006/redis_exporter          Prometheus Exporter for Redis Metrics. Supp…   18
    webhippie/redis                  Docker images for Redis                         10                                      [OK]
    insready/redis-stat              Docker image for the real-time Redis monitor…   9                                       [OK]
    s7anley/redis-sentinel-docker    Redis Sentinel                                  9                                       [OK]
    bitnami/redis-sentinel           Bitnami Docker Image for Redis Sentinel         9                                       [OK]
    redislabs/redisgraph             A graph database module for Redis               9                                       [OK]
    arm64v8/redis                    Redis is an open source key-value store that…   8
    redislabs/redismod               An automated build of redismod - latest Redi…   6                                       [OK]
    centos/redis-32-centos7          Redis in-memory data structure store, used a…   4
    circleci/redis                   CircleCI images for Redis                       3                                       [OK]
    frodenas/redis                   A Docker Image for Redis                        2                                       [OK]
    runnable/redis-stunnel           stunnel to redis provided by linking contain…   1                                       [OK]
    wodby/redis                      Redis container image with orchestration        1                                       [OK]
    tiredofit/redis                  Redis Server w/ Zabbix monitoring and S6 Ove…   1                                       [OK]
    xetamus/redis-resource           forked redis-resource                           0                                       [OK]
    cflondonservices/redis           Docker image for running redis                  0

拉取 ``redis`` 映像（默认标签为 ``latest``\ ）：

::

    $ docker pull redis
    Using default tag: latest
    latest: Pulling from library/redis
    bc51dd8edc1b: Already exists 
    37d80eb324ee: Already exists 
    392b7748dfaf: Already exists 
    48df82c3534d: Pull complete 
    2ec2bb0b4b0e: Pull complete 
    1302bce0b2cb: Pull complete 
    Digest: sha256:7b84b346c01e5a8d204a5bb30d4521bcc3a8535bbf90c660b8595fad248eae82
    Status: Downloaded newer image for redis:latest
    docker.io/library/redis:latest

拉取标签（版本）为 ``rc`` 的 ``redis`` 映像：

::

    $ docker pull redis:rc
    rc: Pulling from library/redis
    bc51dd8edc1b: Already exists 
    37d80eb324ee: Already exists 
    392b7748dfaf: Already exists 
    a1b0f06a879d: Already exists 
    ddf53851e8fb: Already exists 
    cacb31381ac1: Already exists 
    Digest: sha256:0d9535132a352fabbf7cce287286e80cf1ecebc7b18a949bd547ba24413142df
    Status: Downloaded newer image for redis:rc
    docker.io/library/redis:rc

查看已有映像：

::

    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    redis               latest              44d36d2c2374        2 weeks ago         98.2MB
    redis               rc                  9220658d0dd7        2 weeks ago         104MB
    ubuntu              latest              ccc6e87d482b        5 weeks ago         64.2MB


运行映像创建容器
---------------------------

根据映像创建容器（实例）：

::

    $ docker run --name myredis -d redis
    f6b2ed42676c8f8e6499fc14a41ce188701d47f1bd2fac4db735455f24264096

每个容器的使用方法都不完全一样，
在使用前需要查看文档。

查看正在运行的容器的状态：

::

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
    f6b2ed42676c        redis               "docker-entrypoint.s…"   9 seconds ago       Up 7 seconds        6379/tcp            myredis

停止并移除容器：

::

    $ docker stop myredis
    $ docker rm myredis


查看相关信息
---------------------------

::

    $ docker info
    Client:
     Debug Mode: false

    Server:
     Containers: 1
      Running: 0
      Paused: 0
      Stopped: 1
     Images: 2
     Server Version: 19.03.5-ce
     Storage Driver: overlay2
      Backing Filesystem: extfs
      Supports d_type: true
      Native Overlay Diff: false
     Logging Driver: json-file
     Cgroup Driver: cgroupfs
     Plugins:
      Volume: local
      Network: bridge host ipvlan macvlan null overlay
      Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
     Swarm: inactive
     Runtimes: runc
     Default Runtime: runc
     Init Binary: docker-init
     containerd version: d50db0a42053864a270f648048f9a8b4f24eced3.m
     runc version: dc9208a3303feef5b3839f4323d9beb36df0a9dd
     init version: fec3683
     Security Options:
      apparmor
      seccomp
       Profile: default
     Kernel Version: 5.3.18-1-MANJARO
     Operating System: Manjaro Linux
     OSType: linux
     Architecture: x86_64
     CPUs: 16
     Total Memory: 31.38GiB
     Name: pc
     ID: 2BWN:6UK6:T2ON:UDHW:FKC6:4ESF:ZKU5:F2DS:CCAB:CK4Z:4IQN:PX2G
     Docker Root Dir: /var/lib/docker
     Debug Mode: false
     Registry: https://index.docker.io/v1/
     Labels:
     Experimental: false
     Insecure Registries:
      127.0.0.0/8
     Registry Mirrors:
      https://registry.docker-cn.com/
     Live Restore Enabled: false


参考资料
---------------------------

- https://linuxhint.com/docker_arch_linux/

- https://hub.docker.com/_/redis/

- https://docs.docker.com/
