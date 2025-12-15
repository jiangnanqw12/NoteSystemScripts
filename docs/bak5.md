下面这些点，改完能明显提升稳定性、可维护性和“跑 2×24h 不翻车”的概率（按优先级从高到低）。

## 1) 资源释放与错误路径：现在有多处 **fd/heap 泄漏**

* `LTBUS_ETH_GetTcpClientFd()` 里任意一步失败都会 `return`，但 **unixFd 没 close**（多条 early-return）。
* `LTBUS_ETH_OpenDevice()` 在拿 fd 失败时直接 `return NULL`，但 **devHandle 没 free**。
* `LTBUS_ETH_CloseDevice()` 只 `free(handle)`，但 **fd-pass 得到的 tcp fd 没 close**（这是最要命的泄漏）。

**建议改法（只贴修改片段）：**

```c
// LTBUS_ETH_GetTcpClientFd(): unify cleanup (error-path cleanup)
STATIC INT32 LTBUS_ETH_GetTcpClientFd(INT32 *clientFd)
{
    INT32 ret = HELF_EOK;
    INT32 unixFd = -1;
    ...
    unixFd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (unixFd < 0) {
        return LTBUS_ETH_GENERAL_ERRNO(HELF_ESOCKET);
    }

    // (Recommended) keep it blocking; or handle EINPROGRESS if non-blocking
    // Do NOT set O_NONBLOCK before connect unless you handle EINPROGRESS properly.
    if (connect(unixFd, (struct sockaddr *)&unixAddr, sizeof(unixAddr)) < 0) {
        ret = LTBUS_ETH_GENERAL_ERRNO(HELF_ECONNECT);
        goto OUT;
    }

    ...
    if (recvmsg(unixFd, &msg, 0) <= 0) {
        ret = LTBUS_ETH_GENERAL_ERRNO(HELF_ERECV);
        goto OUT;
    }

    cmsg = CMSG_FIRSTHDR(&msg);
    if (cmsg == NULL || cmsg->cmsg_type != SCM_RIGHTS) {
        ret = LTBUS_ETH_GENERAL_ERRNO(HELF_ENOMSG);
        goto OUT;
    }
    *clientFd = *(INT32 *)CMSG_DATA(cmsg);

OUT:
    if (unixFd >= 0) {
        close(unixFd);
    }
    return ret;
}

// LTBUS_ETH_OpenDevice(): free on failure
if (ret != HELF_EOK) {
    free(devHandle);             // (Fix) avoid heap leak
    return NULL;
}

// LTBUS_ETH_CloseDevice(): close passed fd
INT32 LTBUS_ETH_CloseDevice(VOID *handle)
{
    LTBUS_ETH_DevHandle *devHandle = (LTBUS_ETH_DevHandle *)handle;
    if (devHandle == NULL) {
        return LTBUS_ETH_GENERAL_ERRNO(HELF_ENULLPOINTER);
    }

    if (devHandle->handleInfo.clientFd >= 0) {
        close(devHandle->handleInfo.clientFd); // (Fix) close received fd
        devHandle->handleInfo.clientFd = -1;
    }
    free(devHandle);
    return HELF_EOK;
}
```

## 2) 字节序函数命名/语义不一致：`NTOHLL()` 实现其实在做 hton（很容易埋雷）

你现在的 `NTOHLL()` 用的是 `htonl()` 拼 64 位：
而且它被用于组帧：`ethFrame->data.timeStamp = NTOHLL(...)`。
这会导致后续真要填 timestamp 时“看起来能跑，但端序错”。

**建议：分成 HTONLL / NTOHLL 两个（只贴替换片段）：**

```c
static inline UINT64 HTONLL(UINT64 host)
{
    UINT32 high = htonl((UINT32)(host >> 32));
    UINT32 low  = htonl((UINT32)(host & 0xFFFFFFFFu));
    return ((UINT64)high << 32) | low;
}

static inline UINT64 NTOHLL(UINT64 net)
{
    UINT32 high = ntohl((UINT32)(net >> 32));
    UINT32 low  = ntohl((UINT32)(net & 0xFFFFFFFFu));
    return ((UINT64)high << 32) | low;
}
```

然后组帧用 `HTONLL()`，解帧用 `NTOHLL()`（byte order(字节序) 一眼就清楚）。

## 3) `send()` 必须处理“短写”(partial write)，否则会随机丢帧

你现在 `send(fd, &ethFrame, CAN_FRAME_LENGTH, 0)` 只判断 `ret <= 0`，没处理 `ret < CAN_FRAME_LENGTH`。

**建议：封装 send_all（algorithm: loop + retry）**

```c
static INT32 SendAll(INT32 fd, const UINT8 *buf, UINT32 len)
{
    UINT32 off = 0;
    while (off < len) {
        ssize_t n = send(fd, buf + off, len - off, 0);
        if (n > 0) {
            off += (UINT32)n;
            continue;
        }
        if (errno == EINTR) {
            continue;
        }
        return LTBUS_ETH_GENERAL_ERRNO(HELF_ESEND);
    }
    return HELF_EOK;
}

// in LTBUS_ETH_DeviceSend()
ret = SendAll(clientFd, (const UINT8 *)&ethFrame, CAN_FRAME_LENGTH);
if (ret != HELF_EOK) { ... }
```

## 4) 共享内存并发：当前是典型的“写一半被读走”(torn read) 风险

Server 写 `devInfo->canFrame` / `lastRecvTime` / `rxCnt` 没锁：
Client 读 `devInfo->canFrame.data` 也没锁：

**建议二选一：**

* 上锁：shared mutex(进程间互斥锁) / pthread_mutexattr(PTHREAD_PROCESS_SHARED)；
* 无锁：用 seqlock(序列锁，data structure) 或者 “version + double buffer”。

最小侵入的无锁版本一般是：`uint32_t seq;` 写端写前 `seq++`（变奇数），写完 `seq++`（变偶数）；读端读两次 seq，要求相等且为偶数，否则重试。

## 5) fd-pass 逻辑：Server 永远发 `client[0]`，多连接时会错绑

Unix socket 里固定传 `socketInfo->client[0]`：
如果 TCP client 不止一个，或者你想按 deviceName/canId/channelId 绑定，这里会把“错误的 TCP fd”发给业务进程。

**建议方向：**

* Unix 请求里带上 `deviceName` 或 `(canId, channelId)`，server 查表返回对应 tcp fd；或
* 每个 tcp client 建立独立的 “connection context(连接上下文)” 并映射到设备。

## 6) `accept()` 超连接时要 close，否则 fd 泄漏（Server 端）

当 `LTBUS_ETH_SOCKET_LISTEN_NUM` 满了直接 `return`，但 **没 close 新 accept 的 fd**：

```c
if (i == LTBUS_ETH_SOCKET_LISTEN_NUM) {
    close(clientFd); // (Fix) avoid fd leak
    return;
}
```

## 7) `DeviceRecv()` 的 timeout 语义/CPU：现在是“忙等”(busy-wait) + 逻辑容易误用

它用 `lastRecvTime` 和 `formatTimeout` 做判断，然后 `LTR_UsDelay(1)` 循环减计数：
这会：

* 在 15s 超时下跑 1500 万次循环（CPU/抖动风险）；
* “数据太老”等待更新的判据不够直观（更合理的是等 `lastRecvTime` **发生变化**）。

---

如果你愿意，我可以按你现在的约束（不大改结构）给你一版“最小修改补丁清单”，把：**fd 泄漏 + NTOHLL + send 短写 + accept 泄漏 + SHM 并发** 这 5 个点一次性收口。
