---
marp: true
theme: default
paginate: true
size: 16:9
math: false
style: |
  section {
    font-family: "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    padding: 48px 58px 42px 58px;
  }
  h1 { font-size: 38px; color: #0b3a5b; margin-bottom: 18px; }
  h2 { font-size: 30px; color: #0b3a5b; margin-bottom: 16px; }
  h3 { font-size: 23px; color: #134e4a; margin-bottom: 10px; }
  p, li { font-size: 22px; line-height: 1.35; }
  ul { margin-top: 8px; }
  strong { color: #0b3a5b; }
  table { font-size: 18px; }
  .subtitle { font-size: 25px; color: #334155; margin-top: 22px; }
  .tag { display: inline-block; padding: 4px 12px; border-radius: 999px; background: #e0f2fe; color: #075985; font-size: 19px; margin: 6px 8px 6px 0; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }
  .box { border: 2px solid #cbd5e1; border-radius: 14px; padding: 16px 18px; background: #f8fafc; }
  .box h3 { margin: 0 0 8px 0; }
  .small li, .small p { font-size: 19px; }
  .flow { display: flex; align-items: center; gap: 10px; margin-top: 24px; }
  .node { border: 2px solid #0b3a5b; border-radius: 13px; padding: 12px 14px; font-size: 20px; text-align: center; background: #f8fafc; min-width: 118px; }
  .arrow { font-size: 28px; color: #64748b; }
  .note { font-size: 18px; color: #64748b; margin-top: 12px; }
  .center { text-align: center; }
  .tight p, .tight li { font-size: 18px; line-height: 1.28; }
  .mini table { font-size: 16px; }
---

<!-- _class: lead -->
# 一种基于进程组生命周期的处理器核、内存与设备资源确定性编排方法及系统

<div class="subtitle">PPT 压缩版 · 按专利交底模板组织 · Marp</div>

<span class="tag">进程组生命周期</span>
<span class="tag">CPU 核剥离</span>
<span class="tag">物理内存预编排</span>
<span class="tag">设备启动区传递</span>

---

# 核心保护点总览

**一句话概括：** 以进程组生命周期为主线，将 CPU core、物理内存、设备资源、启动区和异常回收绑定为一个确定性资源编排闭环。

<div class="grid2 small">
<div class="box">
<h3>独立保护点</h3>
<ul>
<li>进程组生命周期管理</li>
<li>加载期 CPU / 内存 / 设备统一编排</li>
<li>启动区固化资源描述</li>
<li>正常卸载与异常回收闭环</li>
</ul>
</div>
<div class="box">
<h3>从属增强点</h3>
<ul>
<li>CPU hotplug 核剥离</li>
<li>物理内存块排序与合并</li>
<li>设备注册表查询</li>
<li>心跳监控与诊断快照</li>
</ul>
</div>
</div>

---

# 1. 发明背景与现有技术

## 发明背景技术简介

本发明面向半导体装备、精密运动控制和低时延数据面执行场景。

核心矛盾：关键执行任务若直接运行在通用 OS 或普通实时任务环境中，容易受到：

- 调度、tick、中断迁移影响；
- 内存缺页、运行期分配、驱动栈路径影响；
- CPU、内存、设备资源竞争影响。

**目标：在执行单元启动前完成 CPU、内存、设备和启动参数的确定性编排。**

---

# 1. 发明背景与现有技术

## 现有技术的不足之处

<div class="grid2 small">
<div class="box">
<h3>运行期不确定性</h3>
<ul>
<li>资源申请与执行生命周期解耦</li>
<li>内存、设备、CPU 分散管理</li>
<li>关键路径仍可能动态申请资源</li>
</ul>
</div>
<div class="box">
<h3>隔离与回收不足</h3>
<ul>
<li>绑核不等于脱离 OS 调度</li>
<li>设备查询路径不稳定</li>
<li>异常退出后回收不一致</li>
</ul>
</div>
</div>

<div class="flow center">
<div class="node">实时任务启动</div><div class="arrow">→</div>
<div class="node">运行期申请</div><div class="arrow">→</div>
<div class="node">动态查询设备</div><div class="arrow">→</div>
<div class="node">异常分散回收</div>
</div>

---

# 2. 主要创新技术点说明

## 本发明创造要保护的创新技术与现有技术的区别

**核心创新：以“进程组生命周期”为资源编排单位，而不是分别管理 CPU、内存、设备。**

<div class="flow center">
<div class="node">加载请求</div><div class="arrow">→</div>
<div class="node">创建进程组控制块</div><div class="arrow">→</div>
<div class="node">资源统一编排</div><div class="arrow">→</div>
<div class="node">启动区固化</div><div class="arrow">→</div>
<div class="node">数据面运行</div>
</div>

---

# 2. 主要创新技术点说明

## 关键区别点

1. **以进程组为资源边界**：统一申请、绑定、运行和释放 CPU core、物理内存、设备资源。
2. **加载阶段完成资源固化**：镜像、CPU 数量、内存规格、设备列表在启动前确定。
3. **处理器核剥离**：通过 CPU hotplug 等机制，使关键执行核脱离普通调度干扰。
4. **物理内存预申请与块合并**：降低缺页、碎片和运行期扩展带来的抖动。
5. **设备注册表 + 启动区传递**：避免数据面启动后反复发现设备。
6. **正常卸载与异常回收共用闭环**：确保资源状态与生命周期一致。

---

# 进程组生命周期状态机

<div class="flow center">
<div class="node">未创建</div><div class="arrow">→</div>
<div class="node">资源申请中</div><div class="arrow">→</div>
<div class="node">启动区生成中</div><div class="arrow">→</div>
<div class="node">运行中</div>
</div>

<div class="flow center">
<div class="node">运行中</div><div class="arrow">→</div>
<div class="node">卸载 / 异常</div><div class="arrow">→</div>
<div class="node">回收中</div><div class="arrow">→</div>
<div class="node">已卸载</div>
</div>

<div class="grid2 small">
<div class="box">
<h3>正常路径</h3>
<p>加载成功后进入运行态；控制面主动卸载时，停止进程组并按资源记录释放。</p>
</div>
<div class="box">
<h3>异常路径</h3>
<p>心跳超时或启动失败时，先冻结状态 / 记录诊断信息，再进入统一回收路径。</p>
</div>
</div>

---

# 3. 技术方案及有益效果

## 本发明创造的主要实施方式：系统组成

<div class="grid2 small">
<div class="box">
<h3>控制面</h3>
<ul>
<li>控制面进程</li>
<li>进程组管理模块</li>
<li>状态监控模块</li>
<li>启动区生成模块</li>
</ul>
</div>
<div class="box">
<h3>资源与数据面</h3>
<ul>
<li>CPU 资源管理模块</li>
<li>内存资源管理模块</li>
<li>设备资源管理模块</li>
<li>数据面进程组 / 执行进程</li>
</ul>
</div>
</div>

**进程组控制块记录：PG ID、状态机、CPU core 列表、内存块列表、设备列表、启动参数。**

---

# 3. 技术方案及有益效果

## 本发明创造的主要实施方式：加载流程

<div class="flow center">
<div class="node">提交加载参数</div><div class="arrow">→</div>
<div class="node">创建 PG 控制块</div><div class="arrow">→</div>
<div class="node">申请 CPU</div><div class="arrow">→</div>
<div class="node">申请并整理内存</div>
</div>

<div class="flow center">
<div class="node">查询设备注册表</div><div class="arrow">→</div>
<div class="node">生成启动区</div><div class="arrow">→</div>
<div class="node">启动数据面 PG</div><div class="arrow">→</div>
<div class="node">返回 PG ID</div>
</div>

<div class="note">加载期资源固化：CPU、内存、设备不是运行后动态发现，而是在启动前整理成启动区。</div>

---

# 3. 技术方案及有益效果

## 本发明创造的主要实施方式：启动区内容

| 启动区字段 | 主要内容 | 作用 |
|---|---|---|
| 头部信息 | 版本号、校验值、PG ID、入口地址 | 保证启动一致性 |
| CPU 描述 | core 数量、core 列表、逻辑映射 | 固化执行核边界 |
| 内存描述 | 内存块数量、物理地址、VA 映射、属性 | 避免运行期内存发现 |
| 设备描述 | 设备名称、寄存器基地址、中断号、属性 | 避免运行期设备枚举 |
| 可选参数 | 日志、心跳、共享内存、安全退出入口 | 支持监控与异常回收 |

---

# 3. 技术方案及有益效果

## 本发明创造的其他实施方式

- **可重复加载**：保存资源描述表，复用 CPU、内存、设备规格。
- **分阶段异常回收**：停止执行 → 冻结现场 → 诊断快照 → 释放设备/内存/CPU。
- **多进程组资源隔离**：不同 PG 拥有独立 CPU core、内存块和设备列表。
- **控制面保留核策略**：预留控制面 core，剩余 core 由资源管理模块分配。
- **资源失败回滚**：按申请相反顺序释放已申请资源，避免半加载状态。
- **按业务角色划分 PG**：运动控制、采样、通信、诊断分别编排资源。

---

# 3. 技术方案及有益效果

## 本发明创造的有益效果论证

<div class="grid2 small">
<div class="box">
<h3>确定性</h3>
<ul>
<li>减少运行期资源申请</li>
<li>降低设备发现与内存扩展抖动</li>
<li>便于分析最坏情况时延</li>
</ul>
</div>
<div class="box">
<h3>可靠性</h3>
<ul>
<li>CPU、内存、设备边界清晰</li>
<li>异常后可按控制块确定性回收</li>
<li>减少资源泄漏和残留占用</li>
</ul>
</div>
</div>

**价值总结：把低时延执行环境从“松散配置”变为“可重复、可检查、可回收”的生命周期闭环。**

---

# 验证指标与取证线索

<div class="mini">

| 维度 | 可验证指标 | 取证线索 |
|---|---|---|
| CPU 编排 | core online/offline 状态、PG-core 映射 | 加载日志、CPU 状态变化 |
| 内存编排 | 物理内存块列表、连续块合并记录 | 内存分配记录、启动区内容 |
| 设备编排 | 设备名、寄存器基地址、中断号 | 设备注册表、BOOT 区 |
| 生命周期 | 加载、运行、卸载、异常回收状态 | PG 状态机、心跳记录 |
| 异常恢复 | 资源是否完整释放 | 回收日志、二次加载成功率 |

</div>

**价值：把“内部软件机制”转化为可观察的系统行为。**

---

# 4. 发明创造价值自评

满分 5 分

| 自评维度 | 分数 | 理由 |
|---|---:|---|
| 创新性 | 4.4 | 将 CPU hotplug、内存预分配、设备注册绑定到进程组生命周期，形成组合创新。 |
| 市场价值 | 4.5 | 适用于光刻机、半导体装备、高速运动控制、低时延通信平台。 |
| 技术价值 | 4.8 | 直接解决资源隔离、确定性构造、运行期抖动和异常回收问题。 |
| 可规避程度 | 4.1 | 若覆盖“生命周期 + CPU 剥离 + 内存预申请 + 启动区 + 回收”，较难单点规避。 |
| 侵权证据可获得性 | 3.2 | 可通过加载参数、CPU online/offline、内存块记录、启动区和异常回收行为辅助证明。 |

---

<!-- _class: lead -->
# 一页总结

**进程组生命周期 = 低时延资源编排的主轴**

<div class="flow center">
<div class="node">加载前编排</div><div class="arrow">→</div>
<div class="node">启动区固化</div><div class="arrow">→</div>
<div class="node">独占/隔离运行</div><div class="arrow">→</div>
<div class="node">统一卸载/异常回收</div>
</div>

<div class="subtitle">本方案的保护重点不是单一资源动作，而是“进程组全生命周期 + 多资源确定性闭环”。</div>
