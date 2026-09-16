---
title: LangChain、LangGraph与Mastra：真实产品与公开案例
aliases:
  - Agent框架真实案例
  - LangChain应用案例
  - LangGraph应用案例
  - Mastra应用案例
tags:
  - AI-Agent
  - LangChain
  - LangGraph
  - Mastra
  - 产品案例
  - 技术选型
created: 2026-09-16
updated: 2026-09-16
verified: 2026-09-16
---

# LangChain、LangGraph与Mastra：真实产品与公开案例

## 一句话解释

**这三个框架都有真实产品案例，但通常是某个智能体功能、内部工具或生成出来的应用使用了它们，不是整家公司所有软件都基于同一框架。**

可以关注的名称包括 Flowise、Remote、LinkedIn Hiring Assistant、Klarna AI Assistant、Replit Agent、Salesforce Agentforce Vibes 和 Sanity Content Agent。

**AI = Artificial Intelligence，人工智能**，逐字母读 A-I。这里说的 AI 助手，是应用中的智能体功能，不是模型本身。

核对日期：2026-09-16。本文记录公开资料能够支持的使用范围；历史案例不保证最新版本完全沿用原架构，不将厂商宣传的使用量或效率数字当作独立测评结论。

## 先理解“基于框架”的含义

把一个软件比作商场：支付、会员、客服、库存各有不同系统。客服助手使用 LangGraph，不代表商场里的所有设备、收银系统和网站页面都使用 LangGraph。

看技术案例时，要分清：

- **产品的某项功能使用框架**：例如招聘助手的任务编排。
- **公司内部工具使用框架**：例如员工使用的数据整理工具。
- **平台为用户生成的应用使用框架**：不等于生成应用的平台本身也全部使用它。
- **只是可以连接某款软件**：连接器、教程或合作伙伴标识，不能单独证明那款软件底层使用该框架。

## 真实案例总览

| 相关框架 | 产品或功能 | 实际用途与能够确认的范围 | 主要证据 |
| --- | --- | --- | --- |
| LangChain；公开依赖也包含 LangGraph | Flowise | 可视化搭建智能体和模型工作流；公开代码声明使用 LangChain 相关包 | [官方产品文档](https://docs.flowiseai.com/)与[组件依赖文件](https://github.com/FlowiseAI/Flowise/blob/main/packages/components/package.json) |
| LangChain + LangGraph | Remote 的 Code Execution Agent | 帮助导入新客户的员工与薪资数据，组织工具调用、数据变换和校验流程 | [Remote 工程师撰写的案例，2026-01-19](https://www.langchain.com/blog/customers-remote) |
| LangGraph | LinkedIn Hiring Assistant | 帮招聘人员寻找和评估候选人，进行多步骤任务编排 | [LinkedIn 官方工程文章，2025-09-03](https://www.linkedin.com/blog/engineering/hiring/hiring-assistant-shaped-by-customers-powered-by-ai-innovation) |
| LangGraph | Klarna AI Assistant | 处理支付、退款相关客服问题及请求转交；不是整个支付系统 | [LangChain 官方客户案例，2025-02-12](https://www.langchain.com/blog/customers-klarna) |
| LangGraph | Replit Agent，历史公开案例 | 编程助手的多步骤执行、多智能体协作及人工参与 | [LangChain 的 Replit Agent 架构案例](https://www.langchain.com/breakoutagents/replit) |
| Mastra | Replit Agent 3 的智能体与自动化生成功能 | 根据描述生成并运行 Mastra 智能体与工作流；注意是生成的应用这一层 | [Mastra 的 Replit 客户案例](https://mastra.ai/customers/replit) |
| Mastra | Salesforce Agentforce Vibes 的部分运行路径 | 在案例披露的多模型编程助手中，非 Claude 模型路径使用 Mastra Harness | [Mastra 的 Salesforce 客户案例](https://mastra.ai/customers/salesforce) |
| Mastra | Sanity Content Agent | 在内容管理平台中理解、查询、创建和修改结构化内容 | [Mastra 的 Sanity 客户案例](https://mastra.ai/customers/sanity) |

> [!warning] Flowise 的时间边界
> 本次核对的 GitHub 页面显示，`FlowiseAI/Flowise` 仓库于 2026-08-13 归档为只读。它仍可作为公开代码案例，但不能据此推荐用户直接拿它做新项目；仓库归档也不等于可以推断所有相关服务已经关闭。依赖文件只证明公开版本声明了这些依赖，不证明每个功能都经过 LangGraph。

## LangChain：哪些案例最容易理解

### Flowise：把代码组件变成可视化搭建体验

Flowise 是面向智能体和模型工作流的开发平台，不是面向大众的聊天软件。它的公开组件依赖中可以找到 `langchain`、`@langchain/core` 和 `@langchain/langgraph` 等包。

对初学者而言，这说明：**框架还可以被包进另一款开发工具，让使用者通过界面来组合能力。**公开依赖可以核实组件采用情况，但无法单独证明整个平台的每条执行路线。

来源：[Flowise 官方介绍](https://docs.flowiseai.com/)、[公开依赖文件](https://github.com/FlowiseAI/Flowise/blob/main/packages/components/package.json)。

### Remote：模型决定处理步骤，代码真正整理数据

Remote 是全球雇佣与薪资管理平台。其工程师公开介绍了数据导入环节的 Code Execution Agent（代码执行智能体）：用 LangChain 组织工具调用，让程序处理表格数据，再用 LangGraph 编排步骤与成功、失败、重试路径。

这个案例对应的不是整个 Remote 平台，而是其中的数据迁移与导入能力；也不表示使用框架就能保证数据处理绝不出错。

来源：[Remote 案例](https://www.langchain.com/blog/customers-remote)。

## LangGraph：面向真实用户的助手案例

### LinkedIn Hiring Assistant：招聘助手

LinkedIn 即领英。其 Hiring Assistant（招聘助手）帮助招聘人员处理候选人搜索、评估和多轮沟通等工作。产品方的 2025-09-03 工程文章明确说明使用 LangGraph 进行多步骤编排。

这里能够确认的是招聘助手相关能力，不能扩大成“整个领英网站用 LangGraph 编写”。框架处理的是任务流程，网站的账户、页面、搜索基础设施等仍是另外的组成。

来源：[LinkedIn 官方工程文章](https://www.linkedin.com/blog/engineering/hiring/hiring-assistant-shaped-by-customers-powered-by-ai-innovation)。

### Klarna AI Assistant：客服助手

Klarna 提供支付与购物相关服务。公开案例说明其客服助手使用 LangGraph 路由请求、组织不同处理任务，并使用 LangSmith 检查与评估运行过程。

这个例子说明智能体可以进入具体客服工作流，而不只是回答常识。应当把结论限定在该案例披露的助手上，不能据此断言整个支付业务或最新客服组织方式。

来源：[Klarna 客户案例](https://www.langchain.com/blog/customers-klarna)。

## Mastra：不只是个人演示项目

### Salesforce Agentforce Vibes：多模型编程助手

Salesforce 是企业软件厂商。Agentforce Vibes 是帮助开发者为 Salesforce 平台编写和检查代码的工具。

Mastra 的客户案例披露了两条模型运行路径：Claude 模型使用另一套运行支撑；非 Claude 模型使用基于 Mastra 的 Harness。Salesforce 在此基础上接入自己的模型适配、工具审批和状态保存等能力。

这是“同一产品可以组合不同运行支撑系统”的具体例子。不能扩大成“Salesforce 全部产品都基于 Mastra”，也不能把 Agentforce Vibes 和整个平台的所有 Agentforce 功能混为一谈。

来源：[Salesforce 客户案例](https://mastra.ai/customers/salesforce)。

### Sanity Content Agent：内容管理助手

Sanity 是内容管理平台。**CMS = Content Management System，内容管理系统**，逐字母读 C-M-S，用来管理文章、图片、产品资料等内容。

其 Content Agent（内容智能体）使用 Mastra，在平台的内容结构和权限背景下进行查询、创建及修改。案例还介绍了将改动先放入待审核的变更集合，再由用户确认发布的做法。

这是把模型能力放进真实产品权限与发布流程的例子，不是一个与内容系统脱节的聊天窗口。

来源：[Sanity 客户案例](https://mastra.ai/customers/sanity)。

## 为什么 Replit 会同时出现在 LangGraph 和 Mastra 案例里

**不能看到两个名单就推断它已经整体迁移，或者必然同时把两个框架套在同一条执行链里。**两份公开材料讨论的时间与对象不相同。

1. **LangGraph 的历史案例**讨论的是 Replit Agent 自身如何作为编程助手组织工作。
2. **Mastra 的 Agent 3 案例**重点是 Replit 根据用户描述，生成带有 Mastra 智能体和工作流的应用，并在平台上运行这些应用。

生活类比：一家工厂自己的生产调度软件使用甲技术，它制造出来的设备使用乙技术，这两个事实并不矛盾。

本次资料不足以证明 Replit 最新所有产品的完整技术栈，更不能据此断言“Replit 已经完全从 LangGraph 换成 Mastra”。

来源：[Replit Agent 架构案例](https://www.langchain.com/breakoutagents/replit)、[2024 年生产案例回顾](https://www.langchain.com/blog/top-5-langgraph-agents-in-production-2024)、[Replit Agent 3 与 Mastra 案例](https://mastra.ai/customers/replit)。

## 怎样判断“某个著名产品用了某框架”是否可信

建议依次检查：

1. **是谁说的**：产品工程团队、公开代码，还是框架厂商的客户案例？本文已在链接中区分来源；厂商案例不是独立审计。
2. **用在哪里**：具体产品、某项功能、内部工具，还是平台生成出来的程序？
3. **是哪一天的资料**：旧版本采用过，不等于最新全部版本仍然沿用。
4. **说的是哪个产品名**：使用 LangSmith 做追踪，不自动证明运行流程使用了 LangGraph 或 LangChain。
5. **有没有足够细节**：只有公司标识、招聘要求、连接教程或演示项目，不足以证明底层架构。

客户自己的客户名单也不能继续外推。例如某品牌使用 Sanity，不代表该品牌一定已经使用 Sanity Content Agent，更不能直接认定该品牌的软件基于 Mastra。

本笔记不复述“提升多少倍”“替代多少员工”等宣传指标，也不根据缺少资料就断言某个未列出的软件一定没有使用这些框架。

## 学习建议与关联笔记

把每个案例都拆成四层：**用户看见什么功能 → 模型负责什么 → 框架组织什么 → 工具和业务系统实际做什么。**这样比只背公司名单更有用。

- [[LangChain]]：理解模型组件与工具调用层。
- [[LangGraph：有状态工作流与LangChain的区别]]：理解执行路线、状态与恢复。
- [[Mastra：TypeScript智能体框架与LangChain、LangGraph对比]]：理解整合式框架及比较范围。
- [[Agent Harness：模型之外的运行系统]]：理解上述产品围绕模型补齐了哪些运行能力。
- [[状态机与幂等性]]：理解真实业务为何需要审批、恢复和防止重复执行。

## 资料范围说明

核对日期：2026-09-16。各案例的原始链接已就近标注。名单不是市场份额排名，也不是最新版本的完整技术栈审计；用于回答“有哪些公开可核实的产品采用案例”。
