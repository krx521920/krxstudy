---
title: SQL 基础查询与多表关联
aliases: [SQL基础, JOIN, GROUP BY, CTE]
tags: [数据库, SQL, 查询]
created: 2026-09-08
updated: 2026-09-08
verified: 2026-09-08
---

# SQL 基础查询与多表关联

> [!summary] 一句话解释
> 查询先选定数据来源，再筛选、关联和汇总，最后决定输出哪些列及顺序；最重要的是始终知道一行代表什么。

SQL 全称和路线见 [[SQL与关系型数据库学习地图]]。下面示例使用 [[SQL订单实战：样例数据与练习]] 的表，`amount_cents` 表示分。

## 筛选与排序

像查订单账本一样，先挑出已付款订单，再按付款日期从新到旧排列：

```sql
-- lab: latest_paid
SELECT order_id, customer_id, amount_cents
FROM orders
WHERE status = 'paid'
ORDER BY paid_day DESC, order_id DESC
LIMIT 3;
```

返回订单 109、108、106。`SELECT` 选列，`WHERE` 筛选，`ORDER BY` 排序，`LIMIT` 限制数量。同一天可能有多笔订单，所以增加唯一的订单 ID 作为次序条件，结果才稳定。ID 是 Identifier（标识符，读作 I-D），此处即订单编号。

没有 `ORDER BY` 就不能保证结果顺序。主键、自增 ID 或索引都不能代替显式排序。

查询日期区间常用半开区间：`paid_day >= '2026-08-01' AND paid_day < '2026-09-01'`。对时间戳也采用“含开始、不含结束”，便于表达完整月份，避免漏掉最后一天的小数秒。

## NULL 与三值逻辑

NULL 表示缺失或未知，不等于数字 0，也不等于空字符串。

- 判断是否缺失用 `IS NULL` 或 `IS NOT NULL`。
- `paid_day = NULL` 无法得到期望的“为空”筛选。
- SQL 条件有真、假、未知；`WHERE` 只保留结果为真的行。
- `COUNT(*)` 数行，`COUNT(paid_day)` 只数非 NULL 值。
- `SUM`、`AVG` 等通常跳过 NULL；对空集合求 `SUM` 得到 NULL，`COUNT` 得到 0。
- `COALESCE(value, 0)` 在值缺失时提供 0，但要先确认业务上缺失真的意味着零。

`NOT IN` 的子查询若包含 NULL，可能让本来想保留的行也被排除。查询“没有发生过某事”时，通常更容易用 `NOT EXISTS` 清楚表达。

## JOIN 如何把表联系起来

JOIN（连接，读作 join）按条件匹配两边的行：

| 类型 | 含义 | 例子 |
|---|---|---|
| INNER JOIN | 只保留匹配成功的组合 | 订单及其客户 |
| LEFT JOIN | 左表全部保留，右表无匹配时补 NULL | 包括没有订单的客户 |
| CROSS JOIN | 每个左行与每个右行组合 | 日期 × 城市的完整报表网格 |
| FULL OUTER JOIN | 两边未匹配行也保留 | 两套账本的全量对账；产品支持不同 |
| 自连接 | 同一张表用两个别名关联 | 员工与上级 |

统计每位客户的已付款订单数，并保留没有付款的客户：

```sql
-- lab: customer_counts
SELECT c.customer_id, COUNT(o.order_id) AS paid_orders
FROM customers c
LEFT JOIN orders o
  ON o.customer_id = c.customer_id AND o.status = 'paid'
GROUP BY c.customer_id
ORDER BY c.customer_id;
```

结果是客户 1～5 分别为 3、2、2、0、0。

这里把付款条件写在 `ON` 中，是让它参与右侧匹配。若写成 `WHERE o.status = 'paid'`，没有匹配的客户会被过滤掉。外连接后用 `COUNT(*)` 会连那一行补 NULL 的结果也数进去，所以这里数 `o.order_id`。

## EXISTS：只问有没有

找从未付过款的客户：

```sql
-- lab: never_paid
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM orders o
  WHERE o.customer_id = c.customer_id AND o.status = 'paid'
)
ORDER BY c.customer_id;
```

结果是 4、5。`EXISTS` 检查子查询是否至少有一行，`SELECT 1` 不代表需要统计 1，也不意味着只能读取一行。

## GROUP BY 与 HAVING

`GROUP BY` 把相同客户的订单归成一组；`HAVING` 筛选汇总后的组：

```sql
-- lab: big_customers
SELECT customer_id, SUM(amount_cents) AS paid_cents
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount_cents) >= 30000
ORDER BY customer_id;
```

只得到客户 1、40000 分。`WHERE` 先排除未付款订单，`HAVING` 再判断已付款总额。

概念上的处理次序是：来源与 JOIN → WHERE → 分组与聚合 → HAVING → 窗口计算 → 输出与去重 → 最终排序与分页。它帮助理解语义，不是执行引擎必须照此逐步扫描的物理顺序。

## 子查询与 CTE

**CTE** 是 **Common Table Expression（公用表表达式，读作 C-T-E）**，用 `WITH` 给一个查询结果起临时名称，适合把复杂任务拆成几步。

```sql
-- lab: repeated_buyers
WITH per_customer AS (
  SELECT customer_id, COUNT(*) AS order_count
  FROM orders WHERE status = 'paid'
  GROUP BY customer_id
)
SELECT customer_id FROM per_customer
WHERE order_count >= 2
ORDER BY customer_id;
```

先数每位客户付款次数，再挑出至少两次的客户；结果为 1、2、3。CTE 不等于永久建表，也不保证一定更快；优化器可能内联它，也可能物化中间结果，具体看产品与查询。

`WITH RECURSIVE` 用于递归查询树或图，需要终止条件、循环处理和合理的深度控制。它是后续进阶，不是普通查询的必经步骤。

### CTE 的作用域与多个步骤

CTE 名称通常只在紧随 WITH 的这一条语句内可用；语句结束后，不会自动留下叫 per_customer 的表。普通 CTE 也不是可以在其他程序中直接调用的函数。

多个 CTE 可以依次组织业务逻辑：

```sql
-- lab: cte_steps
WITH paid_orders AS (
  SELECT customer_id, amount_cents FROM orders WHERE status = 'paid'
), customer_totals AS (
  SELECT customer_id, SUM(amount_cents) AS cents
  FROM paid_orders GROUP BY customer_id
)
SELECT COUNT(*) AS customers_above_200_yuan
FROM customer_totals WHERE cents >= 20000;
```

结果是 2。第一步挑订单，第二步汇总客户，最后数达标客户。名字应描述这一阶段的粒度和意义，比 t1、t2 更容易检查。

### CTE、子查询、临时表、视图怎么选

| 方式 | 存在范围和作用 |
|---|---|
| 子查询 | 嵌在另一条查询里，适合局部计算 |
| 普通 CTE | 给当前语句的中间结果起名，提高多步逻辑可读性 |
| 临时表 | 实际保存临时数据，生命周期和事务行为依产品；可分多条语句使用 |
| 普通视图 | 持久保存查询定义，通常每次使用时仍执行相应查询逻辑 |
| 物化视图/汇总表 | 保存预先计算结果，需要刷新或维护 |

是否缓存中间结果、是否能利用索引，应看具体执行计划。不要把 WITH 当成“强制先完整执行这一段”的通用指令。

### 递归 CTE：最小可运行例子

```sql
-- lab: recursive_numbers
WITH RECURSIVE numbers(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1 FROM numbers WHERE n < 5
)
SELECT n FROM numbers ORDER BY n;
```

得到 1～5。`SELECT 1` 是起点；递归部分以已产生的层次结果生成下一层；`n < 5` 是终止条件。理解这个过程后，才把数字换成“部门的下级部门”。

组织关系若有 A→B→A 循环，递归可能无法按预期结束，必须处理已访问节点和深度。不同数据库有不同递归限制；不依赖 LIMIT 作为所有引擎通用的防无限递归保险。

## UNION、去重与数据粒度

`UNION ALL` 拼接结果并保留重复行，`UNION` 按选出的整行去重，后者通常增加处理成本。`DISTINCT` 也只按选出的列去重，它不知道“同一个客户”的业务定义。

一对多 JOIN 会增加行数。订单有两行商品时，关联后订单金额就出现两次；再关联两笔退款，可能变成四行。不要靠 `SUM(DISTINCT amount_cents)` 修补，因为不同订单可能恰好金额相同。正确方法见 [[SQL复杂统计与报表设计]]。

## 写入、参数与学习建议

`INSERT` 增加记录，`UPDATE` 修改，`DELETE` 删除。实际修改前先用相同条件 SELECT 核对目标；涉及多步业务时学习 [[SQL事务、锁与并发一致性]]。

程序接收用户输入时，应通过驱动的参数绑定传入值，不把输入拼进 SQL 字符串。占位符因驱动而异，如 SQLite Python 的 `?`；表名、列名等标识符通常不能当普通值绑定，需要受控白名单。

练习顺序：筛选十条订单 → 找未付款订单 → 保留零订单客户 → 汇总客户金额 → 用 EXISTS 查缺失关联 → 解释每次 JOIN 后的行数。

相关：[[SQL与关系型数据库学习地图]]、[[SQL窗口函数：排名、累计与同期比较]]、[[ORM]]。

## 参考资料

核对日期：2026-09-08。

- [PostgreSQL：SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL：比较与 NULL](https://www.postgresql.org/docs/current/functions-comparison.html)
- [PostgreSQL：WITH 查询](https://www.postgresql.org/docs/current/queries-with.html)
