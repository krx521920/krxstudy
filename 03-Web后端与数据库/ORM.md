---
title: ORM
aliases:
  - Object-Relational Mapping
  - 对象关系映射
tags:
  - 数据库
  - Web后端
  - ORM
created: 2026-08-16
updated: 2026-08-16
---

# ORM

## 一句话解释

**ORM（Object-Relational Mapping，对象关系映射）**是一种在程序对象与关系型数据库表之间建立对应关系的技术，让开发者可以用 Python 等语言中的类和对象查询、创建、修改数据库数据。

## 为什么需要 ORM

关系型数据库通常使用表格和 SQL：

- 表（table）
- 行（row）
- 列（column）
- 主键和外键

面向对象程序通常使用：

- 类（class）
- 对象（object）
- 属性（attribute）
- 对象之间的关系

两边表达同一批业务数据，却使用不同形式。ORM 就像翻译层，在两者之间转换。

## 对应关系

| 程序世界 | 数据库世界 |
|---|---|
| 类 `User` | 表 `user` |
| 一个 `User` 对象 | 表中的一行 |
| 属性 `name` | 列 `name` |
| 对象 ID | 主键 |
| 对象引用/集合 | 外键、多对多关联 |

## Django ORM 示例

先用 Python 类描述数据：

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
```

Django 可以根据模型创建数据库表。之后可使用 Python 代码操作数据：

```python
# 创建
Article.objects.create(title="第一篇笔记", content="正文")

# 查询所有已发布文章
articles = Article.objects.filter(published=True)

# 修改
article = Article.objects.get(id=1)
article.title = "修改后的标题"
article.save()

# 删除
article.delete()
```

查询背后仍会转换成 SQL。上面的筛选可能类似：

```sql
SELECT * FROM article WHERE published = true;
```

## CRUD 是什么

数据库最常见的四类操作常缩写为 CRUD：

- **Create**：创建；
- **Read**：读取；
- **Update**：更新；
- **Delete**：删除。

ORM 通常为这些操作提供一致的对象接口。

## Migration（数据库迁移）

业务不断变化，数据表结构也会变化。例如文章新增 `author` 字段。直接手工修改生产数据库容易出错，所以 ORM 框架通常使用 migration 记录结构变更。

在 [[Django]] 中常见命令是：

```powershell
python manage.py makemigrations
python manage.py migrate
```

- `makemigrations`：根据模型变化生成迁移文件。
- `migrate`：把迁移真正应用到数据库。

迁移文件应像代码一样进入版本控制，但执行迁移前要考虑数据兼容和备份。

## ORM 的优点

- 使用熟悉的编程语言操作数据；
- 减少重复 SQL；
- 自动进行常见参数绑定，降低 SQL 注入风险；
- 数据模型集中、可读；
- 更容易在不同数据库后端之间迁移常规查询；
- 通常集成验证、关系、事务和迁移工具。

## ORM 的限制

### 它不会让数据库知识消失

仍然需要理解表设计、主键、外键、索引、事务和 SQL。

### 自动生成的查询可能效率低

代码看起来只是一行，但可能触发大量 SQL。典型例子是 **N+1 查询**：先查询 N 条记录，又为每条记录单独查一次关联数据。

### 复杂查询不一定更易读

报表、递归、窗口函数或数据库特有功能，有时直接写 SQL 更清楚、更高效。

### 抽象可能隐藏真实成本

读取一个对象属性，有时会悄悄访问数据库。开发者需要学会查看 ORM 实际生成的 SQL。

## ORM 不是什么

- ORM 不是数据库本身；
- ORM 不是数据备份工具；
- ORM 不是 [[SDK与API|Web API]]；
- ORM 不保证查询一定高效；
- ORM 不能代替合理的数据建模。

## 初学建议

学习 ORM 时，同时练习以下 SQL：

1. `SELECT`、`INSERT`、`UPDATE`、`DELETE`；
2. `WHERE`、`ORDER BY`；
3. `JOIN`；
4. 主键、外键、唯一约束；
5. 索引；
6. 事务。

每写一个 ORM 查询，都尝试想一想它可能生成什么 SQL。

## 参考资料

- [Django 官方文档：Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django 官方文档：Making queries](https://docs.djangoproject.com/en/stable/topics/db/queries/)
