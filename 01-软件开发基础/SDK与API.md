---
title: SDK 与 API
aliases:
  - SDK
  - API
tags:
  - 软件开发基础
  - 接口
created: 2026-08-16
updated: 2026-08-17
---

# SDK 与 API

## 一句话解释

- **API（Application Programming Interface，应用程序编程接口）**：一个软件公开给其他软件使用的“办事窗口和规则”。
- **SDK（Software Development Kit，软件开发工具包）**：为了在某个平台或服务上开发程序而准备的一整套工具箱，其中通常包含 API 的封装。

## 先用生活类比理解

把一家餐厅想成一个软件服务：

- **API 像点餐规则和服务窗口**：菜单上写着能点什么、需要提供什么信息、最后会得到什么。
- **SDK 像餐厅发给合作方的开店工具箱**：不仅有菜单，还可能有现成设备、操作手册、示例、调试工具和培训资料。

因此，API 重点是“**怎样和我交流**”，SDK 重点是“**我给你哪些东西，帮助你开发**”。

## API 到底是什么

API 是一份由程序执行的约定。它通常规定：

1. 可以请求哪些功能。
2. 请求时需要传入什么数据。
3. 数据采用什么格式。
4. 成功会返回什么。
5. 失败时如何表示错误。
6. 是否需要身份认证、是否有限流。

API 不一定经过互联网，常见类型包括：

- **库 API**：例如 Python 字符串的 `upper()` 方法。
- **操作系统 API**：例如程序向 Windows 请求打开文件。
- **浏览器 API**：例如定位、摄像头、剪贴板 API。
- **Web API**：通过 HTTP 请求远程服务器，是日常最常听到的 API。

### 一个 Web API 请求例子

假设天气服务提供：

```text
GET https://weather.example.com/current?city=Shanghai
```

可以把它拆成：

- `GET`：请求方法，表示读取数据。
- `/current`：接口地址的一部分，也叫 endpoint（端点）。
- `city=Shanghai`：参数，告诉服务要查上海。
- 返回值：通常是 JSON，例如 `{"temperature": 30}`。
- 状态码：如 `200` 表示成功，`404` 表示资源没找到，`401` 表示没有通过身份认证。

> [!warning] API Key 不是普通参数
> API Key 常用于证明调用者身份，应像密码一样保护，不能直接写进公开的 GitHub 仓库或前端代码。

## SDK 里通常有什么

不同 SDK 内容不同，但常见组成有：

- 编程语言库或 API 封装；
- 类型定义；
- 文档和教程；
- 示例代码；
- 编译器、调试器或模拟器；
- 测试、打包和部署工具；
- 身份认证、重试、错误处理等通用逻辑。

例如，同样调用天气 API：

```python
# 直接调用 Web API：需要自己拼 URL、发送请求、解析 JSON
response = requests.get(url, params={"city": "Shanghai"})
temperature = response.json()["temperature"]

# 假想的天气 SDK：细节由 SDK 帮忙处理
temperature = weather_sdk.current(city="Shanghai").temperature
```

SDK 并没有创造新的天气数据，它只是让已有 API 更容易、安全、一致地被某种语言调用。

## SDK、API、库和框架的区别

| 概念 | 核心问题 | 典型内容 |
|---|---|---|
| API | 别的软件怎样调用我？ | 方法、参数、数据格式、返回值、错误规则 |
| SDK | 怎样更方便地为某平台开发？ | 库、API 封装、文档、示例、调试和构建工具 |
| Library（库） | 哪些现成代码可以直接调用？ | 函数、类、模块 |
| Framework（框架） | 整个应用应该按什么结构运行？ | 生命周期、目录结构、扩展点和大量通用功能 |

一个 SDK 可以包含多个库，也可以包含对 API 的封装；SDK 中甚至可能带一个框架。

## 常见误区

### “API 就是一个网址”

不完全正确。Web API 的 URL 只是接口约定的一部分，完整 API 还包括方法、参数、认证、返回格式和错误规则。

### “安装了 SDK 就不需要理解 API”

也不正确。SDK 简化了调用，但排查错误时仍要理解底层 API，例如限流、权限和返回字段。

### “SDK 越大越好”

不一定。大型 SDK 可能增加安装体积、依赖冲突和升级成本。简单需求有时直接调用 HTTP API 更清楚。

## 和其他笔记的关系

- [[MCP模型上下文协议]] 规定 AI Host 怎样发现和调用外部 Resources、Prompts 与 Tools；MCP Server 常在内部继续调用具体业务 API。
- [[LangChain]] 本身可以看作构建 AI 应用的一组框架与库，也会调用不同模型厂商的 API。
- [[Django]] 可以用来开发自己的 Web API。
- [[DeepSeek Harness、Everything is a Plugin与Cordis]] 中，插件可以通过稳定接口向系统提供能力。

## 建议掌握到什么程度

初学阶段不必背诵所有 HTTP 状态码。先做到：

1. 能用一句话区分 API 和 SDK。
2. 看懂一次简单的“请求 → 响应”。
3. 知道 API Key 需要保密。
4. 遇到 SDK 报错时，知道可以去查它封装的原始 API 文档。

## 参考资料

- [MDN：API 术语解释](https://developer.mozilla.org/en-US/docs/Glossary/API)
- [AWS：What is an SDK?](https://aws.amazon.com/what-is/sdk/)
