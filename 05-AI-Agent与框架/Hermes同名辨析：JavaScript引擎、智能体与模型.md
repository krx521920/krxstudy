---
title: Hermes同名辨析：JavaScript引擎、智能体与模型
aliases:
  - Hermes
  - Hermes Agent
  - Hermes引擎
  - Hermes模型
tags:
  - AI-Agent
  - JavaScript
  - React-Native
  - 概念辨析
created: 2026-10-01
updated: 2026-10-01
verified: 2026-10-01
---

# Hermes同名辨析：JavaScript引擎、智能体与模型

> [!summary] 一句话解释
> **是的，有叫 Hermes 的 JavaScript 引擎，也有叫 Hermes Agent 的智能体；它们是不同团队的不同项目。此外，Nous Research 还有 Hermes 大语言模型系列，不能把三者当成同一个软件。**

Hermes 英文读音近似“赫米兹”，中文也常见“赫尔墨斯”的译名。判断技术项目时，完整名称、维护团队和官方地址比中文译名更可靠。

## 一、先用一张表分清楚

| 名称 | 团队或官方归属 | 是什么 | 主要作用 |
|---|---|---|---|
| Hermes / Hermes JS Engine | Meta；官方仓库 `facebook/hermes` | JavaScript 引擎 | 执行 JavaScript 程序，重点优化 React Native 场景 |
| Hermes Agent | Nous Research；官方仓库 `NousResearch/hermes-agent` | 智能体软件及其运行系统 | 连接模型、工具、记忆等能力来处理用户任务 |
| Hermes 模型系列，如 Hermes 3、Hermes 4 | Nous Research | 大语言模型系列 | 根据输入生成回答或工具调用请求等输出 |

**JS 是 JavaScript 的简称**，在这里指编程语言。**AI 是 Artificial Intelligence（人工智能）**；**LLM 是 Large Language Model（大语言模型）**，用于理解和生成语言等内容。

项目身份依据：[Meta Hermes 仓库](https://github.com/facebook/hermes)、[Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs/)、[Hermes 3 官方模型集合](https://huggingface.co/collections/NousResearch/hermes-3)、[Hermes 4 官方模型卡示例](https://huggingface.co/NousResearch/Hermes-4-14B)。

## 二、React Native 里的 Hermes：执行代码的引擎

[[React Native原生应用与WebView方案对比|React Native]] 应用需要执行 JavaScript 逻辑，例如处理点击、更新数据和计算界面状态。Hermes 就是承担这类代码执行工作的引擎。

**Engine 是“引擎”**。软件里的引擎不是一种统一的产品类型，而是对承担核心处理工作的组件的一种称呼。这里说的是 JavaScript 引擎，不是模型推理引擎，也不是搜索引擎。

生活类比：你给一台机器一份准确的操作程序，它按程序执行；不是向一位智能助手描述模糊目标，再由它选择下一步行动。

例如课程应用中已经编写了“点击收藏，就把收藏状态改为是”的逻辑，Hermes 执行相应 JavaScript，React Native 再完成相关界面更新。Hermes 本身不是整个界面框架。

其官方介绍强调启动速度优化、提前进行的静态优化和紧凑字节码。**字节码**可以先理解为经过转换、供对应运行引擎执行的指令表示，不是大模型的参数文件。[Hermes 引擎说明](https://github.com/facebook/hermes)

React Native 当前默认使用 Hermes。这不代表应用因此拥有人工智能，也不代表开发者要安装 Hermes Agent。[React Native：Using Hermes](https://reactnative.dev/docs/hermes)

## 三、Nous Research 的 Hermes Agent：组织任务执行的智能体

**Agent 读作“诶紧特”，在这里是“智能体”**。Hermes Agent 是 Nous Research 的开源智能体项目，不是 Meta 的 JavaScript 引擎换了用途。

可以把它理解为一套会连接“大语言模型”和“可使用工具”的任务系统：

1. 接收用户请求。
2. 把任务和必要上下文交给所配置的模型。
3. 根据模型输出、运行规则和授权范围调用工具。
4. 获取工具的实际结果，再继续处理或给出答复。

这是帮助初学者理解的简化过程，具体任务不一定经过全部步骤，也不保证每次都能成功。进一步阅读 [[Agent Harness：模型之外的运行系统]]、[[ReAct：推理、行动与观察的Agent模式]]。

官方资料列出的能力包括持久记忆、技能复用、定时任务以及不同交互入口。实际能做什么，还取决于所选模型、已接入工具、配置和权限。[Hermes Agent 官方仓库](https://github.com/NousResearch/hermes-agent)

### 用“整理课程资料”举例

假设用户授权它读取某个课程资料目录，它可能读取文件、归纳要点，再通过文件工具保存笔记；如果没有文件权限或相应工具，就不能仅凭一句请求完成这些动作。

这个例子是能力组合的说明，不是本次实际执行的任务，也不表示任意安装状态下都已经具备这些权限。

### “会学习”是不是不断重新训练大模型

不能这样直接推断。官方这里描述的重要机制包括保存记忆、整理经验、创建和复用技能。

**Skill 是“技能”**，可以理解为可供智能体再次使用的操作说明或流程。保存这种说明、下一次读取它，与更新神经网络的模型权重不是同一件事。“记住了你的偏好”不能作为“重新训练了底层模型”的证据。[官方文档中的记忆与技能说明](https://hermes-agent.nousresearch.com/docs/)

## 四、Hermes 模型：提供语言能力的另一层

Nous Research 也发布 Hermes 模型系列。例如 Hermes 3 是模型系列；Hermes 4 中的 `Hermes-4-14B`，官方模型卡说明它基于 Qwen 3 14B。这些名称指模型，而不是完整的智能体执行软件。[Hermes 3 模型集合](https://huggingface.co/collections/NousResearch/hermes-3)、[Hermes 4 模型卡](https://huggingface.co/NousResearch/Hermes-4-14B)

在任务系统中，可以粗略类比为：

- **模型**：负责理解输入、生成下一步内容的部分。
- **Agent / Harness**：组织模型调用、工具执行、记忆与任务过程的系统。
- **JavaScript 引擎**：运行某种编程语言代码的底层组件。

这个类比不意味着模型具有人类意识，也不表示引擎、模型和智能体是一条固定的依赖链。

尤其注意：**Hermes Agent 并不强制只能使用 Hermes 模型。** 官方提供多种模型服务接入方式，也可配置兼容的自有端点；具体模型和工具调用兼容性仍需核对。[模型接入说明](https://github.com/NousResearch/hermes-agent)

相关基础见 [[大模型从数据、Token到训练与本地部署]]。

## 五、三个同名项目是什么关系

- Meta 的 Hermes 引擎与 Nous Research 的 Hermes Agent 是不同项目；不能因同名推断由同一团队开发，或前者是后者的前身。
- Nous Research 的 Hermes Agent 与 Hermes 模型属于同一团队的不同层次产品，但不是同一个东西。
- 使用 Hermes 引擎的 React Native 应用可以完全不含人工智能功能。
- 即使一个智能体应用使用 JavaScript 开发，具体用了什么引擎也要查看其实现，不能按产品名判断。

换言之：**同名不代表同一产品；同一团队也不代表同一技术层次。**

## 六、以后怎样判断别人说的是哪一个

看上下文线索：

- 出现 React Native、JavaScript、启动速度、字节码：通常是在说 **Hermes 引擎**。
- 出现工具、记忆、技能、任务、机器人、自动化：可能是在说 **Hermes Agent**，还应核对团队和链接。
- 出现模型权重、模型卡、参数规模、微调、Hermes 3 或 Hermes 4：通常是在说 **Hermes 模型**。

不要只搜索一个短名字就复制安装命令。以官方团队的主页、代码仓库和文档交叉确认身份，避免混入同名项目或仿冒网站。本篇只解释概念，没有安装 Hermes、授权账号或修改执行权限。

## 学习建议与关联概念

先记住“引擎执行代码、模型生成内容、智能体组织任务”，再分别深入，暂时不必研究每种底层实现。

- [[React Native原生应用与WebView方案对比]]：理解本次疑问中的 Hermes 引擎来源。
- [[Node.js与pnpm]]：区分语言运行环境、引擎与包管理工具。
- [[Agent Harness：模型之外的运行系统]]：理解模型外的运行系统负责什么。
- [[ReAct：推理、行动与观察的Agent模式]]：理解工具调用和观察结果形成的循环。
- [[大模型从数据、Token到训练与本地部署]]：区分模型权重、推理与训练。

## 参考资料

核对日期：2026-10-01。Hermes Agent 的能力和接入方式变化较快，本文只记录定位和边界，不把宣传中的效果描述视为每次执行都能实现的保证。

- [Meta：facebook/hermes](https://github.com/facebook/hermes)
- [React Native：Using Hermes](https://reactnative.dev/docs/hermes)
- [Nous Research：Hermes Agent 官方文档](https://hermes-agent.nousresearch.com/docs/)
- [Nous Research：hermes-agent 官方仓库](https://github.com/NousResearch/hermes-agent)
- [Nous Research：Hermes 3 模型集合](https://huggingface.co/collections/NousResearch/hermes-3)
- [Nous Research：Hermes-4-14B 模型卡](https://huggingface.co/NousResearch/Hermes-4-14B)
