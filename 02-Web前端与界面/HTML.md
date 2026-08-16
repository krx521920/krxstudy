---
title: HTML
aliases:
  - HyperText Markup Language
  - 超文本标记语言
tags:
  - Web前端
  - HTML
  - 网页基础
created: 2026-08-16
updated: 2026-08-16
---

# HTML

## 一句话解释

**HTML（HyperText Markup Language，超文本标记语言）**是描述网页内容和结构的标记语言。它告诉浏览器：这里是标题、这里是段落、这里是图片、这里是链接，而不是主要负责颜色和复杂程序逻辑。

## 用房子类比

- HTML：房子的结构和房间用途；
- [[CSS]]：装修、颜色、大小和布局；
- JavaScript：开灯、开门、点击按钮等行为；
- [[TCP、HTTP、HTTPS与WebSocket|HTTPS]]：把这些网页文件从服务器安全送到浏览器；
- [[渲染逻辑]]：浏览器把结构和样式变成屏幕像素的过程。

## 一个最小 HTML 页面

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <title>我的第一张网页</title>
  </head>
  <body>
    <h1>你好，世界！</h1>
    <p>这是一个段落。</p>
    <a href="https://example.com">打开示例网站</a>
  </body>
</html>
```

逐项解释：

- `<!doctype html>`：告诉浏览器按现代 HTML 标准解析。
- `<html>`：整个 HTML 文档的根元素。
- `<head>`：网页元数据，例如字符编码、标题、CSS 链接。
- `<body>`：用户实际看到的主要内容。
- `<h1>`：一级标题。
- `<p>`：段落。
- `<a>`：链接。

## Element、Tag 和 Attribute

这三个词经常一起出现：

```html
<img src="cat.jpg" alt="一只橘猫">
```

- **Tag（标签）**：尖括号包围的标记，例如 `<img>`。
- **Element（元素）**：标签及其内容组成的完整结构。
- **Attribute（属性）**：为元素提供额外信息，例如 `src` 和 `alt`。

`src` 指出图片地址；`alt` 是图片无法显示或屏幕阅读器读取时使用的替代文字。

## HTML 的“超文本”和“标记”是什么意思

- **HyperText（超文本）**：文档不仅有普通文字，还能通过链接连接到其他文档或页面位置。
- **Markup（标记）**：使用标签标注内容的含义和结构。

HTML 的价值不只是“把字放到页面上”，而是表达语义。例如：

- `<nav>` 表示导航区域；
- `<main>` 表示主要内容；
- `<article>` 表示独立文章；
- `<button>` 表示可以操作的按钮；
- `<form>` 表示表单。

语义清楚有利于无障碍、搜索引擎和代码维护。

## 浏览器拿到 HTML 后发生什么

1. 浏览器通过 [[TCP、HTTP、HTTPS与WebSocket|HTTPS]] 请求页面。
2. 服务器返回 HTML 文本。
3. 浏览器解析 HTML，构建 DOM（Document Object Model，文档对象模型）树。
4. HTML 可能继续引用 CSS、JavaScript、图片和字体，浏览器再发起请求。
5. DOM 与 CSSOM 组合形成渲染树。
6. 浏览器计算布局、绘制并合成最终画面。

详细过程见 [[渲染逻辑]]。

## DOM 是什么

DOM 是浏览器把 HTML 表示成的树形对象结构。JavaScript 可以读取和修改它。

例如：

```html
<body>
  <h1>标题</h1>
  <p>正文</p>
</body>
```

大致会形成：

```text
body
├── h1
│   └── “标题”
└── p
    └── “正文”
```

当 JavaScript 修改 DOM，浏览器可能需要重新计算和显示相关界面。

## HTML 能做什么

- 标题、段落、列表和表格；
- 图片、音频和视频；
- 链接和导航；
- 输入框、按钮和表单；
- 页面语义结构；
- 一些原生交互元素，例如 `<details>` 和 `<dialog>`；
- 引入 CSS 和 JavaScript。

## HTML 不能独立解决什么

- 复杂视觉设计通常需要 [[CSS]]；
- 复杂交互和数据更新通常需要 JavaScript；
- 登录验证、数据库查询等应由 [[Django]] 等后端完成；
- 网络传输依赖 [[TCP、HTTP、HTTPS与WebSocket]] 等协议；
- HTML 不是数据库，也不是服务器。

## HTML 是编程语言吗

通常不把 HTML 称为通用编程语言，而称为**标记语言**。它主要声明内容结构和语义，没有普通编程语言完整的变量、循环、函数和业务控制流。

这不表示 HTML 不重要。没有清楚的 HTML 结构，CSS、JavaScript、无障碍和搜索引擎都会更难正确工作。

## HTML 与 Markdown 的关系

Obsidian 笔记使用 Markdown。Markdown 是一种更简洁的文本标记语法，通常会被转换为 HTML 后显示：

```markdown
# 标题

这是一个段落。
```

可转换为类似：

```html
<h1>标题</h1>
<p>这是一个段落。</p>
```

HTML 表达能力更完整，Markdown 更适合快速写作。

## 常见误区

### “所有东西都用 `<div>` 就行”

视觉上可能能做出来，但会丢失语义。标题用标题标签，按钮用 `<button>`，导航用 `<nav>`，通常更利于无障碍和维护。

### “按钮看起来像按钮就可以”

用 `<div>` 模拟按钮可能缺少键盘操作和无障碍行为。优先使用原生语义元素。

### “HTML5 是一个需要单独安装的软件”

不是。HTML 是 Web 标准，现代浏览器直接解析它。

## 推荐学习顺序

1. 文档基本结构；
2. 标题、段落、列表和链接；
3. 图片及 `alt`；
4. 语义元素；
5. 表单与输入控件；
6. DOM 基本概念；
7. 再学习 [[CSS]] 和 JavaScript。

## 参考资料

- [MDN：HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN：Structuring content with HTML](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content)
