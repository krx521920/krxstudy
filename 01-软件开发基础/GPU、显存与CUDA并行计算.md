---
title: GPU、显存与 CUDA 并行计算
aliases: [GPU, 显卡与GPU, VRAM, 显存, CUDA, GPU并行计算]
tags: [计算机硬件, GPU, 并行计算, AI]
created: 2026-09-08
updated: 2026-09-08
verified: 2026-09-08
---

# GPU、显存与 CUDA 并行计算

> [!summary] 一句话解释
> GPU 擅长让大量计算任务并行推进，显存保存它需要的数据，CUDA 是让软件利用受支持 NVIDIA GPU 进行通用计算的平台与编程模型。

**GPU = Graphics Processing Unit（图形处理器，读 G-P-U）**。它从图形计算发展而来，也用于科学计算、图像处理和人工智能等任务。

像同一车间中的大量计算工位：当工作能切成许多相似的小任务时，并行设备很合适；但任务若前后严格依赖或很小，搬运与组织成本可能抵消收益。

## GPU 与 CPU 的差别不是“一个有脑子，一个没脑子”

**CPU = Central Processing Unit（中央处理器，读 C-P-U）**，擅长广泛的控制逻辑、分支和低延迟通用处理；GPU 通常把更多资源投入高吞吐的并行计算。

| 场景 | 通常如何理解 |
|---|---|
| 大量像素、向量、矩阵上的相似运算 | 常有机会发挥 GPU 并行能力 |
| 复杂控制流程、小量计算、频繁依赖前一步 | CPU 可能更合适 |
| 读写硬盘、网络等待 | 不会因为换成 GPU 自动消失 |
| 大模型应用 | CPU、GPU、存储、网络和软件共同工作 |

CPU 也能并行和向量计算，GPU 也能执行分支；这里描述侧重点，不是绝对功能限制。GPU 的“核心数”与 CPU 核心数也不能直接一比一换算。

## GPU 芯片不等于整张显卡

一张常见独立显卡包括 GPU 芯片、显存颗粒、PCB、供电电路、接口、固件与散热组件等。**PCB = Printed Circuit Board（印刷电路板，读 P-C-B）**。

集成 GPU 可能与 CPU 集成在同一芯片或封装中，常共享系统物理内存。独立 GPU 常配有专用设备内存，但也存在其他布局。有没有显示器接口不是判断能否计算的充分条件。

## VRAM 是什么，为什么和 RAM 不能简单互换

**VRAM = Video Random-Access Memory（视频随机存取存储器，通称显存，读 V-RAM）**，是你写的 varm 在该语境下的正确拼写。

显存保存纹理、帧缓冲、几何数据，或者模型权重、中间张量、计算缓存等。它主要说明用途，并不是所有显存都使用一种独有的存储单元技术。

**RAM = Random-Access Memory（随机存取存储器，读 RAM）**。日常说“电脑有 32 GB 内存”，通常指系统主内存，不是独立显卡专用显存。

显存常见技术：

- **GDDR = Graphics Double Data Rate（图形双倍数据速率，读 G-D-D-R）**：面向图形/高带宽需求的 DRAM 技术家族。
- **HBM = High Bandwidth Memory（高带宽内存，读 H-B-M）**：采用堆叠等封装组织方式的高带宽 DRAM 技术。
- **DRAM = Dynamic Random-Access Memory（动态随机存取存储器，读 D-RAM）**，需要刷新，详见 [[存储层次：RAM、SRAM、DRAM、Cache与Flash]]。

不是“主内存是 DRAM，所以显存一定不是 DRAM”。这里比较的是角色和技术两个维度。

## 容量、带宽、算力分别是什么

容量决定能放下多少数据；带宽决定单位时间能搬运多少数据；算力描述一定数据类型、运算和条件下能完成多少计算。三者不能互相代替。

假设模型有 10 亿个参数，每个参数按 2 字节保存，权重本身约 20 亿字节，即约 2 GB。运行还需要中间结果、计算缓存、运行环境等，训练还可能需要梯度和优化器状态，不能仅凭权重大小判断总显存需求。

GB 在这里按十进制十亿字节计算；**GiB = Gibibyte（吉比字节）** 按 2³⁰ 字节计算，约 1.86 GiB，不应混淆单位。

同样容量的两张 GPU 可能在带宽、计算类型、驱动与软件支持方面差很多。买到大显存不等于任何模型都运行得快。

## 主内存到显存：数据搬运也是成本

在常见独立 GPU 系统中，应用先在 CPU 侧准备任务，必要数据经互连传到 GPU 设备内存，GPU 运算后再按需交回结果。应用可通过异步执行等方式重叠部分工作，但不是完全免费。

**PCIe = Peripheral Component Interconnect Express（高速外设互连标准，读 P-C-I-E）** 是常见互连方式之一。系统还有其他直连、共享或专用互连设计，不能统一假定路径和带宽。

操作系统显示的“共享 GPU 内存”不等于凭空长出同等速度的专用显存。可能涉及系统内存访问、迁移和性能变化。

## 统一物理内存与 CUDA Unified Memory 不完全相同

某些平台的 CPU/GPU 实际共享同一池物理内存；CUDA **Unified Memory（统一内存）** 则是一种软件可见的内存管理能力，允许相应内存被 CPU/GPU 访问，具体可能利用迁移或硬件一致性等机制。

共同地址空间不等于所有地址的访问速度一样，也不等于永远没有迁移成本。应看具体平台和分配方式，不能只凭“统一”二字判断。

## CUDA 究竟是什么

**CUDA** 历史名称展开为 **Compute Unified Device Architecture（统一计算设备架构，常读“库达”）**。今天通常把它当作 NVIDIA 并行计算平台与编程模型的名称。

它不是一块芯片，不是显存，也不只是“安装一个驱动”。其生态包括编程接口、运行环境、编译工具和计算库等，使软件能组织并启动 GPU 计算任务。

| 层次 | 职责 |
|---|---|
| GPU 硬件 | 实际执行支持的运算 |
| NVIDIA 驱动 | 与设备和系统交互，提供相应执行支持 |
| CUDA 运行库与接口 | 组织设备内存、任务启动、同步等 |
| CUDA Toolkit（工具包） | 编译器、头文件、工具和库等开发能力 |
| 上层框架 | 使用底层库组织模型或其他计算 |

运行某个预编译应用不一定需要在本机安装完整 Toolkit；但必须满足它实际依赖的驱动、运行库和设备条件。能点亮桌面，也不等于已满足某个 CUDA 应用的全部要求。

CUDA 原生生态主要面向受支持 NVIDIA GPU，不能仅靠安装 Toolkit 让任意 AMD、Intel 或 Apple GPU 原生变成 CUDA 设备。其他平台有各自计算接口和迁移方案，具体兼容另行核对。

## Kernel、Thread、Block、Grid 怎么理解

CUDA 中 Kernel（计算内核）是交给 GPU 执行的计算函数，**不是操作系统内核**。

程序将工作组织为线程 Thread（线程）、线程块 Block（块）与 Grid（网格）。例如把两个很长数组相加，每个线程负责一项或若干项；块帮助组织协作，GPU 再按硬件能力调度。

GPU 线程与 CPU 操作系统线程不是一一对应。也不能假定写了某个块编号，它就一定先于另一个块执行。[NVIDIA CUDA 编程模型](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html)

## Cache、Shared Memory 与显存的区别

GPU 内部也有寄存器和缓存等快速小容量存储。CUDA 的 Shared Memory（共享内存）通常指块内协作使用的片上存储概念；它不是 Windows 显示的“共享 GPU 内存”，也不是整个系统 RAM 的同义词。

具体层次、大小、缓存策略和编程限制随架构而异。理解原理时先记住：存得近通常更快但更少，重复搬大数据会影响性能。

此前的 [[高效注意力：FlashAttention、GQA、MLA与线性注意力]] 就涉及减少高带宽设备内存与片上存储之间的数据往返。

## 为什么安装好 CUDA，程序仍可能不用 GPU

还要看应用是否实现了 GPU 路径、框架构建是否支持对应设备、数据是否放在合适设备上、任务有没有实际启动以及依赖是否匹配。

安装 CUDA 不会自动把任意 Python for 循环变成 GPU 并行代码。多个 GPU 的显存也不自动成为一个没有通信成本的统一大池，通常需要模型切分或其他并行策略。

学习建议：先能口述 CPU/GPU 分工与“容量、带宽、算力”的区别，再学习框架的设备选择，最后看 CUDA 内存与线程模型。本次没有安装驱动/Toolkit，也没有在本机 GPU 上跑计算测试。

关联：[[计算机硬件与底层软件学习地图]]、[[PCB、供电与散热：计算机硬件的物理基础]]、[[设备驱动：操作系统控制硬件的翻译层]]、[[大模型推理加速：FP8、量化、KV Cache与多Token预测]]。

## 参考资料

核对日期：2026-09-08。具体支持列表与版本匹配应以正在使用的 CUDA 和设备文档为准。

- [NVIDIA：CUDA 编程模型](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html)
- [NVIDIA：CUDA 介绍与名称来源](https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/introduction.html)
- [NVIDIA：CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/)
- [NVIDIA：CUDA 兼容性](https://docs.nvidia.com/deploy/cuda-compatibility/)
- [Micron：HBM](https://www.micron.com/products/memory/hbm)
- [Micron：Graphics Memory](https://www.micron.com/products/memory/graphics-memory)
