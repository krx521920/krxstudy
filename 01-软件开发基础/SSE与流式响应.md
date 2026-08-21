---
title: SSE 与流式响应
aliases:
  - SSE
  - Server-Sent Events
  - 模型流式输出
tags:
  - 网络
  - HTTP
  - SSE
  - 流式响应
created: 2026-08-21
updated: 2026-08-21
verified: 2026-08-21
---

# SSE 与流式响应

> [!summary] 一句话解释
> **SSE（Server-Sent Events，服务器发送事件，读作“艾斯艾斯伊”）是一种让服务器通过一个长期 HTTP 连接不断向浏览器发送文本事件的技术，AI 聊天常用它实现“回答边生成边显示”。**

## 生活类比

普通 HTTP 像去窗口办业务：提交一次申请，等工作人员全部处理完，再拿到完整结果。

SSE 像收听新闻直播：连接建立后，播音员有新内容就继续播，不必每句话重新拨号。

## 普通响应和流式响应

### 普通响应

```text
用户发送问题
  ↓
服务器生成完整答案
  ↓
一次性返回全部内容
```

如果答案生成需要 30 秒，用户可能 30 秒都看不到内容。

### SSE 流式响应

```text
用户发送问题
  ↓
服务器先建立响应
  ↓
发送第1段 → 第2段 → 第3段 → 完成事件
```

用户更早看到首段文字，这叫降低 **Time to First Token（首个 Token 等待时间）**的体感。

## SSE 的数据格式

服务器通常返回：

```http
Content-Type: text/event-stream
Cache-Control: no-cache
```

事件正文可以是：

```text
event: message
data: {"delta":"你好"}

event: message
data: {"delta":"，世界"}

event: done
data: {}

```

空行表示一个事件结束。常见字段包括：

- `data`：事件内容；
- `event`：事件类型；
- `id`：事件编号；
- `retry`：建议的重连等待时间。

## 浏览器怎样接收

标准浏览器 API 是 `EventSource`：

```js
const stream = new EventSource('/events')

stream.onmessage = (event) => {
  console.log(event.data)
}
```

AI API 经常使用 `fetch()` 读取响应流，因为模型请求通常是 POST，而且需要自定义认证头和 JSON 请求体。

## SSE、轮询和 WebSocket 的区别

| 技术 | 方向 | 连接特点 | 常见用途 |
|---|---|---|---|
| 轮询 | 客户端反复问服务器 | 多次普通请求 | 低频状态查询 |
| SSE | 服务器持续推给客户端 | 长期 HTTP 文本流 | 通知、日志、AI 输出 |
| [[TCP、HTTP、HTTPS与WebSocket|WebSocket]] | 双方都可随时发送 | 协议升级后的双向连接 | 实时聊天、协作、游戏 |

如果主要是“客户端发一次请求，服务器持续返回文字”，SSE 往往比 WebSocket 简单。

## AI 流式响应不只是逐字显示

模型流中可能包含：

- 文字增量；
- reasoning/thinking 增量；
- Tool Call 名称；
- Tool Call 参数分片；
- 完成原因；
- Token 用量；
- 错误或拒绝状态。

Tool Call 参数可能被拆成多个片段，程序必须先完整拼接，再解析 JSON，不能把半截参数直接执行。

## 中文分片问题

网络分片不保证刚好落在字符边界或 JSON 边界。程序应该使用增量 UTF-8 解码器和事件解析器，不要假设每次 `read()` 都得到一条完整消息。

## 取消和断线

用户点击“停止生成”时，客户端应该：

1. 取消本地读取；
2. 尽可能中止上游模型请求；
3. 把当前答案标记为未完整结束；
4. 记录是否已经产生费用或工具副作用。

连接断开不代表供应商一定停止计算。网关需要把取消信号传播到上游。

## 重试为什么危险

如果连接在已经收到一半内容后断开，直接重放可能导致：

- 重复计费；
- 生成两个不同答案；
- 重复 Tool Call；
- 重复写文件或发消息。

因此重试要结合 [[状态机与幂等性]]，区分“尚未发送”“正在响应”“已有可见输出”“工具已产生副作用”。

## 常见误区

### 流式能让模型计算更快

流式主要让用户更早看到部分结果，不一定减少模型总计算时间。

### 一个网络分片就是一个 Token

不是。供应商事件、Token、UTF-8 字符和 TCP 分片是不同层级。

### SSE 永远不会断

代理超时、网络变化、服务器重启和浏览器休眠都可能中断连接。

### 收到文字就代表回答完整成功

还要检查完成事件、`finish_reason`、长度截断、内容过滤和错误状态。

## 在 Otto 中的作用

在 [[Otto USB便携智能体]] 和 [[Otto产品总体技术架构]] 中，SSE 用于模型回答的流式展示。运行时还要处理：

- 中文和 JSON 分片；
- Tool Call 分片；
- 用量汇总；
- 取消传播；
- 429/5xx；
- 截断和拒绝；
- 一旦产生可见输出后的安全重试。

## 参考资料

- [WHATWG HTML Standard：Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [MDN：Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- 核对日期：2026-08-21。
