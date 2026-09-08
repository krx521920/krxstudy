---
title: SQL 索引、执行计划与性能优化
aliases: [SQL优化, SQL执行计划, EXPLAIN, 慢查询]
tags: [数据库, SQL, 性能, 索引]
created: 2026-09-08
updated: 2026-09-08
verified: 2026-09-08
---

# SQL 索引、执行计划与性能优化

> [!summary] 一句话解释
> SQL 优化是在保持结果正确的前提下，找到真正的开销来源，减少不必要的扫描、关联、排序、等待与传输，再用测量验证。

像图书馆查资料：慢可能是没有目录，也可能是你要求搬出半个馆、多人占用同一个柜子，或者书找到了却要跨城运送。不是一切慢查询都靠加索引解决。

树的原理见 [[B+树与数据库索引原理]]；查询语义见 [[SQL基础查询与多表关联]]。

## 一条查询大致怎么执行

```mermaid
flowchart LR
    Q["SQL 与绑定参数"] --> P["解析、名称与权限检查"]
    P --> O["优化器：估算不同方案成本"]
    O --> E["执行：扫描、关联、聚合、排序"]
    E --> R["结果序列化与网络传输"]
    S["统计信息、索引和数据分布"] --> O
```

这是简化模型。优化器选择物理方案，不必按 SQL 的书写顺序逐句做；同一 SQL 在数据分布、参数或版本变化后可能选不同计划。

## 先记录基线，不要盲改

- 明确是接口总耗时、数据库执行时间、连接等待，还是锁等待。
- 记录代表性参数、数据规模、返回行数与查询频率。
- 比较平均值以外的慢请求，例如 P95/P99（第 95/99 百分位延迟，读作 P-95/P-99）。
- 验证当前结果，尤其是 JOIN 放大、NULL、退款和时区口径。
- 在安全测试环境每次改变一个主要因素，再比较相同负载。

十条订单的练习只适合验证语义与观察工具，不适合推导生产索引一定快几倍。缓存冷热和并发负载也会显著改变测量结果。

## 针对查询设计联合索引

需求：“客户 1 最近的三笔已付款订单”。先考虑等值条件，再考虑排序与返回数量：

```sql
-- 在全新练习库中可选执行一次；不是要求在生产建索引
CREATE INDEX idx_orders_customer_status_day
ON orders(customer_id, status, paid_day DESC, order_id DESC);
```

```sql
-- lab: indexed_customer_orders
SELECT order_id, paid_day, amount_cents
FROM orders
WHERE customer_id = 1 AND status = 'paid'
ORDER BY paid_day DESC, order_id DESC
LIMIT 3;
```

客户与状态固定后，索引顺序与查询顺序对齐，可能快速找到前三条。返回结果是 106、102、101。索引仍有空间与写入代价，不是因为语法正确就必须保留。

不同需求如“所有客户的某日销售额”未必适合同一个索引。等值、范围、排序、列选择度和实际负载应一起看。

## EXPLAIN：看方案而不是猜

**EXPLAIN（解释执行计划，读作 explain）** 显示数据库准备如何执行。

SQLite 的只读观察语句：

```sql
EXPLAIN QUERY PLAN
SELECT order_id FROM orders
WHERE customer_id = 1 AND status = 'paid'
ORDER BY paid_day DESC, order_id DESC LIMIT 3;
```

PostgreSQL 方言，在测试环境对只读查询可进一步使用：

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT order_id FROM orders
WHERE customer_id = 1 AND status = 'paid'
ORDER BY paid_day DESC, order_id DESC LIMIT 3;
```

**ANALYZE 在这里真的执行查询。** 不要随手对写语句、带副作用的函数或大负载查询执行。即使事务回滚能撤销表修改，也不一定撤销外部副作用或编号分配。MySQL 的 EXPLAIN ANALYZE 语法和输出不同。

| 计划信息 | 如何理解 |
|---|---|
| Seq Scan / 全表扫描 | 扫表不必然坏，小表或取大部分数据可能合理 |
| Index Scan / 索引访问 | 用了索引不必然快，仍可能读大量数据 |
| estimated rows 与 actual rows | 相差很大时考虑统计信息、偏斜或相关列 |
| loops | 节点重复执行次数，不要只看单次代价 |
| Sort、临时文件 | 排序是否大到需要落盘 |
| Buffers | 数据页缓存命中、读取等，不等于直接测到每次物理磁盘访问 |

PostgreSQL 估算 cost 是规划器的成本单位，不是毫秒；ANALYZE 的实际时间才是相应测量指标。父子节点耗时不能简单相加，重复循环也要考虑。

## JOIN 为什么也会慢

Nested Loop（嵌套循环）可理解为外侧每行去内侧找匹配，外侧很小且内侧有合适索引时很好；外侧很多且内侧反复扫大表时很贵。

Hash Join（哈希连接）先为一侧建立按关联键查找的结构；Merge Join（归并连接）利用两边有序输入向前匹配。实际能用哪些策略、内存不足怎么处理，由产品和条件决定。

不要把“子查询一定慢”“JOIN 一定快”当定律。CTE 主要帮助组织查询，是否内联或物化要看计划；SQL 文本短不代表工作少。

## 让过滤条件更容易利用索引

时间戳上常优先写范围：

```sql
WHERE paid_at >= :start_time AND paid_at < :end_time
```

这是参数表达示意，样例表只有 paid_day；占位符格式取决于驱动。相对 `DATE(paid_at) = ...`，直接范围常更容易利用普通时间列索引，也能清楚处理业务时区的起止时刻。

但“用了函数就绝对失去索引”也不对：产品可能支持匹配的表达式索引、生成列索引或相应优化。

同样需要注意：隐式类型转换、字符排序规则、前导通配符 `%关键词%`、不必要的 OR/去重，都可能改变计划。不要为了迎合口诀把 NULL 或比较语义改错。

## 深分页与游标分页

`OFFSET 1000000 LIMIT 20` 通常仍需处理/跳过很多前面的结果，页越深越可能贵。

如果页面按付款日期与订单号倒序，上一页末尾为 2026-08-04、106，可以从那个位置继续：

```sql
-- lab: keyset_page
SELECT order_id, paid_day
FROM orders
WHERE status = 'paid'
  AND (paid_day < '2026-08-04'
       OR (paid_day = '2026-08-04' AND order_id < 106))
ORDER BY paid_day DESC, order_id DESC LIMIT 3;
```

返回 105、103、102。唯一的 order_id 打破日期并列；排序列 NULL、排序值被修改、分页期间的新数据都要有策略。游标分页适合向后浏览，不天然支持直接跳第 5000 页，也不自动提供固定历史快照。

## 索引进阶与成本

- 唯一索引既支持查询，也参与阻止重复。
- 覆盖索引减少额外取行，但超宽索引会挤占缓存。
- 部分索引只索引满足条件的行，表达式索引按表达式结果索引；语法和优化条件有产品差异。
- PostgreSQL 的 `INCLUDE` 可以带上非排序键列，不等于这些列也能按同样方式定位。
- PostgreSQL 外键引用列不自动都建索引；MySQL InnoDB 的外键索引要求与行为不同，需分别检查。

建索引会用资源，也可能阻塞写入；“在线/并发建索引”有特定限制，并非零影响。删索引更应先验证其他业务是否依赖，不能只看这一条查询。

## SQL 之外的性能问题

**N+1 查询**：先取 N 个订单，再每单发一次客户查询，变成一次列表查询加 N 次请求。可以在保持结果粒度的前提下批量读取、预加载或合理关联；见 [[ORM]]。

连接池太小会等待，太大也可能压垮数据库。长事务造成锁等待与旧版本堆积；资源不足导致排序/哈希落盘；应用把百万行拉回内存再统计，浪费网络与内存。

统计信息更新、PostgreSQL autovacuum、MySQL 相应维护需要纳入监控。分区主要帮助符合条件的分区裁剪与生命周期管理，不是所有查询的自动加速；主从读扩展也不能解决同一个热点写锁。

## 一份优化验收清单

1. 修改前后行数、金额、排序、NULL 和权限语义相同。
2. 使用代表性数据与参数，含热点、冷门和边界值。
3. 同时看单次耗时、吞吐、尾延迟、写入开销与空间。
4. 查看实际计划，而不只看“创建索引成功”。
5. 有监控、回退方式和上线影响评估。

学习建议：在练习库中看一次建索引前后计划并核对结果不变；需要讨论规模性能时再准备独立、可控的大数据实验。

关联：[[SQL事务、锁与并发一致性]]、[[SQL复杂统计与报表设计]]、[[数据库事务日志、主从复制与故障恢复]]。

## 参考资料

核对日期：2026-09-08。

- [PostgreSQL：使用 EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL：多列索引](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [PostgreSQL：部分索引](https://www.postgresql.org/docs/current/indexes-partial.html)
- [PostgreSQL：表达式索引](https://www.postgresql.org/docs/current/indexes-expressional.html)
- [SQLite：EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)
- [MySQL 8.4：优化与索引](https://dev.mysql.com/doc/refman/8.4/en/optimization-indexes.html)
