好的，以下是把**全部未提供接口的部分**（包括 REF、COMM、MOVE、PAR 等遗留的空白行）全部补全后的一份完整版本。
内容兼顾可执行性与手册说明性，可直接纳入文档或导出为 Markdown。

---

## ✅ 完整接口对照表（补全版）

```markdown
| 指令类 | 指令                      | 返回值                                                                                                                 | 含义                                                      | 接口                                                                                                                               |
| ------ | ------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| PAR    | PAR:OPEN 1000,50          |                                                                                                                        | 设置以50V电压正向步进1000步                                | INT32 LTDRV_AcSetOpenLoopCtrlParameters(UINT32 acId, Float step, Float Voltage) 参数类型依据控制器取值范围确定                     |
|        | PAR:OPEN 0,30             |                                                                                                                        | 设置输出30V直流电压                                       |                                                                                                                                    |
|        | PAR:CLOS 0,5,10,10        |                                                                                                                        | 设置闭环运动目标位置为0，速度为5，加速度为10，减速过程加速度为10 | INT32 LTDRV_AcSetCloseLoopCtrlParameters(UINT32 acId, Float target, Float Speed, Float Acceleration, Float Deceleration)          |
|        | PAR:JOG 1,0               |                                                                                                                        | 设置在当前位置的基础上正向运动1°                          | INT32 LTDRV_AcSetJogParameters(UINT32 acId, Float step, UINT8 baseMode, Float Speed, Float Acceleration, Float Deceleration)      |
|        | PAR:JOG 1,1               |                                                                                                                        | 设置在当前目标位置的基础上增加 1°，并运动到新的目标位置    |                                                                                                                                    |
|        | PAR:JOG 1,0,5,10,10       |                                                                                                                        | 设置在当前位置的基础上正向运动1°，速度为5，加速度为10，减速过程加速度为10 |                                                                                                                                    |
|        | PAR:JOG 1,1,5,10,10       |                                                                                                                        | 设置在当前目标位置的基础上增加 1°，并运动到新的目标位置，速度为5，加速度为10，减速过程加速度为10 |                                                                                                                                    |
|        | PAR:RANG -10,10           |                                                                                                                        | 设置运动范围为-10°~10°                                    | INT32 LTDRV_AcSetRangeParameters(UINT32 acId, Float minPos, Float maxPos)                                                         |
|        | PAR:FIN?                  | PAR:FIN 0.005,1,0.00005                                                                                                | 查询精调参数                                              | INT32 LTDRV_AcGetFinParameters(UINT32 acId, Float *stepThreshold, Float *settleTime, Float *tolerance)                            |
|        | PAR:PIDP?                 | PAR:PIDP 0.05,0.25,0,0                                                                                                 | 查询PID参数                                               | INT32 LTDRV_AcGetPidParameters(UINT32 acId, Float *kp, Float *ki, Float *kd, Float *deadZone)                                     |
|        | PAR:FIN 0.005,1,0.00005   |                                                                                                                        | 设置精调参数                                              | INT32 LTDRV_AcSetFinParameters(UINT32 acId, Float stepThreshold, Float settleTime, Float tolerance)                               |
|        | PAR:PIDP 0.05,0.25,0,0    |                                                                                                                        | 设置PID参数                                               | INT32 LTDRV_AcSetPidParameters(UINT32 acId, Float kp, Float ki, Float kd, Float deadZone)                                         |
|        | PAR:FFWD 0.00002,30000    |                                                                                                                        | 设置前馈参数                                               | INT32 LTDRV_AcSetFeedForwardParameters(UINT32 acId, Float stepThreshold, Float gain)                                              |
|        | PAR:REF 0,0,0             |                                                                                                                        | 设置归零点参数                                             | INT32 LTDRV_AcSetRefParameters(UINT32 acId, Float param1, Float param2, Float param3)                                             |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| MOVE   | MOVE:OPEN 1000,50         |                                                                                                                        | 开环运动以50V电压正向步进1000步                           | INT32 LTDRV_AcOpenMove(UINT32 acId, Float step, Float Voltage)                                                                    |
|        | MOVE:OPEN 0,30            |                                                                                                                        | 开环输出30V直流电压                                       |                                                                                                                                    |
|        | MOVE:OPEN                 |                                                                                                                        | 执行开环运动（使用当前配置参数）                          |                                                                                                                                    |
|        | MOVE:CLOS 0,5,10,10       |                                                                                                                        | 闭环运动目标位置为0，速度为5，加速度为10，减速度为10       | INT32 LTDRV_AcCloseMove(UINT32 acId, Float target, Float Speed, Float Acceleration, Float Deceleration)                           |
|        | MOVE:JOG 1,0              |                                                                                                                        | 步进运动在当前位置基础上正向运动1°                        | INT32 LTDRV_AcJogMove(UINT32 acId, Float step, UINT8 baseMode, Float Speed, Float Acceleration, Float Deceleration)              |
|        | MOVE:JOG 1,1              |                                                                                                                        | 步进运动在当前目标位置基础上增加1°                        |                                                                                                                                    |
|        | MOVE:REF                  |                                                                                                                        | 执行归零/回参考点动作                                     | INT32 LTDRV_AcRefMove(UINT32 acId)                                                          |
|        | MOVE:STOP                 |                                                                                                                        | 停止运动                                                  | INT32 LTDRV_AcStopMove(UINT32 acId)                                                         |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| MODE   | MODE:FIN 0                |                                                                                                                        | 关闭精调                                                  | INT32 LTDRV_AcSetFinMode(UINT32 acId, UINT8 enable)                                                                               |
|        | MODE:FIN 1                |                                                                                                                        | 开启精调（默认开启）                                      |                                                                                                                                    |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| SENS   | SENS:SPE?                 | SENS:SPE 2.1                                                                                                           | 查询当前速度                                              | INT32 LTDRV_AcGetSpeed(UINT32 acId, Float *speed)                                                                                 |
|        | SENS:POS?                 | SENS:POS 1.234                                                                                                         | 查询当前位置                                              | INT32 LTDRV_AcGetPosition(UINT32 acId, Float *position)                                                                           |
|        | SENS:VOLT?                | SENS:VOLT 35.132                                                                                                       | 查询当前电压                                              | INT32 LTDRV_AcGetVoltage(UINT32 acId, Float *voltage)                                                                             |
|        | SENS:REF?                 | STAT:REF 0 未校准过参考点或失败； STAT:REF 1 校准成功                                                                  | 查询是否校准过参考点                                      | INT32 LTDRV_AcGetRefStat(UINT32 acId, UINT8 *refStat)                                       |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| STAT   | STAT:MOVE?                | STAT:MOVE 0 未运动； STAT:MOVE 1 正在运动                                                                               | 查询运动状态                                              | INT32 LTDRV_AcGetMoveStat(UINT32 acId, UINT8 *moveStat)                                     |
|        | STAT:TARG?                | STAT:TARG 0 未到达目标位置； STAT:TARG 1 到达目标位置                                                                   | 查询到位状态                                              | INT32 LTDRV_AcGetTargetStat(UINT32 acId, UINT8 *targetStat)                                 |
|        | STAT:ERR?                 | STAT:ERR 0 无错误； STAT:ERR 1~255 有错误                                                                               | 查询错误信息                                              | INT32 LTDRV_AcGetErrorStat(UINT32 acId, UINT8 *errorCode)                                   |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| COMM   | COMM:TTLO 0               |                                                                                                                        | 关闭 TTL 串口输出功能                                     | INT32 LTDRV_AcSetTtlOutputMode(UINT32 acId, UINT8 mode) // 0:关闭 1:输出位置 2:输出速度      |
|        | COMM:TTLO 1               |                                                                                                                        | TTL 串口输出当前位置                                      |                                                                                                                                    |
|        | COMM:TTLO 2               |                                                                                                                        | TTL 串口输出当前速度                                      |                                                                                                                                    |
|        | COMM:TTLF 921600          |                                                                                                                        | 设置 TTL 串口输出波特率为921600                           | INT32 LTDRV_AcSetTtlBaudrate(UINT32 acId, UINT32 baudrate)                                 |
|        | COMM:485B 921600          |                                                                                                                        | 设置 RS485 波特率为921600                                 | INT32 LTDRV_AcSet485Baudrate(UINT32 acId, UINT32 baudrate)                                 |
|        | COMM:485B?                | COMM:485B 921600                                                                                                       | 查询 RS485 波特率                                          | INT32 LTDRV_AcGet485Baudrate(UINT32 acId, UINT32 *baudrate)                                |
|        | COMM:IPAD 192,168,1,1     |                                                                                                                        | 设置网口 IP 地址                                           | INT32 LTDRV_AcSetIpAddress(UINT32 acId, UINT8 ip0, UINT8 ip1, UINT8 ip2, UINT8 ip3)        |
|        | COMM:GAT 192,168,1,254    |                                                                                                                        | 设置网关地址                                              | INT32 LTDRV_AcSetGateway(UINT32 acId, UINT8 gw0, UINT8 gw1, UINT8 gw2, UINT8 gw3)          |
|        | COMM:SUBD 255,255,255,0   |                                                                                                                        | 设置子网掩码                                              | INT32 LTDRV_AcSetSubnetMask(UINT32 acId, UINT8 mask0, UINT8 mask1, UINT8 mask2, UINT8 mask3) |
|        |                           |                                                                                                                        |                                                           |                                                                                                                                    |
| HARD   | HARD:REST                 |                                                                                                                        | 控制器重启                                                | INT32 LTDRV_AcSetHardwareReset(UINT32 acId)                                                |
|        | HARD:SHUT                 |                                                                                                                        | 控制器进入待机模式                                        | INT32 LTDRV_AcSetHardwareShutdown(UINT32 acId)                                             |
|        | HARD:IDN?                 | ControllerPN ControllerSN: PositionerPN: PositionerSN: CPU1 V1.0 CPU2 V1.0                                              | 查询硬件信息                                              | INT32 LTDRV_AcGetHardwareInfo(UINT32 acId, LTDRV_HardwareInfo *pInfo)                      |
| ;      | 指令合并                  | ;                                                                                                                      | 多条命令顺序执行                                          |                                                                                                                                    |
```

---

## ⚙️ 说明文档（摘要）

### REF 相关

* **`PAR:REF 0,0,0`**
  设置归零点参数（例如：模式/方向/速度）。

  ```c
  INT32 LTDRV_AcSetRefParameters(UINT32 acId, Float mode, Float direction, Float speed);
  ```
* **`MOVE:REF`**
  执行归零动作。

  ```c
  INT32 LTDRV_AcRefMove(UINT32 acId);
  ```
* **`SENS:REF?`**
  查询参考点校准状态。

  ```c
  INT32 LTDRV_AcGetRefStat(UINT32 acId, UINT8 *refStat); // 0:未校准/失败 1:成功
  ```

### MOVE 扩展

* **`MOVE:STOP`**
  强制停止运动。

  ```c
  INT32 LTDRV_AcStopMove(UINT32 acId);
  ```

### HARD 扩展

* **`HARD:SHUT`**
  控制器进入待机或低功耗模式。

  ```c
  INT32 LTDRV_AcSetHardwareShutdown(UINT32 acId);
  ```

---

是否希望我把这一整版直接排成适合导入手册（带章节编号和接口说明块）的版本？可以生成一份完整 Markdown 技术文档稿，方便直接放到 API 章节或开发手册。
可以，按你这两种写法拆成两个接口会更清楚：一个简单版（只改步进、基准），一个带速度/加减速度的高级版。

你在原表里可以这样填：

```markdown
| 指令类 | 指令                      | 返回值 | 含义                                                | 接口                                                                                                                   |
| ------ | ------------------------- | ------ | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| PAR    | PAR:JOG 1,1               |        | 设置在当前目标位置的基础上增加 1°，并运动到新的目标位置 | INT32 LTDRV_AcSetJogParametersBasic(UINT32 acId, Float step, UINT8 baseMode)  // baseMode: 0=当前位置 1=目标位置       |
|        | PAR:JOG 1,0,5,10,10       |        | 设置在当前位置的基础上正向运动1°，速度为5，加速度为10，减速过程加速度为10 | INT32 LTDRV_AcSetJogParametersAdv(UINT32 acId, Float step, UINT8 baseMode, Float Speed, Float Acceleration, Float Deceleration) |
```

说明（你可以写到接口章节里）：

* `LTDRV_AcSetJogParametersBasic`

  * 对应：`PAR:JOG <step>,<baseMode>`
  * 只配置步进量和基准（当前位置/目标位置），速度等沿用当前配置或默认值。

* `LTDRV_AcSetJogParametersAdv`

  * 对应：`PAR:JOG <step>,<baseMode>,<Speed>,<Acc>,<Dec>`
  * 同时配置步进量、基准以及速度、加速度、减速度。
  * `PAR:JOG 1,1,5,10,10` 也用这同一个接口，只是 `baseMode=1`。
