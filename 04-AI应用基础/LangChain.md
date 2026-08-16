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
updated: 2026-08-16
verified: 2026-08-16
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
- **Harness**：围绕模型循环的外部运行系统，包括提示词、工具和影响行为的 middleware（中间件）。

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
| LangGraph | 更底层的编排框架，适合显式状态、持久运行和复杂工作流 |
| LangSmith | 追踪、调试、评估和观察模型/Agent 运行过程的工具 |
| Deep Agents | 在 LangChain 之上提供更多开箱即用能力的 Agent 方案 |

截至 2026-08，LangChain Agent 构建在 LangGraph 之上，借助其持久执行、状态和 human-in-the-loop 等能力。

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

## 初学者应该现在学吗

建议先掌握：

1. Python 函数、类、包和虚拟环境；
2. [[SDK与API]]、HTTP 和 JSON；
3. 一次最简单的模型 API 调用；
4. [[Prompt Engineering与Loop Engineering|Prompt Engineering]]；
5. Embedding、向量搜索和 [[RAG、Naive RAG与GraphRAG|基础 RAG]]。

然后再用 LangChain 重新实现一个你已经理解的小项目。这样你会知道框架替你做了什么，而不是只会复制代码。

## 参考资料

- [LangChain 官方文档：Overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain 官方文档：Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)
