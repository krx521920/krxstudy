---
title: 移动端测试：ADB、日志、Monkey与性能诊断
aliases: [ADB, logcat, Monkey测试, ANR, PerfDog, SoloX, SoloPi, HDC, Wukong, DevEco Studio, 云真机]
tags: [软件测试, Android, 鸿蒙, 性能]
created: 2026-11-15
updated: 2026-11-15
verified: 2026-11-15
---

# 移动端测试：ADB、日志、Monkey与性能诊断

## 一句话解释与类比

**移动端测试除了验证业务，还要验证应用在不同设备、网络、系统限制和用户中断下能否正常工作。**像把一个产品带出实验室：电量不足、信号变化、来电和设备差异都会成为真实使用条件。

## 一、怎样选设备和场景

按实际用户分布与风险选系统版本、厂商、屏幕尺寸、内存档位、芯片架构和权限策略；高覆盖常用机型加少量边缘配置，比随便买很多手机更有意义。

| 场景 | 观察重点 |
|---|---|
| 首次安装、覆盖升级、卸载重装 | 权限、数据库迁移、登录和数据保留是否符合规则 |
| Wi-Fi/移动网络切换、弱网、断网恢复 | 超时提示、重试、数据同步、是否重复提交 |
| 来电、锁屏、切后台、系统回收 | 音视频状态、进度、敏感页面和恢复行为 |
| 拒绝/撤回权限 | 功能降级、解释与继续使用路径 |
| 低电量、低存储空间、发热 | 操作失败是否明确，缓存和下载是否可恢复 |

后台受限、应用被系统杀掉与应用自己崩溃不是同一原因；先记录现象再找日志。

## 二、ADB：电脑与 Android 的调试桥

ADB = Android Debug Bridge，Android 调试桥，逐字母读 A-D-B。一般由电脑客户端、电脑上的服务端和设备中的守护程序配合，提供设备枚举、Shell、日志和文件等调试能力。

在自己的测试设备开启开发者选项、允许调试并确认电脑授权后，可使用：

```bash
adb devices
adb shell getprop ro.build.version.release
adb logcat -v threadtime
```

分别检查连接设备、读取 Android 版本、观察带线程/时间信息的日志。多设备时需选择目标，例如 `adb -s SERIAL ...`；`SERIAL` 要换成实际测试设备编号。连接状态 unauthorized 时先处理设备授权，不要假定是应用故障。

ADB 不是绕过锁屏与授权的万能控制器。调试权限也不等于 root；不同系统版本和应用属性限制能读取的信息。

## 三、logcat、Crash 与 ANR

logcat 是 Android 日志工具。先记录复现时间、包名、版本和操作，再结合进程/标签筛选。只搜 ERROR 会漏掉关联信息，也会把其他应用的错误误算成自己的问题。

**Crash（崩溃）**可能来自未捕获异常、原生错误等；**ANR = Application Not Responding，应用无响应**，是系统判定某类交互/组件响应超时。ANR 不一定导致立即退出，阈值随场景和系统规则不同，不能一律背“五秒”。

排查 ANR 应看主线程、锁等待、同步跨进程调用、磁盘/网络操作以及相关线程；堆栈只是某一时点的证据，还需结合时间线和系统负载。原生崩溃需要对应版本符号和崩溃转储，思想可联系 [[Minidump与Windows崩溃转储分析]]，但工具和格式并不相同。

## 四、Monkey 随机事件测试

Android Monkey 随机发送点击、手势等事件，适合暴露异常操作顺序下的稳定性问题。示例仅面向自有隔离练习应用：

```bash
adb shell monkey -p com.example.demo -s 1234 --throttle 200 -v 500
```

`-p` 限定包，`-s` 固定伪随机种子，`--throttle` 设置事件间隔，末尾是事件数。执行前确保测试账号没有真实付款、发消息或外部副作用能力；限定包也不意味着应用内部所有动作都无副作用。

保存种子、事件数、设备、版本、日志、初始状态及结束原因。相同种子有助重放，但系统时序和界面状态变化仍可能影响复现。

“8 小时零 Crash”只能说明这个版本在该设备、起始状态和随机事件策略下未观察到崩溃，不能证明功能、权限、支付或所有路径正确。

## 五、性能采集工具

| 工具 | 做什么 | 不能代替什么 |
|---|---|---|
| PerfDog | WeTest 的终端性能分析工具，按支持平台采集帧率、CPU、内存等 | 业务成功断言和服务端容量测试 |
| SoloX | 移动端性能数据采集项目 | 数据口径核对、真实体验判断 |
| SoloPi | 支付宝开源的 Android 测试工具，涉及录制回放、性能等能力 | 跨版本兼容性核验和清晰的验收标准 |
| 系统 Profiler | 深入线程、内存、调用与系统事件 | 与用户操作关联的业务解释 |

FPS = Frames Per Second，每秒帧数，逐字母读 F-P-S；帧时间也很重要，平均 60 FPS 仍可能夹杂明显卡顿。内存高可能是缓存，不能直接判定泄漏，见 [[OOM：内存不足、显存不足与内存泄漏]]。

功耗/耗电、发热和流量要固定屏幕亮度、网络、设备温度、后台应用、运行时长和功能步骤。USB 供电、工具采样、系统权限都可能影响测量，比较两个版本必须保持条件相近。

## 六、鸿蒙中的 HDC、Wukong 与 DevEco

HDC = OpenHarmony Device Connector，设备连接调试工具，逐字母读 H-D-C。可用 `hdc list targets` 查看连接设备，具体命令以匹配的 SDK 和设备系统为准。它与 Android ADB 的角色相近，但不是可以互换的同一个程序。

Wukong（悟空）用于稳定性测试；DevEco Studio 是开发环境，其 Profiler 提供性能分析能力。不同 HarmonyOS/OpenHarmony 版本、设备类型和权限的支持范围不完全相同，不能用“鸿蒙就是 Android 工具换名字”理解。

## 七、云真机与测试报告

云真机是远程访问真实手机执行检查的平台能力；模拟器则模拟设备环境。云真机利于覆盖设备矩阵，但网络、传感器、专用外设和地域条件未必等同真实用户现场。

记录：设备型号/系统、应用包/版本、测试账号类别、网络条件、权限状态、步骤、指标口径、截图日志和失败次数。测试结束清理账号与测试文件，避免把真实凭据留在共享设备。

学习路径：先连接一台自有测试机并读日志，再做断网与后台恢复，最后增加性能采集、随机事件和设备矩阵。脚本组织见 [[移动自动化：Appium、UIAutomator2、Maestro与Midscene]]。

## 参考资料

核对日期：2026-11-15；设备支持和安装要求按版本核对。本篇未连接手机或执行随机操作。

- [Android ADB](https://developer.android.com/tools/adb)、[logcat](https://developer.android.com/tools/logcat)、[Monkey](https://developer.android.com/studio/test/other-testing-tools/monkey)、[ANR](https://developer.android.com/topic/performance/issues/anr)。
- [SoloX](https://github.com/smart-test-ti/SoloX)、[SoloPi](https://github.com/alipay/SoloPi)、[PerfDog 官网](https://perfdog.wetest.net/)。
- [华为 HDC](https://developer.huawei.com/consumer/cn/doc/HarmonyOS-Guides/hdc/)、[DevEco 性能调优流程](https://developer.huawei.com/consumer/cn/doc/HarmonyOS-Guides/ide-hmos-profiler-process)。
