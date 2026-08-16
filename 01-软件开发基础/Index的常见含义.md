---
title: Index 的常见含义
aliases:
  - Index
  - Indexing
  - 索引
  - 下标
  - 数据库索引
  - Git Index
  - index.html
tags:
  - 计算机基础
  - 编程
  - 数据库
  - Git
  - Web
created: 2026-08-16
updated: 2026-08-16
verified: 2026-08-16
---

# Index 的常见含义

> [!summary] 一句话解释
> **Index 读作“因代克斯”，一般表示“索引”或“位置编号”：它帮助程序根据一个位置、关键词或键快速找到目标；但在数组、数据库、搜索系统、Git 和网页文件名中，具体含义并不相同。**

## 单词本身是什么意思

**Index** 的常见中文翻译有：

- **索引**：帮助查找内容的目录或数据结构；
- **下标/位置编号**：表示某个元素在一组数据中的位置；
- **编制索引**：当它作为动词使用时，表示整理数据并建立可搜索结构。

常见英文形式：

- `index`：单数，也可作动词；
- `indexes` 或 `indices`：复数；
- `indexing`：正在建立索引，常译为“索引构建”或“编制索引”。

虽然这些用法共享“帮助定位”的想法，但不能只看到 `index` 就固定翻译。必须结合上下文判断。

## 生活类比：书的目录与页码

一本书里有两种与 Index 很相似的东西：

1. **页码**：第 1 页、第 2 页，表示内容的位置；
2. **书末索引**：例如“数据库：第 35、82 页”，根据关键词快速定位内容。

数组的 index 更像页码；数据库和搜索引擎的 index 更像书末的关键词索引。

它们共同解决的问题是：

```text
我知道一个位置或关键词
          ↓
怎样更快地找到对应内容？
```

---

## 最常见的六种 Index

| 看到它的场景 | 这里的 Index 是什么 | 常见中文 |
|---|---|---|
| `users[0]`、`array[index]` | 元素的位置编号 | 下标、索引 |
| `CREATE INDEX` | 帮数据库加速查询的辅助数据结构 | 数据库索引 |
| 搜索引擎、RAG 的 indexing | 把资料处理成可检索结构的过程 | 建立索引 |
| Git index | 为下一次提交准备的文件内容 | 暂存区 |
| `index.html` | Web 服务器常用的默认页面文件 | 首页、默认文档 |
| `src/index.ts`、`index.js` | 项目约定的入口或集中导出文件 | 入口文件、聚合文件 |

下面逐一展开。

---

## 一、数组中的 Index：元素的位置编号

**Array（数组）**可以先理解为“一排按顺序存放的数据”。

```ts
const fruits = ['苹果', '香蕉', '橙子']

console.log(fruits[0]) // 苹果
console.log(fruits[1]) // 香蕉
console.log(fruits[2]) // 橙子
```

方括号中的数字就是 index，也常叫**数组下标**。

### 为什么第一个元素是 0

JavaScript、TypeScript、Python、C 等许多语言使用 **Zero-based Indexing（从零开始的索引）**：

```text
数据：   苹果    香蕉    橙子
index：   0       1       2
```

可以把 index 理解为“从起点向后偏移多少个位置”——第一个元素距离起点的偏移量是 0，所以它的 index 是 0。

如果数组长度为 `length`：

```text
第一个元素的 index = 0
最后一个元素的 index = length - 1
```

例如长度为 3，最后一个下标就是 `3 - 1 = 2`。

> [!warning] 并非所有系统都从 0 开始
> 数据库表格的行号、数学教材和某些编程语言可能从 1 开始。不要把“Index 永远从 0 开始”当成普遍定律。

### 越界是什么意思

```ts
const fruits = ['苹果', '香蕉', '橙子']
console.log(fruits[10])
```

数组里没有 index 为 10 的元素，这叫 **Out of Bounds（越界）**。

在 JavaScript 中，上面的读取通常得到 `undefined`；其他语言可能直接抛出越界异常。[[TypeScript与JavaScript|TypeScript]] 能提前发现一部分问题，但普通数组下标是否越界仍可能只能在运行时确定。

---

## 二、数据库中的 Index：加速查询的辅助结构

假设用户表有一百万行：

| id | name | email |
|---|---|---|
| 1 | 小明 | ming@example.com |
| 2 | 小红 | hong@example.com |
| ... | ... | ... |

现在要查找某个邮箱：

```sql
SELECT * FROM users
WHERE email = 'ming@example.com';
```

### 没有合适索引时

数据库可能需要从第一行开始逐行检查，这叫 **Full Table Scan（全表扫描）**：

```text
第 1 行 → 第 2 行 → 第 3 行 → …… → 第 1,000,000 行
```

### 建立索引后

可以为 `email` 列建立索引：

```sql
CREATE INDEX idx_users_email ON users(email);
```

数据库会额外维护一种适合查找的数据结构。许多常规索引使用 **B-tree（B 树）**一类的有序树结构，让系统不必每次扫描整张表。

```mermaid
flowchart LR
    Query["查询 email"] --> Planner["数据库查询规划器"]
    Planner --> Index["在 email 索引中定位"]
    Index --> Row["找到对应数据行"]
```

数据库索引很像书末索引：看到“TypeScript”，先在索引里找到页码，再翻到正文，而不是从第一页开始阅读。

### 索引为什么不能越多越好

索引不是免费的：

- 占用额外磁盘空间；
- 插入数据时要更新索引；
- 修改被索引字段时要更新索引；
- 删除数据时也要维护索引；
- 不合适或很少使用的索引可能只有成本，没有收益；
- 数据库查询规划器也不保证每次都选择索引。

所以正确理解是：

```text
索引通常让特定读取更快
但会增加存储和写入维护成本
```

在 [[ORM]] 中，即使不经常手写 SQL，也仍然需要理解数据库索引，因为一行看似简单的 ORM 查询可能扫描大量数据。

---

## 三、搜索引擎和 RAG 中的 Index

搜索系统不能等用户输入关键词后，才临时阅读互联网上的全部网页。它会提前处理资料并建立可搜索结构。

一个简化流程是：

```mermaid
flowchart LR
    Source["网页或文档"] --> Collect["抓取/导入"]
    Collect --> Process["解析、分词和清洗"]
    Process --> Index["建立搜索索引"]
    Query["用户查询"] --> Search["检索索引"]
    Index --> Search
    Search --> Result["返回相关内容"]
```

### 倒排索引是什么

**Inverted Index（倒排索引）**会记录“哪个词出现在哪些文档中”。

```text
TypeScript → 文档 2、文档 5、文档 9
Django     → 文档 1、文档 7
```

用户搜索 `TypeScript` 时，系统可以直接找到相关文档编号，不必逐篇重新阅读。

### RAG 中的 Indexing

在 [[RAG、Naive RAG与GraphRAG|RAG]] 中，“离线索引”通常是一个较宽泛的阶段：

1. 读取文档；
2. 切成较小文本块；
3. 计算 Embedding（嵌入向量）；
4. 保存文本、向量和元数据；
5. 建立适合相似度检索的结构。

所以 RAG 文档中的 `index` 可能指：

- 整套资料处理过程；
- 已处理好的可检索资料集合；
- 向量数据库中的近邻搜索结构。

具体含义要看工具文档，不能认为所有产品里的 `index` 都是同一种文件或数据表。

### 搜索索引不等于搜索排名

- **Crawling（抓取）**：找到并下载网页；
- **Indexing（建立索引）**：理解、整理并保存可搜索信息；
- **Ranking（排序）**：用户搜索时决定哪些结果更靠前。

网页已被抓取，不代表一定成功进入索引；进入索引，也不代表一定排在搜索结果前面。

---

## 四、Git Index：暂存区

在 Git 中，**Index** 是一个专有名称，也就是常说的 **Staging Area（暂存区）**。

它保存的是“准备放入下一次提交的文件内容”。

```mermaid
flowchart LR
    Work["工作区：正在编辑"] -->|"git add"| Index["Git Index：暂存区"]
    Index -->|"git commit"| Repo["本地提交历史"]
    Repo -->|"git push"| Remote["GitHub 远程仓库"]
```

例如：

```powershell
git add note.md
git commit -m "更新笔记"
git push
```

含义分别是：

1. `git add`：把 `note.md` **当前这一刻的内容**放进 Git Index；
2. `git commit`：根据 Index 中准备好的内容创建本地提交；
3. `git push`：把本地提交发送到远程仓库。

### 为什么修改后可能要再次 git add

如果先运行 `git add note.md`，然后又继续修改 `note.md`：

- 暂存区里保存的是第一次 `git add` 时的版本；
- 工作区里是后来修改的新版本；
- 想把新修改也提交，需要再次运行 `git add note.md`。

两个有用的比较命令：

```powershell
git diff           # 工作区与暂存区的差异
git diff --cached  # 暂存区与上一次提交的差异
```

Git Index 通常保存在仓库内部的 `.git/index` 二进制文件中，但日常不应手动编辑它，而应使用 `git add`、`git restore --staged`、`git status` 等命令操作。

> [!warning] `git add` 不等于上传 GitHub
> `git add` 只更新本地暂存区；还需要 `git commit` 和 `git push`，远程仓库才会同步。

---

## 五、index.html：网站默认页面

`index.html` 是 Web 项目里很常见的文件名：

```text
my-site/
├── index.html
├── styles/
│   └── main.css
└── scripts/
    └── app.js
```

许多 Web 服务器被配置为：当用户只访问一个目录，没有写具体文件名时，尝试返回这个目录中的 `index.html`。

```text
访问：https://example.com/
可能返回：https://example.com/index.html
```

这里的 `index` 可以理解为“这个目录的默认入口页”。

但要注意：

- `index.html` 不是 [[HTML]] 语法规定的关键字；
- 它是广泛使用的文件命名和服务器配置惯例；
- 服务器也可以改用其他默认文件；
- 现代单页应用或后端路由可能没有一一对应的实体页面文件。

---

## 六、index.js 与 index.ts：项目入口或聚合文件

你还会经常看到：

```text
src/
├── index.ts
├── user.ts
└── article.ts
```

`index.ts` 可能承担两种角色。

### 角色 1：程序入口

构建工具或运行命令从这个文件开始加载程序：

```ts
import { startApp } from './app'

startApp()
```

在 [[Webpack与HMR|Webpack]] 中，入口可以配置为 `src/index.js`，但文件名并不是强制的，也可以配置成 `main.ts` 或其他名字。

### 角色 2：集中导出

```ts
export { User } from './user'
export { Article } from './article'
```

其他模块只需从这个目录导入，而不用分别知道每个文件的位置。这种集中导出的文件有时叫 **Barrel File（桶文件/聚合导出文件）**。

这同样属于项目约定，不是 JavaScript 或 TypeScript 赋予 `index.ts` 的特殊语法能力。

---

## Index、ID 和 Key 有什么区别

这三个词经常一起出现：

| 概念 | 常见中文 | 主要作用 | 是否一定不变 |
|---|---|---|---|
| Index | 索引、下标 | 帮助定位或加速查找 | 不一定 |
| ID（Identifier） | 标识符、编号 | 唯一识别某个对象 | 通常希望稳定 |
| Key | 键 | 用来查找、关联或唯一标识数据 | 取决于场景 |

例如：

```ts
const users = [
  { id: 101, name: '小明' },
  { id: 205, name: '小红' }
]
```

- 小明的数组 index 是 `0`；
- 小明的 ID 是 `101`；
- 如果把小红移动到数组第一位，她的 index 会变成 `0`，但 ID 仍可以是 `205`。

所以不要用会变化的数组 index 冒充稳定的业务 ID。

---

## 怎样根据上下文判断含义

看到这些表达时，可以快速判断：

```text
array[index] / list[0]
→ 数组或列表的位置下标

CREATE INDEX / database index
→ 数据库查询加速结构

index documents / search index / vector index
→ 搜索或 RAG 的可检索结构

git index / add to the index
→ Git 暂存区

index.html
→ 网站的默认入口页面

src/index.js / index.ts
→ 项目约定的入口或集中导出文件
```

如果还不能确定，可以继续问三个问题：

1. 它正在给什么东西编号或建立查找结构？
2. 它帮助谁找到什么内容？
3. 它是语言规则、工具内部结构，还是文件命名惯例？

---

## 常见误区

### 误区 1：所有 Index 都是数据库索引

不是。数组下标、Git 暂存区和 `index.html` 都不是数据库索引。

### 误区 2：所有 Index 都从 0 开始

不是。许多编程语言的数组从 0 开始，但数据库索引、搜索索引和 Git Index 根本不是这种位置编号。

### 误区 3：数据库索引一定让所有操作更快

不是。它主要加速合适的查询，同时增加空间和写入维护成本。

### 误区 4：`index.html` 是 HTML 强制要求的文件名

不是。它是服务器和项目广泛采用的默认页面惯例，可以配置改变。

### 误区 5：`git add` 已经把文件上传了

不是。它只把指定内容放入本地 Git Index，随后还要提交和推送。

### 误区 6：Index 与 ID 是一回事

不是。数组 index 可能随排序和增删改变，稳定 ID 通常用于识别具体对象。

---

## 学习建议

初学阶段建议按这个顺序理解：

1. 用数组练习 `items[0]`、`items[1]` 和 `length - 1`；
2. 学 Git 时画出“工作区 → 暂存区 → 提交 → 远程仓库”；
3. 学 [[HTML]] 时理解为什么网站常有 `index.html`；
4. 学 [[ORM]] 和 SQL 后，再练习数据库索引与查询计划；
5. 学 [[RAG、Naive RAG与GraphRAG|RAG]] 时再区分关键词索引、向量索引与索引流程。

不要先背各种索引算法。先学会根据上下文判断 `index` 指的到底是什么。

## 关联概念

- [[TypeScript与JavaScript]]：数组下标、`index.ts` 和类型检查。
- [[Git Hook与自动化检查]]：Git 提交前后的自动检查，以及 Git Index 的位置。
- [[HTML]]：`index.html` 常作为网站默认页面。
- [[Webpack与HMR]]：`index.js` 或 `index.ts` 常被配置为构建入口。
- [[ORM]]：ORM 查询的性能仍受数据库索引影响。
- [[RAG、Naive RAG与GraphRAG]]：文档、向量和图数据的索引与检索。
- [[TCP、HTTP、HTTPS与WebSocket|HTTP 与 HTTPS]]：浏览器通过它们请求 `index.html` 等网页资源。

## 参考资料

> [!info] 核对日期
> 2026-08-16。不同语言、数据库、搜索产品和 Web 服务器的具体行为可能不同，实际项目应继续查看相应工具的官方文档。

- [MDN：JavaScript Arrays](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/Arrays)
- [PostgreSQL 官方文档：Indexes Introduction](https://www.postgresql.org/docs/current/indexes-intro.html)
- [Git 官方文档：The Index](https://git-scm.com/docs/gitdatamodel.html#_the_index)
- [MDN：The default index.html page](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Creating_links#the_default_index.html_page)
- [Google Search Central：Crawling and Indexing](https://developers.google.com/search/docs/crawling-indexing)
- [Elastic 官方文档：Index and search basics](https://www.elastic.co/docs/solutions/search/get-started/index-basics)
