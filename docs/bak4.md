## UDS

UDS：LTBUS_ETH_CreatUnixSocket()：socket(AF_UNIX, SOCK_STREAM) + unlink() + bind() + listen()（用于 fd-pass）

这里的 **UDS** 指的是 **Unix Domain Socket（Unix 域套接字）**，不是汽车诊断那个 **UDS（Unified Diagnostic Services）**。

在你这套代码里，`LTBUS_ETH_CreatUnixSocket()` 做的事情是：**在本机上创建一个 Unix 域“服务端监听口”**（路径一般是类似 `/tmp/uds_passfd.sock`），专门用来 **fd-pass（file descriptor passing，文件描述符传递）**。

### 这串调用分别干嘛

* `socket(AF_UNIX, SOCK_STREAM, 0)`

  * 创建一个 **本机 IPC** 的连接型 socket（stream-oriented，类似 TCP 语义，但不走网卡、不走 IP）。

* `unlink(UNIX_PATH)`

  * Unix 域 socket 用 **文件路径** 作为“地址”。进程异常退出时，这个路径文件可能残留。
  * `unlink()` 先删掉旧文件，避免 `bind()` 报 **EADDRINUSE**。

* `bind(fd, {sun_family=AF_UNIX, sun_path=...})`

  * 把这个 socket 绑定到某个路径（会在文件系统里生成一个 socket 文件节点）。

* `listen(fd, backlog)`

  * 进入监听状态，允许别的进程 `connect()` 进来，然后你再 `accept()`。

### “用于 fd-pass”是什么意思

只有 **AF_UNIX** 支持用 `sendmsg()/recvmsg()` 携带 **SCM_RIGHTS** 控制消息，把一个已经打开的 **fd** 传给另一个进程。

你的整体意图一般是这样的：

1. `ltbus_eth_server` 进程：对外 `accept()` 到 TCP 客户端连接，拿到 `tcp_client_fd`
2. 同时起一个 UDS 监听（就是这个 `LTBUS_ETH_CreatUnixSocket()`）
3. 其他进程（或库函数 `OpenDevice`）用 UDS `connect()` 上来
4. server 用 `sendmsg(..., SCM_RIGHTS)` 把 `tcp_client_fd` 传过去
5. 接收方 `recvmsg()` 拿到这个 fd，以后就能直接 `send()/recv()` 操作那条 TCP 连接

### 使用时的关键注意点

* **这是“同一台机器内”进程间传 fd**：跨机器不行。
* fd 传过去后，两个进程共享同一个 socket 对象（kernel state）：一边 `close()` 可能会影响另一边（引用计数语义）。
* UDS 路径文件的 **权限/所有权** 会影响谁能连上来（常见要考虑 `umask` / `chmod` / 放到 `/run` 等）。

如果你愿意，我也可以直接按你这份代码把 **fd-pass 的完整时序**（server `accept`/`sendmsg` ↔ client `connect`/`recvmsg`）画成一张 sequence diagram，方便写进设计文档里。
