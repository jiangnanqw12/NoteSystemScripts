
| 指令类 | 指令                      | 返回值                                                                                                                 | 含义                                                      | 接口                                                                                                                               |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| PAR    | PAR:OPEN 1000,50          |                                                                                                                        | 设置以50V电压正向步进1000步                                | INT32 LTDRV_AcSetOpenLoopCtrlParameters(UINT32 acId, Float step, Float Voltage) 参数是用 UINT32/Float/Double 根据控制器实际取值确定 |
|        | PAR:OPEN 0,30             |                                                                                                                        | 设置输出30V直流电压                                       |                                                                                                                                    |
|        | PAR:CLOS 0,5,10,10        |                                                                                                                        | 设置闭环运动目标位置为0，速度为5，加速度为10，减速过程加速度为10 | INT32 LTDRV_AcSetCloseLoopCtrlParameters(UINT32 acId, Float target, Float Speed, Float Acceleration, Float Deceleration)          |
|        | PAR:JOG 1,0               |                                                                                                                        | 设置在当前位置的基础上正向运动1°                          | INT32 LTDRV_AcSetJogParameters(UINT32 acId, Float step, UINT8 baseMode, Float Speed, Float Acceleration, Float Deceleration)      |
|        | PAR:JOG 1,1               |                                                                                                                        | 设置在当前目标位置的基础上增加 1°，并运动到新的目标位置    |                                                                                                                                    |
|        | PAR:JOG 1,0,5,10,10       |                                                                                                                        | 设置在当前位置的基础上正向运动1°，速度为5，加速度为10，减速过程加速度为10 |                                                                                                                                    |
|        | PAR:JOG 1,1,5,10,10       |                                                                                                                        | 设置在当前目标位置的基础上增加 1°，并运动到新的目标位置，速度为5，加速度为10，减速过程加速度为10 |                                                                                                                                    |
|        | PAR:RANG -10,10           |                                                                                                                        | 设置运动范围为-10°~10°                                    | INT32 LTDRV_AcSetRangeParameters(UINT32 acId, Float minPos, Float maxPos)                                                         |
|        | PAR:FIN?                  | PAR:FIN 0.005,1,0.00005                                                                                                | 查询精调参数                                              | INT32 LTDRV_AcGetFinParameters(UINT32 acId, Float *stepThreshold, Float *settleTime, Float *tolerance)                            |
|        | PAR:PIDP?                 | PAR:PIDP 0.05,0.25,0,0                                                                                                 | 查询PID参数                                               | INT32 LTDRV_AcGetPidParameters(UINT32 acId, Float *kp, Float *ki, Float *kd, Float *deadZone)                                     |
|        | PAR:FIN 0.005,1,0.00005   |                                                                                                                        | 设置精调参数：步进值0.005°以内进入精调模式；判定1秒内是否波动到达0.00005°以内 | INT32 LTDRV_AcSetFinParameters(UINT32 acId, Float stepThreshold, Float settleTime, Float tolerance)                               |
|        | PAR:PIDP 0.05,0.25,0,0    |                                                                                                                        | 设置位置PID参数 比例为0.05，积分为0.25，微分为0，死区为0  | INT32 LTDRV_AcSetPidParameters(UINT32 acId, Float kp, Float ki, Float kd, Float deadZone)                                         |
|        | PAR:FFWD 0.00002,30000    |                                                                                                                        | 设置前馈参数：步进值在0.00002°以内进入前馈模式，前馈增益为30000 | INT32 LTDRV_AcSetFeedForwardParameters(UINT32 acId, Float stepThreshold, Float gain)                                              |
|        | PAR:REF 0,0,0             |                                                                                                                        | 设置归零点                                                |                                                                                                                                    |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| MOVE   | MOVE:OPEN 1000,50         |                                                                                                                        | 开环运动以50V电压正向步进1000步                           | INT32 LTDRV_AcOpenMove(UINT32 acId, Float step, Float Voltage) 参数是用 UINT32/Float/Double 根据控制器实际取值确定                |
|        | MOVE:OPEN 0,30            |                                                                                                                        | 开环运动输出30V直流电压                                   |                                                                                                                                    |
|        | MOVE:OPEN                 |                                                                                                                        | 开环运动（使用当前配置参数）                              |                                                                                                                                    |
|        | MOVE:CLOS 0,5,10,10       |                                                                                                                        | 闭环运动目标位置为0，速度为5，加速度为10，减速过程加速度为10 | INT32 LTDRV_AcCloseMove(UINT32 acId, Float target, Float Speed, Float Acceleration, Float Deceleration) 参数类型同上              |
|        | MOVE:JOG 1,0              |                                                                                                                        | 步进运动在当前位置的基础上正向运动1°                     | INT32 LTDRV_AcJogMove(UINT32 acId, Float step, UINT8 baseMode, Float Speed, Float Acceleration, Float Deceleration)              |
|        | MOVE:JOG 1,1              |                                                                                                                        | 步进运动在当前目标位置的基础上增加 1°，并运动到新的目标位置 |                                                                                                                                    |
|        | MOVE:REF                  |                                                                                                                        | 运动至参考点                                              |                                                                                                                                    |
|        | MOVE:STOP                 |                                                                                                                        | 停止运动                                                  |                                                                                                                                    |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| MODE   | MODE:FIN 0                |                                                                                                                        | 关闭精调                                                  | INT32 LTDRV_AcSetFinMode(UINT32 acId, UINT8 enable)                                                                               |
|        | MODE:FIN 1                |                                                                                                                        | 开启精调（默认开启）                                      |                                                                                                                                    |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| SENS   | SENS:SPE?                 | SENS:SPE 2.1                                                                                                           | 查询当前速度                                              | INT32 LTDRV_AcGetSpeed(UINT32 acId, Float *speed)                                                                                 |
|        | SENS:POS?                 | SENS:POS 1.234                                                                                                         | 查询当前位置                                              | INT32 LTDRV_AcGetPosition(UINT32 acId, Float *position)                                                                           |
|        | SENS:VOLT?                | SENS:VOLT 35.132                                                                                                       | 查询当前电压                                              | INT32 LTDRV_AcGetVoltage(UINT32 acId, Float *voltage)                                                                             |
|        | SENS:REF?                 | STAT:REF 0 未校准过参考点或者校准失败； STAT:REF 1 校准成功                                                             | 查询是否校准过参考点                                      |                                                                                                                                    |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| STAT   | STAT:MOVE?                | STAT:MOVE 0 未运动； STAT:MOVE 1 正在运动                                                                               | 查询当前运动状态                                          | INT32 LTDRV_AcGetMoveStat(UINT32 acId, UINT8 *moveStat)                                                                           |
|        | STAT:TARG?                | STAT:TARG 0 未到达目标位置； STAT:TARG 1 到达目标位置                                                                   | 查询当前到位状态                                          | INT32 LTDRV_AcGetTargetStat(UINT32 acId, UINT8 *targetStat)                                                                       |
|        | STAT:ERR?                 | STAT:ERR 0 无错误； STAT:ERR 1~255 有错误                                                                               | 查询错误信息                                              | INT32 LTDRV_AcGetErrorStat(UINT32 acId, UINT8 *errorCode)                                                                         |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| COMM   | COMM:TTLO 0             |                          | 关闭 TTL 串口输出功能， 默认开机即关闭  | INT32 LTDRV_AcSetTtlOutputMode(UINT32 acId, UINT8 mode)  // 0:关闭；1:输出位置；2:输出速度     |
|        | COMM:TTLO 1             |                          | TTL 串口输出当前位置                    |                                                                                                |
|        | COMM:TTLO 2             |                          | TTL 串口输出当前速度                    |                                                                                                |
|        | COMM:TTLF 921600        |                          | 设置 TTL 串口输出的波特率为921600       | INT32 LTDRV_AcSetTtlBaudrate(UINT32 acId, UINT32 baudrate)                                    |
|        | COMM:485B 921600        |                          | 设置 RS485 的波特率为921600             | INT32 LTDRV_AcSet485Baudrate(UINT32 acId, UINT32 baudrate)                                    |
|        | COMM:485B?              | COMM:485B 921600         | 查询 RS485 波特率                       | INT32 LTDRV_AcGet485Baudrate(UINT32 acId, UINT32 *baudrate)                                   |
|        | COMM:IPAD 192,168,1,1   |                          | 设置网口的 IP 地址为 192.168.1.1        | INT32 LTDRV_AcSetIpAddress(UINT32 acId, UINT8 ip0, UINT8 ip1, UINT8 ip2, UINT8 ip3)           |
|        | COMM:GAT X,X,X,X        |                          | 设置网口的网关                          | INT32 LTDRV_AcSetGateway(UINT32 acId, UINT8 gw0, UINT8 gw1, UINT8 gw2, UINT8 gw3)             |
|        | COMM:SUBD X,X,X,X       |                          | 设置网口的子网掩码                      | INT32 LTDRV_AcSetSubnetMask(UINT32 acId, UINT8 mask0, UINT8 mask1, UINT8 mask2, UINT8 mask3)  |
| HARD   | HARD:REST                 |                                                                                                                        | 控制器重启                                                | INT32 LTDRV_AcSetHardwareReset(UINT32 acId)                                                                                       |
|        | HARD:SHUT                 |                                                                                                                        | 控制器进入待机模式                                        |                                                                                                                                    |
|        | HARD:IDN?                 | ControllerPN  ControllerSN:  PositionerPN:  PositionerSN:  CPU1 Version:V1.0  CPU2 Version:V1.0                       | 查询控制器的硬件信息                                      | INT32 LTDRV_AcGetHardwareInfo(UINT32 acId, LTDRV_HardwareInfo *pInfo)                                                             |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| ;      | 指令合并                  | ;                                                                                                                      |                                                           |                                                                                                                                    |



| 接口                                      | 说明                                                                                                                                         | 示例                                                | 帧格式说明                                           |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| INT32 LTDRV_AcSetVoltage(UINT32 acId, Float voltage) | 功能码 0x01、0x02 保留；功能码 0x03 为电压设定，对应指令：0x03 0x00 0x03 0xE8 0x93 - 1V；0x03 0x00 0x00 0x00 0x3A - 0V（内部按比例换算为 3 字节数值） | 例如：00 03 E8 为 0x0003E8(16进制) = 1000，对应 1V | 指令 5 帧：功能码 + 3 字节数据位 + 校验码；校验 CRC8 多项式：x8+x2+x+1 |



我先直接把所有有 `xxx` 的接口都补完整，你再按控制器实际情况把 `float/double/UINT8` 这些细节微调就行。

---

## 1. 参数配置类接口（PAR）

### 1.1 JOG 参数

SCPI 语义：

* `PAR:JOG 1,0` → 在**当前位置**基础上正向 1°
* `PAR:JOG 1,1` → 在**当前目标位置**基础上增加 1°
* `PAR:JOG 1,0,5,10,10` / `PAR:JOG 1,1,5,10,10` → 多了 速度/加减速度

建议统一一个接口，包含全部参数：

```c
INT32 LTDRV_AcSetJogParameters(
    UINT32 acId,
    float  step,        // JOG 步进量，单位：deg
    UINT8  baseMode,    // 0: 基于当前位置；1: 基于目标位置
    float  speed,       // 速度
    float  accel,       // 加速度
    float  decel        // 减速度（减速过程的加速度）
);
```

* 当 SCPI 只给两个参数（`step, baseMode`）时，可以在解析层给 `speed/accel/decel` 传默认值。

---

### 1.2 运动范围参数

SCPI：`PAR:RANG -10,10` → 运动范围 -10° ~ 10°

```c
INT32 LTDRV_AcSetRangeParameters(
    UINT32 acId,
    float  minPos,    // 最小位置
    float  maxPos     // 最大位置
);
```

---

### 1.3 精调参数 FIN

SCPI：

* 查询：`PAR:FIN?` → `PAR:FIN 0.005,1,0.00005`
* 设置：`PAR:FIN 0.005,1,0.00005`

语义：

* 步进值在 0.005° 以内进入精调模式
* 在 `1 秒` 内判断是否收敛到 `0.00005°` 以内

```c
INT32 LTDRV_AcSetFinParameters(
    UINT32 acId,
    float  stepThreshold,   // 步进阈值，进入精调模式的阈值
    float  settleTime,      // 判定时间窗口，单位：s
    float  tolerance        // 目标附近容差，单位：deg
);

INT32 LTDRV_AcGetFinParameters(
    UINT32 acId,
    float *stepThreshold,   // 输出：步进阈值
    float *settleTime,      // 输出：判定时间窗口
    float *tolerance        // 输出：容差
);
```

---

### 1.4 PID 参数

SCPI：

* 查询：`PAR:PIDP?` → `PAR:PIDP 0.05,0.25,0,0`
* 设置：`PAR:PIDP 0.05,0.25,0,0`

语义：P/I/D/死区

```c
INT32 LTDRV_AcSetPidParameters(
    UINT32 acId,
    float  kp,        // 比例
    float  ki,        // 积分
    float  kd,        // 微分
    float  deadZone   // 死区
);

INT32 LTDRV_AcGetPidParameters(
    UINT32 acId,
    float *kp,        // 输出：比例
    float *ki,        // 输出：积分
    float *kd,        // 输出：微分
    float *deadZone   // 输出：死区
);
```

---

## 2. 运动指令类接口（MOVE）

### 2.1 开环运动

SCPI：

* `MOVE:OPEN 1000,50` → 以 50V 正向步进 1000 步
* `MOVE:OPEN 0,30`    → 输出 30V 直流电压
* `MOVE:OPEN`         → 按当前 PAR:OPEN 已配置参数开环运动（可选）

建议接口跟 `PAR:OPEN` 一致：

```c
INT32 LTDRV_AcOpenMove(
    UINT32 acId,
    float  step,      // 步数（或步进量），0 表示只按电压输出
    float  voltage    // 输出电压，单位：V
);
```

（如果你希望 `MOVE:OPEN` 无参数时仅按已配置参数执行，可以在上层解析里调用一个不带 step/voltage 的重载或用保存的参数。）

---

### 2.2 闭环运动

SCPI：`MOVE:CLOS 0,5,10,10`
语义：目标位置 0，速度 5，加速度 10，减速度加速度 10

```c
INT32 LTDRV_AcCloseMove(
    UINT32 acId,
    float  target,    // 目标位置
    float  speed,     // 速度
    float  accel,     // 加速度
    float  decel      // 减速度
);
```

---

### 2.3 JOG 运动

SCPI 同 PAR:JOG，只是这里是“执行一次步进运动”：

* `MOVE:JOG 1,0`
* `MOVE:JOG 1,1`
* （如扩展）`MOVE:JOG 1,0,5,10,10` 等

```c
INT32 LTDRV_AcJogMove(
    UINT32 acId,
    float  step,        // 步进量
    UINT8  baseMode,    // 0: 基于当前位置；1: 基于目标位置
    float  speed,       // 速度
    float  accel,       // 加速度
    float  decel        // 减速度
);
```

---

## 3. 模式相关接口（MODE）

SCPI：

* `MODE:FIN 0` → 关闭精调
* `MODE:FIN 1` → 开启精调（默认开启）

```c
INT32 LTDRV_AcSetFinMode(
    UINT32 acId,
    UINT8  enable    // 0: 关闭；1: 开启
);
```

---

## 4. 传感/监控类接口（SENS / STAT）

### 4.1 当前速度 / 位置 / 电压

SCPI：

* `SENS:SPE?`  → `SENS:SPE 2.1`
* `SENS:POS?`  → `SENS:POS 1.234`
* `SENS:VOLT?` → `SENS:VOLT 35.132`

```c
INT32 LTDRV_AcGetSpeed(
    UINT32 acId,
    float *speed      // 输出：当前速度
);

INT32 LTDRV_AcGetPosition(
    UINT32 acId,
    float *position   // 输出：当前位置
);

INT32 LTDRV_AcGetVoltage(
    UINT32 acId,
    float *voltage    // 输出：当前电压
);
```

---

### 4.2 状态类：运动状态 / 到位状态 / 错误信息

SCPI：

* `STAT:MOVE?` → `STAT:MOVE 0 / 1`
* `STAT:TARG?` → `STAT:TARG 0 / 1`
* `STAT:ERR?`  → `STAT:ERR 0 / 1~255`

```c
INT32 LTDRV_AcGetMoveStat(
    UINT32 acId,
    UINT8 *moveStat   // 输出：0 未运动；1 正在运动
);

INT32 LTDRV_AcGetTargetStat(
    UINT32 acId,
    UINT8 *targetStat // 输出：0 未到位；1 到达目标位置
);

INT32 LTDRV_AcGetErrorStat(
    UINT32 acId,
    UINT8 *errorCode  // 输出：0 无错误；1~255 错误码
);
```

（如果你希望错误码可扩展，也可以改成 `UINT32 *errorCode`。）

---

## 5. 硬件相关接口（HARD）

### 5.1 重启 / 待机

SCPI：`HARD:REST` → 控制器重启

```c
INT32 LTDRV_AcSetHardwareReset(
    UINT32 acId
    // 无额外参数，如需扩展可增加 resetMode
);
```

### 5.2 硬件信息查询

SCPI：`HARD:IDN?` → 返回 PN/SN/CPU 版本等

建议用一个结构体承载所有信息：

```c
typedef struct _LTDRV_HardwareInfo {
    char controllerPN[32];
    char controllerSN[32];
    char positionerPN[32];
    char positionerSN[32];
    char cpu1Version[16];
    char cpu2Version[16];
} LTDRV_HardwareInfo;

INT32 LTDRV_AcGetHardwareInfo(
    UINT32             acId,
    LTDRV_HardwareInfo *pInfo  // 输出：硬件信息
);
```

---

## 6. 电压设定接口（485 功能码 0x03）

表中最后一行：

`INT32 LTDRV_AcSetVoltage(UINT32 acId, xxx)`

结合说明：

* 功能码 `0x03` 为“电压设定”
* 数据为 3 字节（例：`00 03 E8` = 1000 → 对应 1V）

建议高层接口直接用“物理量”电压，由底层换算成整数并打包：

```c
INT32 LTDRV_AcSetVoltage(
    UINT32 acId,
    float  voltage    // 目标电压（V），底层转换成 24-bit 整数
);
```

如果你更倾向于直接传“数码量”（例如 0~0xFFFFFF），也可以改成：

```c
INT32 LTDRV_AcSetVoltage(
    UINT32 acId,
    UINT32 rawValue   // 数码量，与 3 字节数据字段一一对应
);
```

先把 **COMM** 这一段表格补完整，然后下面给一份简短的“说明文档”。

---

### 1. COMM 段补全后的表格

```markdown
| 指令类 | 指令                    | 返回值                   | 含义                                    | 接口                                                                                           |
| ------ | ----------------------- | ------------------------ | --------------------------------------- | ---------------------------------------------------------------------------------------------- |
| COMM   | COMM:TTLO 0             |                          | 关闭 TTL 串口输出功能， 默认开机即关闭  | INT32 LTDRV_AcSetTtlOutputMode(UINT32 acId, UINT8 mode)  // 0:关闭；1:输出位置；2:输出速度     |
|        | COMM:TTLO 1             |                          | TTL 串口输出当前位置                    |                                                                                                |
|        | COMM:TTLO 2             |                          | TTL 串口输出当前速度                    |                                                                                                |
|        | COMM:TTLF 921600        |                          | 设置 TTL 串口输出的波特率为921600       | INT32 LTDRV_AcSetTtlBaudrate(UINT32 acId, UINT32 baudrate)                                    |
|        | COMM:485B 921600        |                          | 设置 RS485 的波特率为921600             | INT32 LTDRV_AcSet485Baudrate(UINT32 acId, UINT32 baudrate)                                    |
|        | COMM:485B?              | COMM:485B 921600         | 查询 RS485 波特率                       | INT32 LTDRV_AcGet485Baudrate(UINT32 acId, UINT32 *baudrate)                                   |
|        | COMM:IPAD 192,168,1,1   |                          | 设置网口的 IP 地址为 192.168.1.1        | INT32 LTDRV_AcSetIpAddress(UINT32 acId, UINT8 ip0, UINT8 ip1, UINT8 ip2, UINT8 ip3)           |
|        | COMM:GAT X,X,X,X        |                          | 设置网口的网关                          | INT32 LTDRV_AcSetGateway(UINT32 acId, UINT8 gw0, UINT8 gw1, UINT8 gw2, UINT8 gw3)             |
|        | COMM:SUBD X,X,X,X       |                          | 设置网口的子网掩码                      | INT32 LTDRV_AcSetSubnetMask(UINT32 acId, UINT8 mask0, UINT8 mask1, UINT8 mask2, UINT8 mask3)  |
```

> 类型说明：这里默认用 `UINT8` 表示 IPv4 每一段（0~255），`UINT32` 表示波特率数值。你可以根据实际固件实现改成 `UINT32 ip` 或字符串等。

---

### 2. COMM 模块说明文档（简要版）

#### 2.1 TTL 串口输出控制

**指令：**

* `COMM:TTLO 0`：关闭 TTL 串口输出
* `COMM:TTLO 1`：TTL 串口周期性输出当前位置
* `COMM:TTLO 2`：TTL 串口周期性输出当前速度

**对应接口：**

```c
INT32 LTDRV_AcSetTtlOutputMode(UINT32 acId, UINT8 mode);
// mode = 0: 关闭输出
//      = 1: 输出位置（Position）
//      = 2: 输出速度（Speed）
```

**说明：**

* 该功能用于通过 TTL 串口对外实时输出运动数据（位置/速度）。
* 建议在内部初始化时根据应用场景设置好，不对普通用户开放 GUI 配置（降低误操作风险）。
* 输出格式（比如二进制/ASCII、数据帧结构）应在通信协议章节中统一说明，这里只负责开关与模式选择。

---

#### 2.2 TTL 串口波特率设置

**指令：**

* `COMM:TTLF 921600`：设置 TTL 串口输出的波特率为 921600 bps

**对应接口：**

```c
INT32 LTDRV_AcSetTtlBaudrate(UINT32 acId, UINT32 baudrate);
```

**说明：**

* `baudrate` 为实际波特率数值，如 115200、921600 等。
* 设置成功后，TTL 串口后续输出将使用新的波特率，外部设备（示波器/逻辑分析仪/上位机）需同步配置相同波特率。
* 若固件仅支持固定几个档位，建议在文档中列出支持列表，例如：`[9600, 19200, 115200, 921600]`，其他值返回错误码。

---

#### 2.3 RS485 波特率设置与查询

**指令：**

* `COMM:485B 921600`：设置 RS485 波特率为 921600 bps
* `COMM:485B?`：查询当前 RS485 波特率

  * 返回示例：`COMM:485B 921600`

**对应接口：**

```c
INT32 LTDRV_AcSet485Baudrate(UINT32 acId, UINT32 baudrate);
INT32 LTDRV_AcGet485Baudrate(UINT32 acId, UINT32 *baudrate);
```

**说明：**

* RS485 通讯的波特率必须与上位机/柜内其他节点一致，否则无法正常通讯。
* 建议：

  * 设置非法波特率时返回错误码；
  * 在用户手册中给出推荐/支持的波特率列表；
  * 明确说明是否需要重启控制器或重新上电后设置才生效（如果有）。

---

#### 2.4 以太网 IP / 网关 / 子网掩码设置

**指令：**

* `COMM:IPAD 192,168,1,1`
  设置控制器网口 IP 地址为 `192.168.1.1`
* `COMM:GAT 192,168,1,254`
  设置网关（Gateway）为 `192.168.1.254`
* `COMM:SUBD 255,255,255,0`
  设置子网掩码为 `255.255.255.0`

（示例中的数字可根据实际网络规划调整）

**对应接口：**

```c
INT32 LTDRV_AcSetIpAddress(
    UINT32 acId,
    UINT8  ip0, UINT8 ip1, UINT8 ip2, UINT8 ip3
);

INT32 LTDRV_AcSetGateway(
    UINT32 acId,
    UINT8  gw0, UINT8 gw1, UINT8 gw2, UINT8 gw3
);

INT32 LTDRV_AcSetSubnetMask(
    UINT32 acId,
    UINT8  mask0, UINT8 mask1, UINT8 mask2, UINT8 mask3
);
```

**说明：**

* 以上接口针对 IPv4 地址，每一段取值范围为 0~255。
* 执行 IP/网关/掩码设置后，通常：

  * 若固件支持“在线切换”，则立即生效；
  * 若不支持，则需要在文档中明确说明“需重启控制器后生效”。
* 建议：

  * 在上位机界面做基础合法性校验（例如不能设置广播地址、0.0.0.0 等）；
  * 在用户手册中给出典型配置示例（比如默认 IP、默认子网掩码、默认网关等）。

---

如果你愿意，我可以帮你把 **COMM** 这一段也合并进你那份完整的大表里，输出成一份“接口对照 + 简要说明”的最终版 Markdown，直接塞到手册里就能用。

