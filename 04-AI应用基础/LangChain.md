---
title: LangChain
aliases:
  - LangChain Framework
tags:
  - AI应用
  - LLM
  - Agent
  - 框架
created: 2026-08-16
updated: 2026-09-16
verified: 2026-08-17
---

# LangChain

> [!warning] 版本变化提示
> LangChain 发展很快，旧教程可能以“Chain（链）”为中心，而截至 2026-08 的官方文档更突出 `create_agent` 和可配置的 Agent Harness。学习时要核对教程对应的版本。

## 一句话解释

**LangChain** 是用于构建大语言模型应用和 Agent 的开源开发框架。它帮助开发者把**模型、提示词、工具、外部数据、状态和中间件**组织到一个可运行的应用中。

它不是大语言模型。LangChain 自己不会凭空生成答案，它要连接 OpenAI、Anthropic、Google、本地模型等模型提供方。

## 为什么会需要 LangChain

最简单的 AI 应用只需要一次模型调用：

```text
用户问题 → 模型 → 回答
```

复杂应用可能需要：

```text
接收问题
→ 判断是否要查资料
→ 调用搜索或数据库工具
→ 把结果放入上下文
→ 调用模型
→ 检查输出格式
→ 记录运行状态
→ 必要时继续下一步
```

如果全部自己编写，需要处理不同模型 API、工具 schema、消息格式、错误、重试、状态和追踪。LangChain 提供了一组通用抽象和集成，减少这些重复工作。

## 当前官方文档中的核心思路

官方把 Agent 简化为：

```text
Agent = Model + Harness
```

- **Model**：负责语言理解和生成。
- **Harness**：围绕模型循环的外部运行系统，包括提示词、工具和影响行为的 middleware（中间件）。具体分工和例子见 [[Agent Harness：模型之外的运行系统]]。

`create_agent` 可以把模型、工具和系统提示词组合起来：

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """查询城市天气。"""
    return f"{city} 今天晴朗"

agent = create_agent(
    model="某个模型",
    tools=[get_weather],
    system_prompt="你是一名耐心的天气助手",
)
```

这只是结构示例。真实天气工具应调用可靠的 [[SDK与API|天气 API]]，不能永远返回固定文字。

## LangChain 常见能力

### 统一模型接口

不同厂商的模型 API 格式不同。LangChain 尝试提供相近的调用方式，方便替换模型或组合多种模型。

### Prompt 与消息组织

将系统规则、用户消息、历史记录和动态数据组合成模型输入。相关概念见 [[Prompt Engineering与Loop Engineering]]。

### Tool Calling（工具调用）

把普通函数或外部服务暴露为模型可以选择调用的工具，例如：

- 查天气；
- 搜索文档；
- 查询数据库；
- 发送邮件；
- 执行某个业务操作。

模型只是决定“调用什么和传什么参数”，真正操作由程序执行。

### Retrieval 与 RAG

可以连接文档加载器、文本切分、Embedding、向量数据库和 Retriever，构建 [[RAG、Naive RAG与GraphRAG|RAG]] 应用。

### Middleware（中间件）

在模型调用或工具调用周围加入日志、权限、重试、限流、人工确认、敏感信息处理等行为。

### Agent

Agent 可以根据当前目标和观察结果决定下一步调用什么工具，而不是完全按照写死的固定步骤执行。

## LangChain、LangGraph、LangSmith 和 Deep Agents

| 名称 | 简化理解 |
|---|---|
| LangChain | 高层组件与可配置 Agent Harness，适合快速组合模型、工具和中间件 |
| LangGraph | 更底层的编排框架与运行时，适合显式状态、持久运行和复杂工作流 |
| LangSmith | 追踪、调试、评估和观察模型/Agent 运行过程的工具 |
| Deep Agents | 在 LangChain 之上提供更多开箱即用能力的 Agent 方案 |

补充核对日期：2026-09-16。LangChain Agent 构建在 LangGraph 之上，借助其持久执行、状态和 human-in-the-loop（人工介入流程）等能力。这不代表 LangChain 的每一项普通模型调用都必须经过一个图，也不代表 LangGraph 必须使用 LangChain 的高层组件。

## LangChain 与 LangGraph 怎么选

**LangChain 更偏“使用现成组件搭建助手”，LangGraph 更偏“亲自设计助手与业务步骤怎样执行”。**两者不是旧版与新版，也不是“链只能直行、图才能循环”。LangChain Agent 本身就能循环使用工具，并支持状态和人工介入等能力。

如果通用的模型—工具循环符合需求，可以先使用 LangChain；如果需要细致设计分支、循环、审核、并行及恢复机制，可以直接使用 LangGraph，也可以把 LangChain 助手放进 LangGraph 的某个步骤。简单的一次模型调用则未必需要任何一个框架。

状态、节点、边的通俗解释，以及课程通知审核的完整例子，统一放在 [[LangGraph：有状态工作流与LangChain的区别]]，避免两篇重复维护全部细节。

如果还在比较 Mastra，见 [[Mastra：TypeScript智能体框架与LangChain、LangGraph对比]]。Mastra 把智能体、工作流及开发管理能力组织在同一套 TypeScript 体系中；LangChain 和 LangGraph 也有 JavaScript/TypeScript 版本，不能按“Python 对 TypeScript”简单区分。

## LangChain 不是什么

- 不是一个模型；
- 不是向量数据库；
- 不是 [[RAG、Naive RAG与GraphRAG|RAG]] 本身；
- 不是调用大模型的必需品；
- 不会自动解决提示词质量、数据质量和幻觉；
- 不是“装上就能得到可靠 Agent”的魔法包。

简单应用直接调用模型 SDK 可能更清楚。只有当组合、状态、工具、切换模型或可观测性带来真实价值时，框架才值得引入。

## LangChain 和普通 SDK 的关系

模型厂商 SDK 主要帮助你调用某一家服务；LangChain 位于更高一层，把不同模型和工具组织成应用。

```text
你的 AI 应用
  ↓
LangChain（组织模型、工具、流程）
  ↓
模型 SDK / Web API
  ↓
模型服务
```

## LangChain 与 Dify 的区别

补充核对日期：2026-09-15。Dify 是带可视化配置、应用发布与运行管理的 AI 应用平台；LangChain 是放进开发者程序中的框架。一个更偏“配置平台已有能力”，另一个更偏“用代码组合组件”，但两者都可以构建知识检索和 Agent 应用。

不要把它们理解为前端和后端、初级版和高级版，或“不会编程只能用 Dify、专业项目只能用 LangChain”。Dify 可以通过工具和接口扩展；LangChain 的灵活性也需要开发者承担实现、测试和维护责任。

详细比较、同一个课程助手的两种实现方式、组合与迁移边界，集中放在 [[Dify：可视化AI应用、知识库与工作流平台#Dify 与 LangChain 的详细区别|Dify 与 LangChain 的详细区别]]，避免重复维护两份完整对照。

## 初学者应该现在学吗

建议先掌握：

1. Python 函数、类、包和虚拟环境；
2. [[SDK与API]]、HTTP 和 JSON；
3. 一次最简单的模型 API 调用；
4. [[Prompt Engineering与Loop Engineering|Prompt Engineering]]；
5. Embedding、向量搜索和 [[RAG、Naive RAG与GraphRAG|基础 RAG]]。

然后再用 LangChain 重新实现一个你已经理解的小项目。这样你会知道框架替你做了什么，而不是只会复制代码。

## 关联概念

- [[Dify：可视化AI应用、知识库与工作流平台|Dify]]：提供可视化配置、应用发布和运行管理；LangChain 更偏代码框架，两者都能组织模型应用，但不是同一种产品。
- [[MCP模型上下文协议]]：MCP 负责 Host 与外部资料/工具程序之间的标准通信；LangChain 负责在应用内部组织模型、状态、工具和 Agent 流程，两者位于不同层次。
- [[SDK与API]]：LangChain 常通过模型 SDK 或 Web API 访问模型服务。
- [[Prompt Engineering与Loop Engineering]]：LangChain 可承载 Prompt 和 Agent loop，但不会自动保证循环可靠。
- [[RAG、Naive RAG与GraphRAG]]：LangChain 提供构建检索流程的组件，RAG 是具体方法。

## 参考资料

- [LangChain 官方文档：Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph 官方文档：Overview](https://docs.langchain.com/oss/python/langgraph/overview)：2026-09-16 补充核对两者关系。
- [LangChain 官方文档：Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)
