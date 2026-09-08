---
title: SQL 窗口函数：排名、累计与同期比较
aliases: [窗口函数, ROW_NUMBER, SQL排名, SQL累计]
tags: [数据库, SQL, 数据分析]
created: 2026-09-08
updated: 2026-09-08
verified: 2026-09-08
---

# SQL 窗口函数：排名、累计与同期比较

> [!summary] 一句话解释
> 窗口函数在保留每一行明细的同时，参考与它相关的一组行，计算排名、累计、前后差值等结果。

像老师在每个学生的成绩旁边添上“班级平均分、班内排名”：学生没有被合并成一行，只是每行多了基于全班的信息。

数据来自 [[SQL订单实战：样例数据与练习]]；先读 [[SQL基础查询与多表关联]]。

## GROUP BY 和窗口的区别

`GROUP BY customer_id` 通常把该客户的多笔订单汇总成一行；`SUM(...) OVER (PARTITION BY customer_id)` 可以保留订单明细，同时附上该客户合计。

```sql
-- lab: share_of_customer
SELECT order_id, customer_id, amount_cents,
       SUM(amount_cents) OVER (PARTITION BY customer_id) AS customer_total
FROM orders WHERE status = 'paid'
ORDER BY customer_id, order_id;
```

客户 1 的订单 101、102、106 每行都会显示客户合计 40000 分。若要算订单占客户金额比例，用订单金额除以该合计，注意零分母和数值类型。

## 看懂 OVER 的三个部分

```sql
SUM(amount_cents) OVER (
  PARTITION BY customer_id
  ORDER BY paid_day, order_id
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

- `PARTITION BY`：按谁分区，类似先把学生分到不同班级；不写则所有输入行算一组。
- 窗口内 `ORDER BY`：以什么顺序计算；不是最终展示顺序。
- 窗口框架 `ROWS ...`：在分区内，当前行实际参考哪些行；这里是从第一行到当前行。

`OVER` 把支持窗口使用的函数与一份窗口定义连接起来。不是每个函数都能随意加 OVER。

## 三种排名：并列怎么处理

```sql
-- lab: ranks
SELECT order_id, amount_cents,
       ROW_NUMBER() OVER (ORDER BY amount_cents DESC, order_id) AS row_no,
       RANK() OVER (ORDER BY amount_cents DESC) AS rank_no,
       DENSE_RANK() OVER (ORDER BY amount_cents DESC) AS dense_no
FROM orders WHERE status = 'paid'
ORDER BY amount_cents DESC, order_id;
```

金额序列为 20000、20000、15000、12000、5000、5000、5000 分。

| 函数 | 本例排名序列 | 用途 |
|---|---|---|
| ROW_NUMBER | 1、2、3、4、5、6、7 | 每行唯一序号，确定性取 N 行 |
| RANK | 1、1、3、4、5、5、5 | 并列后留空位，如竞赛排名 |
| DENSE_RANK | 1、1、2、3、4、4、4 | 并列后不留空位，前 N 个分数档 |

`ROW_NUMBER` 用 order_id 打破同额并列，结果稳定；RANK 的窗口故意不加唯一 ID，否则同金额也不再并列。这两个目标不要混用。

## 每个客户最新一笔付款订单

```sql
-- lab: latest_per_customer
WITH numbered AS (
  SELECT order_id, customer_id,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id ORDER BY paid_day DESC, order_id DESC
         ) AS rn
  FROM orders WHERE status = 'paid'
)
SELECT customer_id, order_id FROM numbered
WHERE rn = 1 ORDER BY customer_id;
```

结果是客户 1→106、2→108、3→109。先在每个客户内部编号，再取第 1 行。普通 WHERE 在窗口计算之前执行，不能直接在同一层写 `WHERE rn = 1`；使用 CTE 或子查询。部分产品有专用筛选窗口结果的语法，但不通用。

把 `rn = 1` 改为 `rn <= 2` 就是每人最多两笔。若要求保留所有边界并列，要选合适的 RANK/DENSE_RANK，并接受可能超过 N 行。

## 每个客户的累计消费

```sql
-- lab: customer_running
SELECT order_id, customer_id,
       SUM(amount_cents) OVER (
         PARTITION BY customer_id ORDER BY paid_day, order_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_cents
FROM orders WHERE status = 'paid'
ORDER BY customer_id, paid_day, order_id;
```

客户 1 的累计依次是 15000、20000、40000 分。显式写 ROWS 和唯一排序条件，是想“一笔一笔加”，而不是一次把同一天所有订单合进去。

## ROWS、RANGE 与默认框架

`ROWS` 按排序后的行位置确定边界；`RANGE` 按排序值及其同值行确定边界，具体可用的偏移类型因数据库而异。

许多常用实现中，聚合窗口有 ORDER BY、未写框架时，默认从分区开始到当前排序值的同值组末尾。因此 `ORDER BY paid_day` 下同一天几笔订单可能显示同一个累计值。这不是随机出错，而是框架语义不同。

`LAST_VALUE` 也受框架影响：默认框架下可能得到“当前框架的最后值”，不一定是整组最后值。要取整组最后值，应考虑：

```sql
LAST_VALUE(amount_cents) OVER (
  PARTITION BY customer_id ORDER BY paid_day, order_id
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

这是表达式片段，不是可单独执行的 SELECT。排名函数和 LAG/LEAD 等并不都按聚合窗口那样使用框架；不能给所有窗口函数套同一规则。

## LAG、LEAD：取前一行和后一行

`LAG` 取前面的行，`LEAD` 取后面的行；它们常用于前后比较，名称分别有“滞后、领先”的意思。

```sql
-- lab: daily_lag
WITH daily AS (
  SELECT c.day, COALESCE(SUM(o.amount_cents), 0) AS cents
  FROM calendar c LEFT JOIN orders o
    ON o.paid_day = c.day AND o.status = 'paid'
  GROUP BY c.day
), compared AS (
  SELECT day, cents, LAG(cents) OVER (ORDER BY day) AS previous_cents
  FROM daily
)
SELECT day, cents, previous_cents,
       1.0 * (cents - previous_cents) / NULLIF(previous_cents, 0) AS growth_rate
FROM compared ORDER BY day;
```

8 月 2 日相对 1 日增长约 0.6667，即 66.67%；第一天没有对照，显示 NULL；前一天是零时增长率也为 NULL，不能编造“增长无穷倍”。

这里先补齐日历，LAG 一行才等于前一个自然日。月度同比可以在连续且唯一的月序列上用 LAG 12，但缺月时不能这么直接用；按明确上年月份关联通常更容易检查。闰日、财务周期还需要业务规则。

## 最近七个自然日的移动平均

```sql
-- lab: rolling_week
WITH daily AS (
  SELECT c.day, COALESCE(SUM(o.amount_cents), 0) AS cents
  FROM calendar c LEFT JOIN orders o
    ON o.paid_day = c.day AND o.status = 'paid'
  GROUP BY c.day
)
SELECT day,
       SUM(cents) OVER (ORDER BY day ROWS UNBOUNDED PRECEDING) AS cumulative_cents,
       COUNT(*) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS days_used,
       AVG(cents) OVER (ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) / 100.0 AS avg_yuan
FROM daily ORDER BY day;
```

8 月 7 日的七日平均是 820÷7≈117.14 元。前六天实际窗口不足七天，因此同时输出 days_used，避免把“不完整观察窗口”包装成完整七日均值。

`6 PRECEDING` 加当前行是最多 7 行，不是 6 行。如果要输出区间从 8 月 7 日开始的七日均值，内层必须包含之前六天，不能先把这些历史行过滤掉。

## 常见误区与学习建议

- 窗口 ORDER BY 不保证输出顺序，外层仍要 ORDER BY。
- 分区列选错会混合不同客户、不同币种的数据。
- 先 WHERE 再窗口，意味着窗口看不到已被筛掉的行。
- 窗口依赖排序和分区，也会耗内存、可能落盘；不是自动加速器。
- 不应在同一表达式层直接嵌套窗口函数；先用子查询或 CTE 算出中间结果。

学习顺序：客户合计 → 排名并列 → 每组最新 → 逐笔累计 → 补日历 → 环比和移动平均。每一步先预测输出，再运行。

相关：[[SQL复杂统计与报表设计]]、[[SQL数据清洗与质量校验]]、[[SQL索引、执行计划与性能优化]]。

## 参考资料

核对日期：2026-09-08。

- [PostgreSQL：窗口函数入门](https://www.postgresql.org/docs/current/tutorial-window.html)
- [PostgreSQL：窗口函数与框架注意事项](https://www.postgresql.org/docs/current/functions-window.html)
- [SQLite：窗口函数与框架](https://www.sqlite.org/windowfunctions.html)
- [MySQL 8.4：窗口函数](https://dev.mysql.com/doc/refman/8.4/en/window-functions.html)
