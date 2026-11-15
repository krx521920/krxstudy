---
title: AI产品全景清单：办公、智能体、编程、研究与创作
aliases: [AI产品大全, AI工具全景, AI产品汇总, AI办公产品目录]
tags: [AI产品, 市场调研, 工具选型, MOC]
created: 2026-11-15
updated: 2026-11-15
verified: 2026-11-15
---

# AI产品全景清单：办公、智能体、编程、研究与创作

> [!summary] 一句话结论
> **AI 产品可以按“聊天理解、查资料、执行任务、办公协作、开发软件、创作内容、搭建系统”来认识。**本次联网整理 **112 条产品/产品家族/功能入口**，分成 12 类，并单列停运和迁移信息；同一公司的模型、客户端与功能模式不应混为一谈。

## 范围、日期与读法

- 调研与核对日期：**2026-11-15**。优先读取官方产品页、帮助文档、发布说明和官方代码仓库。
- “稍有名气”没有统一统计标准；本页是覆盖国内外常见产品的代表性目录，不是全球穷尽名录、使用量排行榜或效果排名。
- **112 是目录条目数，不是 112 家公司，也不代表 112 个均可立即注册的独立产品。**例如 Claude 与 Cowork、Perplexity 与 Computer/Comet 有家族或功能关系；Atlas 标为历史产品。另附 Sora、QClaw、Gemini Code Assist 三组历史/迁移提醒。
- 每行产品名都是官方来源或官方入口链接。“主要用途”依据公开资料归纳；“场景与边界”包含本笔记的使用判断，没有把厂商宣传的第一、最强、提效倍数当成实测成绩。
- 本次没有注册账号、购买套餐或逐款操作。动态页面只确认到入口时已注明；具体开放地区、操作系统、额度、价格和企业版本，要以使用当天账户及官方条款为准。
- AI = Artificial Intelligence，人工智能，读 A-I；Agent = 智能体，指围绕目标调用工具执行任务的系统。前置知识见 [[Agent Harness：模型之外的运行系统]]。

你最初提到的 **QuWork** 仍未锁定准确名称，可能对应 QoderWork 或 QwenWork；这里将两者分别收录，不直接认定为某一款。Muse 按 **Meta Muse**、dot 按 **OpenAI dot** 整理。重点比较见 [[AI办公智能体对比：QoderWork、千问办公、WorkBuddy、Muse、dot与Manus]]。

## 先按需求定位

| 你想完成的事情 | 先看哪一类 | 举例 |
|---|---|---|
| 学习概念、讨论想法、写一段文字 | 通用助手 | ChatGPT、Claude、Gemini、DeepSeek、豆包、千问、Kimi |
| 交代目标后，让它自己处理多个步骤 | 通用执行型 Agent | WorkBuddy、千问办公、Manus、dot、Muse、Genspark |
| 查有出处的资料、读论文和自己的文件 | 搜索研究 | Perplexity、秘塔、Gemini Notebook、Elicit |
| 在邮件、会议、文档和团队资料中工作 | 办公协作 | Copilot、Workspace Gemini、WPS、飞书、Notion |
| 写代码或搭建网站 | 编程与应用搭建 | Codex、Claude Code、Cursor、Qoder、Replit、Lovable |
| 做课件、海报、图片、短视频、配音 | 创作工具 | Gamma、Canva、即梦、Runway、ElevenLabs |
| 搭一个长期复用的业务助手 | 工作流与企业平台 | 扣子、Dify、n8n、Copilot Studio |
| 自己接模型或部署资料问答 | 本地与自托管 | Ollama、LM Studio、Open WebUI、AnythingLLM |

分类按主要用途，不代表产品只能做这一类事情。比如 Kimi 有 Agent 入口，Codex 也能处理文件，Canva 也能制作视频。

## 一、通用对话与综合助手（15 条）

适合学习问答、写作、资料分析和日常咨询。现在不少产品也能执行任务，但具体权限和工具取决于所用模式。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 001 | [ChatGPT](https://chatgpt.com/overview/) | OpenAI | 对话、研究、文件分析、图文和办公产物 | 学习问题、分析上传资料、准备报告；Work 与 Codex 是不同任务入口 |
| 002 | [Claude](https://claude.com/product/overview) | Anthropic | 对话、文档分析、写作及跨文件工作 | Cowork 能力正并入 Claude；Claude Code 仍有编程任务定位 |
| 003 | [Gemini](https://gemini.google/overview/) | Google | 多模态问答、研究和 Google 应用协作 | 个人 Gemini、Workspace 内能力和 Spark 的入口/权益需分别看 |
| 004 | [DeepSeek](https://www.deepseek.com/) | 深度求索 | 推理问答、写作和代码辅助 | 聊天应用、API 服务、Harness 是不同层次 |
| 005 | [豆包](https://www.doubao.com/) | 字节跳动 | 面向大众的综合 AI 助手 | 适合中文日常使用；本次官网为动态页面，未核验每个账号的功能列表 |
| 006 | [千问](https://www.qianwen.com/) | 阿里巴巴 | 面向用户的综合 AI 助手 | 千问应用、Qwen 模型和千问办公不能当成同一件东西 |
| 007 | [Kimi](https://www.kimi.com/) | 月之暗面 | 问答、资料处理与 Agent 任务入口 | 看当前选用的是聊天还是任务模式，交付物也需检查 |
| 008 | [腾讯元宝](https://yuanbao.tencent.com/) | 腾讯 | 问答、搜索与内容创作 | 个人助手入口；企业办公场景另看 WorkBuddy |
| 009 | [百度文心（历史名称：文心一言、文小言）](https://wenxin.baidu.com/) | 百度 | 办公学习助手 | 旧 yiyan 地址跳转至 wenxin；旧名作为检索别名，不重复计为三款 |
| 010 | [智谱清言](https://chatglm.cn/) | 智谱 | 对话助手入口 | 已核到官方入口；页面动态加载，详细功能与权益以登录后展示为准 |
| 011 | [讯飞星火](https://xinghuo.xfyun.cn/doc/) | 科大讯飞 | 问答、写作、语音交互及场景助手 | 与讯飞听见的录音转写定位不同 |
| 012 | [Grok](https://docs.x.ai/grok/overview) | Grok 团队（官方文档现标 SpaceXSI） | 对话、研究及关联工具入口 | 旧资料常写 xAI；这里按当前官方文档记录，不展开公司沿革 |
| 013 | [Meta AI](https://ai.meta.com/meta-ai) | Meta | 对话、图像及社交应用中的助手 | 与拥有独立执行环境的 Muse 分开理解 |
| 014 | [Mistral Vibe（原 Le Chat 入口）](https://mistral.ai/products/vibe/) | Mistral | 对话、研究、知识与工具协作 | 原 Le Chat 官网已跳转 Vibe，现定位覆盖长任务与代码 |
| 015 | [Poe](https://poe.com/) | Poe | 多模型对话与机器人聚合 | 一个界面访问多种模型；不是一个自研模型的名称 |

## 二、通用执行型 Agent 与桌面办公（19 条）

Agent（智能体，近似读“诶简特”）接收目标后规划步骤、调用工具并交付结果。这一组最接近你举出的产品。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 016 | [QoderWork](https://docs.qoder.com/zh/qoderwork/introduction) | Qoder | 文件整理、数据处理、文档和浏览器/桌面任务 | QoderWork CN 已公布迁移安排；具体见后文状态表 |
| 017 | [千问办公 QwenWork](https://docs.qwenwork.cn/product-introduction) | 阿里巴巴/钉钉体系 | 文档、表格、演示、网页和企业办公协作 | 与 QoderWork 名称接近，但不能直接混写；区分个人与企业版本 |
| 018 | [WorkBuddy](https://cloud.tencent.com/product/workbuddy) | 腾讯 | 可执行任务的综合办公工作台 | 文件处理、研究和协作；还存在单独的企业版入口 |
| 019 | [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | Meta | 持续处理个人任务和跨应用事务 | 按 Meta 的个人智能体版本整理；同名模型/其他产品不混入 |
| 020 | [dot / dots](https://openai.com/index/introducing-dots/) | OpenAI | 有独立云端电脑的常驻智能体 | 持续推进任务、使用已授权应用；开放受套餐和地区等条件影响 |
| 021 | [Manus](https://manus.im/) | Manus | 多步骤任务、研究、演示、网站和创作 | 适合按成果交办研究和制作任务；多步骤执行结果仍需验收 |
| 022 | [Claude Cowork](https://claude.com/product/cowork) | Anthropic | 跨文件和工具完成知识工作 | 官网已说明能力并入 Claude；此行是功能入口，不是另一家模型公司 |
| 023 | [Gemini Spark](https://support.google.com/gemini/answer/17094507?hl=en) | Google | 持续任务、计划与已连接应用工作流 | 是 Gemini 体系中的 Agent 能力，需核对账号开放范围 |
| 024 | [Genspark](https://www.genspark.ai/) | Genspark | 研究、文档、表格、演示和创作工作台 | 多种任务入口组合；不要把官网效率案例当成自己的必达速度 |
| 025 | [Skywork / 天工](https://skywork.ai/home_agent/ai-docs) | Skywork | 研究和文档、演示、表格等产物 | 已核到官方文档生成产品页；本次首页抓取超时 |
| 026 | [MiniMax Code / MiniMax Agent](https://agent.minimax.io/download) | MiniMax | 编程、办公文件和浏览器工作 | 当前入口主打 MiniMax Code，官方仍解释桌面 Code 与网页 Agent 的关系 |
| 027 | [阶跃 AI 桌面伙伴](https://chat.stepfun.com/download) | 阶跃星辰 | 电脑操作、文件管理、信息收集和定时任务 | 桌面执行能力与聊天模型本身分开看 |
| 028 | [OpenClaw](https://docs.openclaw.ai/help/faq/what-is-openclaw) | OpenClaw 项目 | 在自有基础设施运行的个人/团队助手 | 需自行配置模型、消息渠道和权限；自托管不自动等于本地推理 |
| 029 | [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | 带记忆和技能积累的可部署智能体 | 与 React Native 的 Hermes 引擎不是同一项目 |
| 030 | [DeepSeek Harness](https://www.deepseek.com/harness/) | 深度求索 | 可组合插件的工作、代码与研究运行系统 | 官方提供开源项目及桌面预览版；不同于 DeepSeek 聊天网页 |
| 031 | [Perplexity Computer](https://www.perplexity.ai/personal-computer) | Perplexity | 研究、工具编排和多步骤工作 | 云端 Computer、Mac 上 Personal Computer 与 Comet 浏览器各有职责 |
| 032 | [QoderWake](https://qoder.com/en/blog/qoderwake) | Qoder | 持续推进工作的 AI 员工产品 | 与 Qoder 编程工作台、QoderWork 的名称和使用入口分开 |
| 033 | [纳米 work（纳米 AI 升级入口）](https://bbs.360.cn/thread-16187876-1-1.html) | 360 | 云端办公任务与产物交付 | n.cn 已跳转 work.n.cn；官方社区有产品定位，页面细节本次不可完整读取 |
| 034 | [WPS 灵犀](https://lingxi.cn/) | 金山办公 | 围绕 Word、Excel、PPT 成品的办公助手 | 与 WPS 内嵌 AI 功能相关，但有独立产品入口 |

## 三、搜索、研究与资料学习（8 条）

这一组更适合“有来源地找信息”和“读懂自己的资料”。有引用不等于结论自动正确，仍要看来源能否支持结论。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 035 | [Perplexity](https://www.perplexity.ai/en-GB/hub/getting-started) | Perplexity | 联网回答与研究 | 适合带来源的专题调查；与旗下 Computer/Comet 分工不同 |
| 036 | [秘塔 AI 搜索](https://metaso.cn/) | 秘塔 | 中文 AI 搜索 | 适合搜资料与整理线索；引用原文仍需回看 |
| 037 | [Felo](https://felo.ai/search) | Felo | 多语言搜索、理解与内容生成 | 适合跨语言找资料、形成初稿 |
| 038 | [Gemini Notebook（旧名 NotebookLM）](https://notebook.google/) | Google | 基于提供资料的阅读、问答和知识整理 | 旧 notebooklm.google 入口现跳转 notebook.google；保留旧名便于搜索 |
| 039 | [Elicit](https://elicit.com/) | Elicit | 科学文献搜索、提取与研究工作 | 适合文献表格与证据整理，不能替代对研究方法和原文的判断 |
| 040 | [Consensus](https://consensus.app/) | Consensus | 科研问答与证据搜索 | 学术资料方向；本次首页动态加载，细项权益未逐项核验 |
| 041 | [SciSpace](https://scispace.com/) | SciSpace | 论文搜索、阅读、综述与研究产物 | 生成综述前检查引用是否真实、是否读到了相应内容 |
| 042 | [You.com](https://you.com/) | You.com | AI 搜索、研究与推理基础设施 | 当前官网偏 API/企业基础设施，不按旧聊天搜索首页来介绍 |

## 四、AI 浏览器与浏览入口（3 条）

浏览器是打开网页的工具；加入 AI 后可以理解页面、组织标签页或执行网页任务。它与底层大模型不是同一层。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 043 | [Comet](https://www.perplexity.ai/comet) | Perplexity | 带个人 AI 助手的浏览器 | 适合网页研究和网页流程；使用账号权限时需要知道它能访问什么 |
| 044 | [ChatGPT Atlas【已弃用】](https://openai.com/index/introducing-chatgpt-atlas/) | OpenAI | ChatGPT 体系的浏览器入口 | 官方发布页已标记 deprecated；仅保留历史识别，不作为当前浏览器推荐 |
| 045 | [夸克](https://www.quark.cn/) | 阿里巴巴 | AI 浏览器、搜索、文件处理与网盘相关能力 | 适合中文检索和资料处理；搜索与文件功能可能走不同计费入口 |

## 五、办公套件、企业协作与会议（13 条）

这些能力往往嵌在既有办公系统中。企业本来用什么文档、邮件和会议系统，通常会直接影响接入成本。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 046 | [Microsoft Copilot / Microsoft 365 办公入口](https://www.microsoft.com/en-us/copilot) | 微软 | 工作资料、办公应用与 AI 产物协作 | 个人 Copilot、组织授权与 Copilot Studio 的权益不能混为一谈 |
| 047 | [Google Workspace with Gemini](https://workspace.google.com/solutions/ai/) | Google | 邮件、文档、表格、会议等工作流中的 AI | 与个人 Gemini App 分开核对组织授权和数据范围 |
| 048 | [WPS AI](https://ai.wps.cn/) | 金山办公 | 文档写作、PPT 与表格处理 | 适合 Office 文件工作；需检查生成结果是否保留可编辑结构 |
| 049 | [飞书 AI / aily](https://www.feishu.cn/content/article/7621764358124604369) | 飞书 | 企业资料、协作与智能体 | 与飞书已有文档、消息和业务权限一起评估 |
| 050 | [钉钉 AI](https://www.dingtalk.com/) | 钉钉 | AI 融入企业工作平台 | 钉钉是工作平台，千问办公是相关办公产品，不能完全画等号 |
| 051 | [Notion AI](https://www.notion.com/product/ai) | Notion | 笔记、搜索、会议和工作区 Agent | 适合已有 Notion 资料的团队，授权范围决定它能看到什么 |
| 052 | [ClickUp Brain](https://clickup.com/brain) | ClickUp | 项目、任务和团队资料上的 AI | 适合把任务上下文接到 AI；当前官网使用 Brain² 等品牌表述 |
| 053 | [Slack AI](https://slack.com/features/ai) | Slack | 消息摘要、搜索和工作协作 | 效果依赖工作区资料、索引和访问权限 |
| 054 | [ZoomMate / Zoom AI Companion 相关入口](https://www.zoom.com/en/products/ai-assistant/) | Zoom | 会议与工作助手 | 旧 AI assistant 产品地址当前展示 ZoomMate，按现有入口核对权益 |
| 055 | [腾讯会议 AI 小助手 Pro](https://meeting.tencent.com/ai/) | 腾讯会议 | 会议总结、问答、提醒和关键信息提取 | 会议内容识别、参会者归属和待办负责人要复核 |
| 056 | [Otter](https://otter.ai/) | Otter.ai | 会议转写、笔记与会议信息问答 | 先核对会议语言和采集方式是否适合实际会议 |
| 057 | [Granola](https://www.granola.ai/) | Granola | 结合会议内容整理笔记 | 适合连续开会后的要点沉淀和查询 |
| 058 | [讯飞听见](https://www.iflyrec.com/) | 科大讯飞 | 录音转写、纪要和语音翻译 | 适合中文录音整理；转写准确率随噪声、口音和专业词变化 |

## 六、编程与应用搭建（14 条）

IDE = Integrated Development Environment，集成开发环境，读 I-D-E；CLI = Command-Line Interface，命令行界面，读 C-L-I。这些是产品交互方式，不能直接代表智能程度。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 059 | [Codex](https://openai.com/codex/) | OpenAI | 理解仓库、修改代码、测试与代码审查 | 适合软件开发和已有仓库工作；模型与 Codex 产品分开看 |
| 060 | [Claude Code](https://claude.com/product/claude-code) | Anthropic | 编程智能体与开发工作流 | 适合仓库理解、修改和验证，不仅是回答代码问题 |
| 061 | [Cursor](https://cursor.com/) | Cursor | AI 编程工作台与 Agent | 适合在项目上下文中迭代软件 |
| 062 | [GitHub Copilot](https://github.com/features/copilot) | GitHub | 与开发和 GitHub 协作结合的编程助手/Agent | 不要与 Microsoft 365 办公 Copilot 混淆 |
| 063 | [Devin Desktop（Windsurf 旧入口）](https://devin.ai/desktop) | Devin | 桌面编程工作台 | windsurf.com 当前跳转 Devin Desktop；保留旧名称供对照 |
| 064 | [TRAE](https://www.trae.ai/) | TRAE | AI 开发工具及工作入口 | 国内与国际站版本/权益分别核对；本次国内站抓取超时 |
| 065 | [Qoder](https://qoder.com/) | Qoder | 编程 Agent、桌面和 IDE/CLI 等入口 | 与 QoderWork、QoderWake 是同一体系中的不同入口 |
| 066 | [CodeBuddy](https://www.codebuddy.cn/) | 腾讯 | 智能编程伙伴 | 与偏办公任务的 WorkBuddy 分开理解 |
| 067 | [通义灵码](https://lingma.aliyun.com/lingma) | 阿里云 | 编码、工程理解、终端与开发辅助 | 使用 IDE/插件等形态时需核对项目和编辑器兼容性 |
| 068 | [Antigravity](https://antigravity.google/) | Google | 编程 Agent 与项目工作台 | Google 已引导部分旧 Code Assist/CLI 用户迁移，见状态表 |
| 069 | [Replit](https://replit.com/) | Replit | 用自然语言构建并运行应用 | 原型容易生成，业务正确性和线上运维仍需验证 |
| 070 | [Lovable](https://lovable.dev/) | Lovable | 应用与网站搭建 | 适合快速验证想法，接数据库和真实支付后需单独验收 |
| 071 | [Bolt](https://bolt.new/) | Bolt | 对话生成网站、应用与原型 | 看代码导出、托管、外部集成和后续维护方式 |
| 072 | [v0](https://v0.app/) | Vercel | 网页界面、全栈应用与部署协作 | 适合 Web 产物，发布前检查权限和数据处理 |

## 七、演示、设计与图像（10 条）

PPT 常用来指演示文稿。本类主要交付可视化内容，质量不只看第一张图，还要看文字、风格、可编辑性和导出结果。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 073 | [Gamma](https://gamma.app/) | Gamma | 演示文稿、文档和网站表达 | 适合把内容组织成视觉叙事，导出后仍应检查排版 |
| 074 | [AiPPT](https://www.aippt.cn/) | AiPPT | 根据主题或资料生成演示文稿 | 区分大纲正确、版式漂亮和文件可继续编辑三件事 |
| 075 | [Canva AI / 可画相关入口](https://www.canva.com/ai/) | Canva | 设计、演示、图像和营销素材 | 国内外服务及模板/素材权益需分别确认 |
| 076 | [Adobe Firefly](https://www.adobe.com/products/firefly.html) | Adobe | 生成式图像、视频与创意工作流 | 与 Adobe 编辑工具结合；商用条款按模型与素材分别看 |
| 077 | [Midjourney](https://www.midjourney.com/) | Midjourney | 视觉图像创作 | 适合风格探索与概念图；生成图不等于真实产品照片 |
| 078 | [Krea](https://www.krea.ai/) | Krea | 图像、视频、增强与 3D 创作工作台 | 是多项创作能力的平台，不只是一个生图模型 |
| 079 | [Ideogram](https://ideogram.ai/) | Ideogram | 图像设计与视觉工作流 | 官网已拓展 Creative、API、Agents 等入口 |
| 080 | [Figma AI / Make 相关能力](https://www.figma.com/ai/) | Figma | 界面设计、图表和可交互原型 | 设计稿、代码原型和真正上线的系统仍是不同交付阶段 |
| 081 | [稿定 AI](https://www.gaoding.com/ai) | 稿定 | 海报、图片、文案与营销设计 | 适合中文营销素材；本次读取到的页面缓存较旧，具体功能复核 |
| 082 | [美图设计室 / Designkit](https://www.designkit.cn/help/143) | 美图 | 电商、社媒海报与营销视频 | 官方帮助中心列出国内 designkit.cn 与海外 designkit.com，权益按版本核对 |

## 八、视频生成与剪辑（7 条）

文生视频、图生视频和剪辑工具可以配合，但“生成一段镜头”与“交付完整课程视频”工作量不同。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 083 | [Runway](https://runway.com/) | Runway | 视频与视觉创作平台 | 原 runwayml.com 当前跳转 runway.com，官网也有开发与其他产品线 |
| 084 | [可灵 AI / Kling](https://docs.qingque.cn/d/home/eZQDKi7uTmtUr3iXnALzw6vxp?identityId=1oE1iQt0sbr) | 快手 | 视频生成与创作 | 官网抓取受限，能力定位参考官方使用指南，不承诺当前模型/额度 |
| 085 | [即梦 AI](https://jimeng.jianying.com/) | 即梦 | 中文图像、视频和智能画布创作 | 适合中文创意内容；不同生成入口费用可能不同 |
| 086 | [海螺 AI / Hailuo](https://hailuoai.video/) | MiniMax | 视频创作 | 与 MiniMax Code 的办公/编程入口不同 |
| 087 | [Pika](https://pika.art/) | Pika | 视频、图像和音频创意工具 | 适合创意片段与视觉效果，实际结果需逐镜头检查 |
| 088 | [Google Flow](https://flow.google.com/) | Google | 图像与视频创作工作室 | 产品是 Flow，具体底层模型名称不是同一层 |
| 089 | [CapCut / 剪映相关产品](https://www.capcut.com/) | CapCut | 剪辑、字幕及 AI 视频工具 | 国内剪映与国际 CapCut 功能、素材和账号权益可能不同 |

## 九、语音、音乐与数字人（6 条）

ASR = Automatic Speech Recognition，自动语音识别；TTS = Text-to-Speech，文本转语音，均按字母读。音乐生成和数字人视频则是另外的输出形态。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 090 | [ElevenLabs](https://elevenlabs.io/) | ElevenLabs | 语音生成、配音、声音 Agent 与音频创作 | 配音、客服语音和声音克隆分别涉及不同配置与授权 |
| 091 | [Suno](https://suno.com/) | Suno | 歌曲与音乐创作 | 适合音乐草稿和创作；商业使用以当前套餐及条款为准 |
| 092 | [Udio](https://www.udio.com/) | Udio | AI 音乐生成 | 已确认官方入口；本次动态首页不足以核实下载和商用权益 |
| 093 | [Descript](https://www.descript.com/) | Descript | 按文字编辑音视频、转写和 AI 剪辑 | 适合播客、采访和讲解视频的编辑流程 |
| 094 | [HeyGen](https://www.heygen.com/) | HeyGen | 数字人、视频翻译与人物视频 | 涉及真人形象/声音时要有相应授权 |
| 095 | [Synthesia](https://www.synthesia.io/) | Synthesia | 企业培训和讲解型数字人视频 | 适合知识讲解与培训素材，内容和人物呈现仍需审核 |

## 十、翻译、写作与营销（3 条）

专门工具的价值常在术语、文风、模板和组织工作流，而不仅是能否写出一段文字。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 096 | [DeepL](https://www.deepl.com/en) | DeepL | 文本/文档翻译、写作和语音相关能力 | 术语、数字、专有名词和文档排版需要复核 |
| 097 | [Grammarly](https://www.grammarly.com/) | Grammarly | 英文写作、改写、语气和校对 | 更适合语言表达工作；不代表事实核查自动完成 |
| 098 | [Jasper](https://www.jasper.ai/) | Jasper | 品牌内容与营销 Agent 工作流 | 适合营销团队统一风格和流程，仍要核验广告事实 |

## 十一、搭建工作流、企业知识与客服（9 条）

这组通常需要配置数据、流程和权限。用户是在搭建可复用的系统，而不只是给现成助手提一个问题。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 099 | [扣子 / Coze](https://docs.coze.cn/) | 扣子 | 办公创作、Agent 团队与编程/工作流能力 | 当前已超出旧“拖节点搭机器人”定位；Coze Studio 开源项目另看已有笔记 |
| 100 | [Dify](https://dify.ai/) | Dify | AI 应用、知识库和可管理工作流 | 适合构建自己的业务 AI，需有人维护数据、接口和部署 |
| 101 | [n8n](https://n8n.io/) | n8n | 可视化自动化与 AI 工作流 | 适合连接系统和控制流程；自托管与许可、模型费用分别核对 |
| 102 | [Zapier Agents](https://zapier.com/agents) | Zapier | 连接业务应用并执行任务 | 适合现成 SaaS 应用联动，按连接器权限与任务费用评估 |
| 103 | [Make AI Agents](https://www.make.com/ai-agents) | Make | 可视化编排与智能决策 | 适合把灵活 Agent 接进明确自动化流程 |
| 104 | [Microsoft Copilot Studio](https://www.microsoft.com/en-us/copilot/products/copilot-studio) | 微软 | 组织级 Agent 与业务流程搭建 | 与直接使用办公 Copilot 的角色不同 |
| 105 | [Salesforce Agentforce](https://www.salesforce.com/agentforce/) | Salesforce | 客服、销售和企业服务 Agent | 适合既有业务数据和 CRM 流程；CRM 即客户关系管理系统 |
| 106 | [Glean](https://www.glean.com/) | Glean | 企业搜索、助手与 Agent | 重点是企业知识连接和权限，而不是普通公开网页搜索 |
| 107 | [Fin](https://fin.ai/) | Intercom/Fin | 客户服务、销售及相关客户体验 Agent | 需接入帮助资料和业务系统，评价真实解决率与转人工 |

## 十二、本地模型、多模型客户端与自托管知识库（5 条）

“软件装在本机”只说明一个运行位置；推理、嵌入、检索、遥测和外部工具仍可能走云端。

| 编号 | 产品与官方依据 | 提供方/体系 | 主要用途 | 场景与边界 |
|---|---|---|---|---|
| 108 | [Ollama](https://ollama.com/) | Ollama | 运行和管理模型，本地及云端入口 | 选择本地模型或云模型决定主要推理路径，不把软件名称等同于离线 |
| 109 | [LM Studio / Bionic](https://lmstudio.ai/) | LM Studio | 本地模型与电脑 Agent 相关能力 | 当前首页主推 Bionic；旧教程中的本地模型界面仍需按版本核对 |
| 110 | [Cherry Studio](https://www.cherryai.com.cn/) | Cherry Studio | 多模型 AI 工作站 | 客户端与模型服务是两层；本次官网动态，细项功能未逐项核验 |
| 111 | [Open WebUI](https://openwebui.com/) | Open WebUI | 自托管聊天、Agent 与模型接入界面 | 搭在自己服务器不等于所有连接的模型都在自己服务器 |
| 112 | [AnythingLLM](https://anythingllm.com/) | AnythingLLM | 本地/自部署资料问答与工作助手 | 检查使用的模型、Embedding 和资料索引实际在哪里运行 |

## 十三、容易被旧文章带偏的更名、停运与迁移

本表单独记录产品生命周期，不能将“历史上著名”直接当成“今天适合新注册”。

| 名称 | 本次核实到的状态 | 官方依据 |
|---|---|---|
| QoderWork CN | 公告计划 **2027-09-05** 停止运营；此前仍可下载和使用，建议迁移 Qoder CN 桌面版。这个日期明确针对 CN 公告，不能无条件外推全球版本 | [Qoder CN 下载页中的运营调整说明](https://qoder.cn/download?product=qoderwork) |
| QClaw | 官网已提供停服专区及迁移 WorkBuddy 入口；迁移页注明当前支持个人版 WorkBuddy 授权迁移。本轮未从可读官方页面取得完整停运时间表，不填猜测日期 | [QClaw 官网](https://qclaw.qq.com/)、[官方迁移页](https://qclaw.qq.com/migration) |
| Sora | 官方说明网页与 App 已于 **2026-04-26** 停止，API 已于 **2026-09-24** 停止；因此不放入当前视频工具候选列表 | [Sora 停止服务说明](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) |
| ChatGPT Atlas | 官方发布页顶端已标注弃用，并引导至 ChatGPT Work；保留名称用于识别旧教程 | [Atlas 官方状态提示](https://openai.com/index/introducing-chatgpt-atlas/) |
| Gemini Code Assist / Gemini CLI 旧个人登录服务 | 个人及相应 Pro/Ultra 层级的旧服务自 **2026-06-18** 停止，官方引导迁移 Antigravity；这不等于所有 API、源码或企业合同同日结束 | [个人服务调整](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals) |
| Gemini Code Assist Standard / Enterprise | **2026-10-09** 起停止新购，已有订阅按合同和续约安排继续；应按官方不同期限处理 | [企业服务调整](https://docs.cloud.google.com/gemini/docs/codeassist/sunset) |
| Claude Cowork | 官网说明正在并入 Claude，文件工作可自动调用其能力；旧名称仍有说明文档，不应简单当作另一款独立聊天模型 | [Cowork 产品页](https://claude.com/product/cowork) |
| NotebookLM / Le Chat / Windsurf | 旧入口分别展示或跳转 Gemini Notebook、Mistral Vibe、Devin Desktop；这里只报告本次观察到的入口变化，不凭跳转猜测全部账号迁移细则 | [Gemini Notebook](https://notebook.google/)、[Mistral Vibe](https://mistral.ai/products/vibe/)、[Devin Desktop](https://devin.ai/desktop) |
| 纳米 AI / MiniMax Agent / Zoom AI Assistant | 当前入口分别偏向纳米 work、MiniMax Code、ZoomMate；历史教程名称仍可能出现，应对照现有产品页 | [纳米官方社区说明](https://bbs.360.cn/thread-16187876-1-1.html)、[MiniMax 下载页](https://agent.minimax.io/download)、[Zoom 当前产品页](https://www.zoom.com/en/products/ai-assistant/) |

## 十四、为什么这些产品名字不同，却看起来都能做同一件事

一个完整产品往往组合了多层：

1. **模型**：理解输入、生成文本/图像或提出行动。
2. **运行系统**：保存任务状态，管理文件、工具、权限和重试。
3. **资料连接**：连接本地文件、云盘、邮箱、企业知识库。
4. **产品界面**：聊天窗、桌面应用、浏览器、编辑器或协作空间。
5. **交付方式**：回答、文件、代码变更、系统记录、已执行的操作。

因此，同样接入一个模型，也可能因为工具、上下文和执行环境不同而表现不同。一个产品接入多个模型，也不代表任务一定做得更好。关联 [[SDK与API]]、[[Agent Harness：模型之外的运行系统]]、[[MCP模型上下文协议]]、[[Dify：可视化AI应用、知识库与工作流平台]]。

## 十五、按你的学习与办公场景，怎样缩小选择范围

下表是根据用途做的试用顺序建议，不是性能实测排名：

| 场景 | 可先挑 2～3 个对照 | 用同一个任务怎么比较 |
|---|---|---|
| 日常学习计算机知识 | 当前正在使用的助手 + 另一家综合助手 | 同一问题要求类比、原理、实例、来源，看能否解释清楚并指出不确定处 |
| 整理 Obsidian 笔记 | 支持授权目录读写和 Git 的 Agent；当前 Codex 流程也可继续 | 能否复用旧主题、正确链接、保留原文、只提交指定修改 |
| 做课程课件和销售汇总 | WorkBuddy、千问办公、WPS 灵犀、Genspark/Skywork 中任选少量 | 给同一份脱敏表格和讲义，比较数据正确性、可编辑文件与返工次数 |
| 查资料与整理文献 | Perplexity、秘塔、Gemini Notebook；学术再看 Elicit/Consensus/SciSpace | 核对是否真的找到原始资料、引用是否支持结论、是否漏掉限制条件 |
| 做课程海报和宣传短片 | Canva/稿定/美图设计室 + 即梦/可灵/Runway | 是否遵守尺寸、文字准确、人物/产品一致、能否导出合适格式 |
| 建课程客服与知识库 | Dify/扣子；现有系统自动化可看 n8n/Make | 检查答复依据、用户权限、查订单工具和转人工路径 |
| 开发直播平台功能 | Codex、Claude Code、Cursor、Qoder 等编程工具 | 能否基于现有代码实现、验证、解释影响，而不只生成漂亮界面 |

如果涉及营养品和课程宣传，产品工具可以帮助整理与排版，具体健康主张、商品说明和宣传内容仍需由具备相应专业知识的人核对。本页不据此判断某种宣传是否合法或某种产品是否有效。

## 十六、费用与数据路径怎么问才有用

不要只问“免费吗”，可以分别核对：

- 是基础功能免费，还是注册送一次额度？额度是否会过期？
- 订阅包含多少任务/积分，失败重试、联网、图片和视频是否另外计费？
- 是否需要另买模型 API？应用会员与 API 余额通常是不同账目，具体看供应商规则。
- 交付的是可编辑文件、截图、链接还是只能在平台内使用的页面？
- 资料在本机、供应商云端，还是会进入第三方模型与连接器？
- 团队成员能否隔离资料？能否导出任务、文件、知识和日志？
- 服务停运或套餐变化后，已有内容如何迁移？

**API = Application Programming Interface，应用程序编程接口，读 A-P-I；它是软件之间调用能力的入口。**“我买了聊天会员”不自动意味着自己的程序可以无限调用 API。

本次不写精确价格排行榜，因为地区、税费、年付折扣、积分制和企业合同会让数字不可直接比较。准备付费时再针对候选核对对应定价页。

## 参考与维护

正文每行的产品链接、状态表的公告链接就是该条主要依据；参考日期统一为 2026-11-15。动态页面或抓取失败的条目已标注核实边界，目录不代表真实账号功能测试完成。

下次补充时优先更新对应行，保留更名前后关系，不把旧产品、功能模式和底层模型重复堆成数量。核心办公产品的详细差别继续看 [[AI办公智能体对比：QoderWork、千问办公、WorkBuddy、Muse、dot与Manus]]。
