---
title: Mastra：TypeScript智能体框架与LangChain、LangGraph对比
aliases:
  - Mastra
  - Mastra与LangChain
  - Mastra与LangGraph
tags:
  - AI-Agent
  - Mastra
  - TypeScript
  - LangChain
  - LangGraph
  - 技术选型
created: 2026-09-16
updated: 2026-09-17
verified: 2026-09-16
---

# Mastra：TypeScript智能体框架与LangChain、LangGraph对比

## 一句话解释

**Mastra 是以 TypeScript 为中心的智能体应用开发框架，把智能体、工具、工作流、记忆以及开发管理工具组织在同一套体系中；它与 LangChain、LangGraph 有大量能力重叠，但产品范围和开发方式不完全相同。**

Mastra 读音可近似记为“马斯特拉”，是项目名称，不需要展开成英文缩写。

**TS = TypeScript**，通常逐字母读 T-S，是在 JavaScript 基础上增加类型检查能力的编程语言；**JS = JavaScript**，读 J-S。可先阅读 [[TypeScript与JavaScript]]。[Mastra 官方入门](https://mastra.ai/docs)明确将其定位为 TypeScript 框架。

本笔记核对日期为 2026-09-16。以下“更偏向”“优先考虑”属于基于文档定位和开发需求的判断，不是性能测试结论。

## 先把比较范围摆正

用搭建课程运营系统打比方：

- **LangChain**：提供模型与工具等组件，以及可配置的通用智能体结构。
- **LangGraph**：提供流程控制基础，让你明确安排步骤、分支和状态变化。
- **Mastra**：提供一套整合式开发工具，既有智能体组件，也有工作流、存储接入和可交互管理界面。

因此，将“整个 Mastra”只与“LangGraph 的流程引擎”比较，容易比较失衡。讨论完整开发体验时，通常还要考虑 LangChain、LangGraph 及实际选用的调试、评测和部署工具。

这不意味着“Mastra 严格等于 LangChain 加 LangGraph 加某个平台”。这里只是在对齐职责范围，不表示实现、接口或功能逐项等价。

## Mastra 具体提供什么

### Agent：让模型根据目标选择行动

Agent 指智能体。开发者为它指定模型、行为要求和工具，让模型能够选择调用工具，再根据真实执行结果继续处理任务。

例如课程助手可以查询课表、读取课程说明，再回答学员问题。它仍依赖你提供的数据连接与权限，不会自动访问公司系统。[Mastra Agents](https://mastra.ai/docs/agents/overview)

### Workflow：让开发者规定工作流程

Workflow 是工作流。你可以把业务拆成步骤，并说明每步接收什么数据、返回什么数据、接下来走哪里。

通用概念详解见 [[LangGraph：有状态工作流与LangChain的区别#Agent 的 Workflow 主要做什么|Agent 的 Workflow 主要做什么]]：包括数据传递、分支并行、人工确认、失败处理，以及工作流和 Agent 自主判断怎样配合。这些职责并不限于某一个框架。

Mastra 支持串行、并行、条件分支与循环，也支持在步骤中调用智能体或普通工具。因此不能说“Mastra 只能做简单聊天，复杂流程只能用 LangGraph”。[工作流概览](https://mastra.ai/docs/workflows/overview)、[控制流程说明](https://mastra.ai/docs/workflows/control-flow)

对比两者的常见表达方式：

- LangGraph：强调 State（状态）、Node（节点）、Edge（连接路线）。
- Mastra Workflow：强调 Step（步骤）、输入输出约束及步骤组合；也支持工作流状态。

这是主要开发抽象的差别，不是说 LangGraph 没有数据约束，或 Mastra 没有共享状态。

### Memory、运行记录和评测

Memory 是记忆能力，例如根据配置保存和使用历史对话；它不是重新训练模型，也不是自动拥有无限上下文。

运行记录可以帮助查看调用了什么工具、哪里失败；评测则用测试案例和评分规则检查结果质量。这些能力仍需要配置存储、记录策略和合理的评测标准，不能因为“有评分功能”就认为答案一定正确。[Mastra Memory](https://mastra.ai/docs/memory/overview)、[Studio 功能说明](https://mastra.ai/docs/studio/overview)

### Studio：可交互的开发与管理界面

Studio 可以理解成项目工作台，用来测试智能体、检查工具调用、查看工作流执行情况和管理相关配置。

它不仅能在开发时使用，也有部署和访问控制的配套方案。但“提供 Studio”不意味着自动拥有完整的用户端产品、账户体系和所有业务管理功能。[Mastra Studio](https://mastra.ai/docs/studio/overview)

## 与 LangChain、LangGraph 的核心对照

| 比较点 | Mastra | LangChain | LangGraph |
| --- | --- | --- | --- |
| 主要定位 | TypeScript 智能体应用框架，整合多类开发能力 | 高层模型组件与智能体框架 | 状态化流程编排框架与运行时 |
| 语言路线 | 以 TypeScript 为中心 | 有 Python 与 JavaScript/TypeScript 版本 | 有 Python 与 JavaScript/TypeScript 版本 |
| 常见开发入口 | 定义 Agent、Tool、Workflow，并在项目中注册使用 | 组合模型、工具、中间件和智能体 | 定义状态、节点、连接和运行配置 |
| 复杂流程 | 提供步骤、分支、并行、循环等机制 | 可用现成智能体结构，复杂编排可结合 LangGraph | 直接控制执行结构与状态更新 |
| 暂停与恢复 | 工作流支持暂停、恢复与存储快照 | Agent 利用底层 LangGraph 的相关能力 | 检查点与中断等机制是重要组成 |
| 调试和评测 | 有 Studio、运行追踪与评测配套 | 可以接 LangSmith 或其他工具 | 可以接 LangSmith 或其他工具 |
| 需要承担的工作 | 学习其组件约定，配置工具、存储、权限和部署 | 理解组件与扩展方式，配置运行能力 | 设计更多流程、状态、恢复和副作用处理细节 |

**LangChain 和 LangGraph 并非只能用 Python。**官方均有 [JavaScript/TypeScript 版 LangChain](https://docs.langchain.com/oss/javascript/langchain/overview)与 [JavaScript/TypeScript 版 LangGraph](https://docs.langchain.com/oss/javascript/langgraph/overview)。不能只凭“我的项目使用 TypeScript”就排除它们。

另外，LangChain Agent 构建在 LangGraph 之上；使用 LangChain Agent 时，不一定需要自己编写 LangGraph 图。LangGraph 也可以不依赖 LangChain 使用。Mastra 是另一套可选的应用开发框架，而不是要求再接在这两者后面的必选层。[LangChain 定位](https://docs.langchain.com/oss/python/langchain/overview)、[LangGraph 定位](https://docs.langchain.com/oss/python/langgraph/overview)

## 各自的优势与代价：到底帮你省了什么

下面是根据官方抽象方式做出的工程判断，不是通用难度排行榜；实际难度还取决于团队熟悉的语言和业务需求。

### LangChain：省去从头搭建通用智能体循环的工作

你提供模型、提示词和工具，再按需要添加中间件。中间件可以理解为运行过程中的处理环节，例如限制工具使用、处理错误或调整传给模型的内容。

- **主要优势**：可以先利用现成的模型调用和工具执行结构做出助手，不必一开始就设计全部执行节点。
- **需要承担的工作**：理解消息、工具参数和运行配置；当业务规则越来越具体时，需要判断是在现有结构上扩展，还是直接使用 LangGraph 定制流程。
- **适合的问题**：“我想让一个助手根据用户问题选择查询资料、查询订单等工具，然后回答。”

它不只是“把几个提示词串起来”的工具；目前官方也把它的 Agent 定位为可配置的 Harness，即模型外围的运行支撑结构。[LangChain 官方概览](https://docs.langchain.com/oss/python/langchain/overview)

### LangGraph：省去从零实现状态化流程运行基础的工作

你明确设计状态、节点和连接路线。状态就是任务的进度与已有结果；节点是一步处理；连接路线决定下一步去哪。

- **主要优势**：能更直接地表达固定业务规则与模型自主判断如何结合，例如“未经人工批准，不能进入发布节点”。
- **需要承担的工作**：通常需要设计更多状态字段、节点边界、分支、保存与恢复方式，并测试失败路径。
- **适合的问题**：“任务可能执行很多步、等待人工处理、返回修改，重启后还要继续，我要精细掌握执行过程。”

它的“更底层”指暴露更多控制细节，不是说模型更聪明，或系统天然更稳定。更多控制权也意味着更多设计责任。[LangGraph 官方概览](https://docs.langchain.com/oss/python/langgraph/overview)

### Mastra：省去部分分散组件整合与开发工作台搭建的工作

你在一套 TypeScript 项目约定中组织 Agent、工具、工作流和记忆，并使用 Studio 检查运行情况。

- **主要优势**：智能体能力与开发管理配套集中在同一体系中，适合希望统一项目组织方式的 TypeScript 团队。
- **需要承担的工作**：学习它自己的工具、步骤、存储等接口；确认所需外部服务是否有合适接入方式，没有时仍要编写适配代码。
- **适合的问题**：“我用 TypeScript 开发应用，希望把助手、业务流程和调试工作台一起组织起来。”

它不是 LangGraph 的“简化版”，也不是只能做简单任务。工作流同样有分支、并行、循环与暂停恢复；应比较具体业务表达和运行机制，而不是只数功能名称。[Mastra 工作流](https://mastra.ai/docs/workflows/overview)、[控制流程](https://mastra.ai/docs/workflows/control-flow)、[Studio](https://mastra.ai/docs/studio/overview)

## 同一个课程通知项目，分别怎么做

沿用 [[LangGraph：有状态工作流与LangChain的区别]] 的例子：

> 查询课表 → 生成通知草稿 → 等待讲师审核 → 修改或批准 → 发布已批准的版本。

这是教学设计，不代表正在访问真实课程数据或发布消息。

如果需求只是“查询课程并回答问题”，可以先用 LangChain Agent 或 Mastra Agent 完成。上面的“必须审核后发布”则增加了明确业务约束：需要把审核结果、权限校验和发布条件落实在程序中，而不只是写一句提示词。LangChain 可以利用底层能力加入人工审核；选择直接用 LangGraph，是为了更明确地控制整个业务流程，而不是因为 LangChain 完全不能暂停。

### 用 Mastra

1. 编写“查询课表”和“发布通知”等工具，落实真实访问权限。
2. 配置一个写作 Agent，使用模型生成草稿。
3. 用 Workflow 组织查询、写作、审核和发布步骤。
4. 审核步骤可以暂停；系统接到有效审核结果后，再恢复对应运行。
5. 根据需要使用 Studio 检查输入、工具结果和实际执行路径。

### 用 LangChain 与 LangGraph

1. 编写同样的业务工具，可以利用 LangChain 组织写作助手。
2. 用 LangGraph 定义课表、草稿、审核结果等状态。
3. 把查询、写作、审核和发布安排成节点及连接路线。
4. 配置中断、检查点与恢复方式。
5. 选择调试与评测工具检查运行结果。

两种方案都可以做到。真正要比较的是：现有代码更容易接哪一套、哪个流程表达更清晰、出了错能否查明和恢复，以及团队愿意维护哪一种结构。

## Mastra 的暂停恢复是不是就能保证可靠

不能把“提供恢复机制”理解为“所有操作自动绝不重复”。

Mastra 工作流暂停时可以保存执行快照，并结合配置的存储恢复任务。生产环境仍要确认存储是否持久、能否找到正确运行、恢复数据是否正确，以及失败后的处理方式。[暂停与恢复说明](https://mastra.ai/docs/workflows/suspend-and-resume)

不管选择哪套框架，发布通知、写入订单等真实操作都应考虑 [[状态机与幂等性|幂等性]]，避免因重试或重复请求多执行一次。审核结果也要验证用户权限，并绑定正确的内容版本。

测试时应当故意模拟：工具失败、审核等待、进程重启、重复恢复请求和达到循环上限。不能只测试顺利成功的一条路线。

## TypeScript 框架不等于浏览器前端框架

React 主要用来制作用户界面；Mastra 主要提供智能体应用能力。两者可以合作，而不是互相替代。

典型分工可以是：

```text
React 页面：输入问题、展示回答与审核按钮
    ↓
服务端 Mastra：运行 Agent 和 Workflow、调用工具
    ↓
模型服务、课程数据库及其他业务服务
```

**Node.js** 是让 JavaScript 在浏览器之外运行的环境，读作“Node 点 JS”。Mastra 可以部署到兼容的运行环境，也可以与现有 Web 框架集成，不要求只能使用官方托管平台。[部署说明](https://mastra.ai/docs/deployment/overview)

模型服务密钥和数据库管理凭据不应直接放进公开网页代码。开发工作台也应有访问控制，不应当作普通用户页面无保护地公开。

“框架运行在内网”不代表数据一定留在内网：如果调用外部模型、工具或日志服务，数据仍可能外发。需要检查整条数据路径，而不只是框架名称。参见 [[内网、公网与私有化服务器部署]]。

## 应该怎么选

以下是按需求做出的选型建议，不是绝对排名：

- **主要使用 TypeScript，想在同一体系中组织 Agent、工作流和开发工作台**：Mastra 值得优先做小原型验证；同时可对比 LangChain/Graph 的 TypeScript 版本。
- **主要使用 Python，已有很多 Python 工具或数据处理代码**：先评估 LangChain 与 LangGraph，通常有利于复用现有代码；并非不能通过服务接口使用 Mastra。
- **最关心复杂状态与精细执行结构**：优先仔细研究 LangGraph，同时检查 Mastra 的工作流表达和恢复机制能否满足实际需求，不按“是否支持循环”一项下结论。
- **只想调用一次模型，或业务只有几步普通逻辑**：可以暂时不用这些框架。
- **主要需要业务人员通过界面配置应用**：也可以比较 [[Dify：可视化AI应用、知识库与工作流平台]]，但不要把它与代码框架当成完全相同的产品。

评估时让候选方案完成同一小任务，比较工具正确率、审核约束、故障恢复、调用次数、耗时和维护难度。本文没有执行性能测试，不能据此声称某个框架必然更快、更省钱或更可靠。

### 哪个更快、更省钱、更聪明

不能只看框架名称下结论。实际回答质量还取决于模型、提供的资料、工具质量和流程设计；耗时与费用也会受到模型调用次数、输入输出长度、外部工具耗时、并行安排及存储操作影响。

例如，同一个问题，一套设计调用模型一次，另一套设计调用五次，即使后者框架本身很轻，也不代表总耗时或模型费用更低。这里是影响因素说明，不是对三者做过性能测试。

同样，提供工作流、记忆和调试能力，不等于替你完成用户权限、数据保护、业务数据库、故障监控和上线运维。对前面讨论的直播平台而言，这些框架可以用于课程问答、客服或通知助手；它们不是视频推流、视频分发或支付系统的替代品。

### 初学者怎样学比较顺

1. 先理解“调用模型 → 模型提出工具调用 → 程序执行工具 → 把结果交回模型”的基本循环。
2. 选择一种语言和一个入口：学习 Python 可以先试 LangChain；学习 TypeScript 可以对比 Mastra 与 LangChain 的 TypeScript 版本，选一个完成小助手。
3. 当任务出现分支、等待审核、重启恢复等要求，再深入工作流与状态管理；LangGraph 和 Mastra Workflow 都可以用于学习这些概念。
4. 不必同时学习三套，也不必为了使用框架而把几行普通业务代码变成复杂智能体。

## 从一套框架换到另一套，能直接照搬吗

通常不能把整个项目原样复制后就运行，但不代表业务代码必须全部重写。

- 课表查询、文件处理等独立业务函数，在语言与运行环境兼容时，可能通过适配器复用。
- Agent 配置、工具包装、工作流定义和事件格式通常需要调整。
- 对话记忆、任务快照和检查点不应假定格式兼容；迁移中的任务需要单独设计处理方式。
- 权限、人工审批和防重复逻辑要重新测试，不能只看到“模型能回答”就认为迁移完成。

也可以通过 **API = Application Programming Interface，应用程序编程接口**（逐字母读 A-P-I）让不同语言的服务协作；但同时维护两套编排系统会增加定位故障和恢复任务的复杂度，不应仅为堆叠框架而组合。

## 常见误区与记忆方法

- **Mastra 不是另一个大模型**，仍然要连接实际模型能力。
- **不是“Mastra 只能简单，LangGraph 才能复杂”**：两者都具备复杂流程相关能力，要比较具体机制。
- **不是“TypeScript 就选 Mastra，Python 就只能 LangChain”**：语言是重要条件，但不是唯一条件。
- **有可视化工作台，不等于不用编程就能完成所有定制业务**；同样，也不能说 Mastra 完全没有可视化管理能力。
- **Harness 是通用运行支撑概念**，不是与 Mastra、LangChain、LangGraph 互斥的另一个品牌。

记忆句：**LangChain 偏模型与智能体组件，LangGraph 偏流程与状态运行基础，Mastra 偏 TypeScript 智能体应用的整合式开发框架。**

## 真实产品案例

公开案例包括 Salesforce Agentforce Vibes 的部分模型运行路径、Sanity Content Agent，以及 Replit Agent 3 为用户生成并运行的智能体应用。尤其不能把“生成的应用使用 Mastra”直接等同于“Replit 自身全部基于 Mastra”。来源与边界见 [[LangChain、LangGraph与Mastra：真实产品与公开案例]]。

## 关联笔记与参考资料

先理解 [[Agent Harness：模型之外的运行系统]]、[[LangChain]] 和 [[LangGraph：有状态工作流与LangChain的区别]]，再结合 [[TypeScript与JavaScript]]、[[Node.js与pnpm]] 阅读 Mastra 示例。

核对日期：2026-09-16。以下均为官方文档；部署要求和接口会变化，实际开发时应匹配所安装的版本。

- [Mastra 入门](https://mastra.ai/docs)与 [Agents](https://mastra.ai/docs/agents/overview)：框架定位与智能体能力。
- [Mastra Workflows](https://mastra.ai/docs/workflows/overview)与 [Control Flow](https://mastra.ai/docs/workflows/control-flow)：步骤组织、分支、并行与循环。
- [Mastra Suspend and Resume](https://mastra.ai/docs/workflows/suspend-and-resume)：快照、存储与恢复。
- [Mastra Memory](https://mastra.ai/docs/memory/overview)：记忆组件。
- [Mastra Studio](https://mastra.ai/docs/studio/overview)：开发、管理、追踪与评测界面。
- [Mastra Deployment](https://mastra.ai/docs/deployment/overview)：自部署与托管等选项。
- [LangChain 概览](https://docs.langchain.com/oss/python/langchain/overview)与 [LangGraph 概览](https://docs.langchain.com/oss/python/langgraph/overview)：Agent Harness、编排运行时及两者关系。
- [LangChain JavaScript/TypeScript](https://docs.langchain.com/oss/javascript/langchain/overview)与 [LangGraph JavaScript/TypeScript](https://docs.langchain.com/oss/javascript/langgraph/overview)：语言支持与框架定位。
