---
title: CSS
aliases:
  - Cascading Style Sheets
  - 层叠样式表
tags:
  - Web前端
  - CSS
created: 2026-08-16
updated: 2026-08-16
---

# CSS

## 一句话解释

**CSS（Cascading Style Sheets，层叠样式表）**是一种描述网页“长什么样、怎样排列”的样式语言。

## HTML、CSS、JavaScript 如何分工

可以把网页比作一间房子：

- **[[HTML]]**：房子的结构，哪里是门、窗、桌子。
- **CSS**：装修和布局，颜色、尺寸、间距、桌子摆在哪里。
- **JavaScript**：行为和交互，点击开关后灯亮、按按钮后弹出提示。

它们会互相配合，但职责不同。CSS 不是用来存数据库数据的，也通常不负责向服务器发送请求。

## 一条 CSS 规则长什么样

```css
.save-button {
  color: white;
  background-color: #2563eb;
  padding: 8px 16px;
  border-radius: 8px;
}
```

逐项解释：

- `.save-button` 是 selector（选择器），表示找到 class 为 `save-button` 的元素。
- `color`、`background-color` 等是 property（属性）。
- `white`、`#2563eb` 等是 value（值）。
- 一条 `属性: 值;` 叫 declaration（声明）。

对应 HTML：

```html
<button class="save-button">保存</button>
```

## CSS 主要能做什么

- 设置文字、颜色、背景、边框和阴影；
- 控制宽高、内外边距和圆角；
- 使用 Flexbox、Grid 等方式进行布局；
- 适配手机、平板和电脑等不同屏幕；
- 实现 hover、focus 等交互状态；
- 添加过渡和动画；
- 控制打印、语音等其他媒体上的表现。

## 为什么叫“层叠”

同一个元素可能同时匹配多条规则。浏览器需要根据一套规则决定谁生效，重要因素包括：

1. 来源和重要性；
2. selector specificity（选择器优先级/特异性）；
3. 规则出现顺序；
4. inheritance（继承）。

初学者常遇到“我明明写了 CSS，为什么没生效”，很多时候就是旧规则被优先级更高或位置更后的规则覆盖了。

## 盒模型

浏览器通常把每个元素看成一个盒子：

```text
margin（外边距）
  border（边框）
    padding（内边距）
      content（内容）
```

- `content`：文字、图片等实际内容。
- `padding`：内容和边框之间的空白。
- `border`：盒子的边线。
- `margin`：这个盒子和其他盒子之间的距离。

理解盒模型，是处理“为什么元素这么宽”“为什么两个组件离得这么远”的基础。

## 布局：Flexbox 与 Grid

- **Flexbox**：擅长一维排列，例如一行按钮或一列菜单。
- **Grid**：擅长二维网格，例如同时控制多行多列的仪表盘。

初学时先掌握普通文档流、盒模型和 Flexbox，再学习 Grid，会更顺畅。

## 响应式设计

同一个网页需要在不同尺寸的屏幕上可用。CSS 可以通过 media query（媒体查询）改变布局：

```css
@media (max-width: 600px) {
  .sidebar {
    display: none;
  }
}
```

含义是：屏幕宽度不超过 600px 时，隐藏侧边栏。

## CSS 与“渲染”的关系

浏览器解析 CSS 后会构建 CSSOM，再与 HTML 形成的 DOM 组合，确定哪些元素可见、大小和位置是什么，最后把像素绘制到屏幕。完整过程见 [[渲染逻辑]]。

## 常见误区

### “CSS 是一种普通编程语言”

通常把 CSS 称为样式表语言。它有变量、计算和条件能力，但主要职责仍是声明“应该呈现什么样式”，而不是像 JavaScript 那样组织通用业务流程。

### “会用组件库就不用学 CSS”

组件库只能覆盖常见设计。遇到布局错位、样式覆盖、响应式问题时，仍需要理解选择器、盒模型和布局。

### “只要页面看起来对就可以”

还要考虑不同屏幕、浏览器、键盘操作、无障碍、性能和可维护性。

## 推荐学习顺序

1. 选择器和基本语法；
2. 颜色、字体、单位；
3. 盒模型；
4. 普通文档流与定位；
5. Flexbox；
6. Grid；
7. 响应式设计；
8. 层叠、继承和优先级；
9. 动画与工程化。

## 参考资料

- [MDN：CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [MDN：CSS styling basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics)
