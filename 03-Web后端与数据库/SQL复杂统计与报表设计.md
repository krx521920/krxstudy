---
title: SQL 复杂统计与报表设计
aliases: [SQL复杂统计, SQL报表, 统计口径]
tags: [数据库, SQL, 数据分析, 报表]
created: 2026-09-08
updated: 2026-09-08
verified: 2026-09-08
---

# SQL 复杂统计与报表设计

> [!summary] 一句话解释
> 复杂统计是把多张表按明确业务口径变成可信指标；最难的通常不是函数，而是避免重复、漏算和时间含义混乱。

像做家庭账本：买东西 100 元、后来退回 20 元，“消费额”可以指原始 100，也可以指净额 80。没约定口径，两份都能执行的 SQL 可能回答的是不同问题。

本篇使用 [[SQL订单实战：样例数据与练习]]。基础见 [[SQL基础查询与多表关联]]。

## 写查询前先写指标合同

| 要明确的内容 | 本例约定 |
|---|---|
| 统计对象 | 已付款订单，不含待付款和取消订单 |
| 金额单位 | 存储为整数分，展示时除以 100.0 |
| 时间窗口 | 2026-08-01 含起点，2026-08-08 不含终点 |
| 时间字段 | 付款额按 paid_day，退款按 refund_day |
| 去重单位 | 订单数按订单；买家数按 customer_id |
| 退款状态 | 样例 refunds 只含成功退款 |
| 数据截止 | 所有演示结果以样例这批数据为准 |

“付款总额”“订单净额”“期间净流入”“会计确认收入”不是天然相等。样例用的净额不含手续费、税费、结算在途等，不能直接当正式财务报表。

## 条件聚合：一次扫描算几种状态

```sql
-- lab: status_summary
SELECT COUNT(*) AS all_orders,
       SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) AS paid_orders,
       SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_orders,
       SUM(CASE WHEN status = 'paid' THEN amount_cents ELSE 0 END) AS paid_cents
FROM orders;
```

结果：10 条订单、7 条付款、2 条待付款、82000 分付款额。`CASE` 像给每行贴分类标签，再按标签求和。

```sql
-- lab: order_metrics
SELECT COUNT(*) AS paid_orders,
       COUNT(DISTINCT customer_id) AS buyers,
       SUM(amount_cents) / 100.0 AS gross_yuan,
       SUM(amount_cents) / 100.0 / NULLIF(COUNT(*), 0) AS average_order_yuan
FROM orders WHERE status = 'paid';
```

结果为 7 单、3 位买家、820 元，平均每单约 117.14 元。`NULLIF(x, 0)` 把分母 0 变成 NULL，避免除零；`100.0` 有助于避免整除截断。此处“平均每单”不等于“平均每个买家”。

## 多表统计最危险的坑：关联放大

订单 101 有两行商品、两笔退款。如果同时直接关联，组合变成 2 × 2 = 4 行：

```sql
-- lab: fanout_wrong
-- 故意展示错误算法，不能拿来做真实报表
SELECT COUNT(*) AS joined_rows, SUM(o.amount_cents) AS wrong_total
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN refunds r ON r.order_id = o.order_id
WHERE o.order_id = 101;
```

返回 4 行、60000 分，而这笔订单只有 15000 分。`SUM(DISTINCT amount_cents)` 不是可靠补丁，因为不同订单可能金额相同。

原则：**先把每个一对多来源汇总到相同粒度，再关联。**

```sql
-- lab: net_order_total
WITH refund_per_order AS (
  SELECT order_id, SUM(amount_cents) AS refund_cents
  FROM refunds
  WHERE refund_day < '2026-08-08'
  GROUP BY order_id
)
SELECT SUM(o.amount_cents) AS gross_cents,
       SUM(COALESCE(r.refund_cents, 0)) AS refund_cents,
       SUM(o.amount_cents - COALESCE(r.refund_cents, 0)) AS net_cents
FROM orders o
LEFT JOIN refund_per_order r ON r.order_id = o.order_id
WHERE o.status = 'paid'
  AND o.paid_day >= '2026-08-01' AND o.paid_day < '2026-08-08';
```

结果为 82000、5000、77000 分。每个订单最多匹配一条退款汇总，所以不会重复付款金额。这是“该期间付款订单截至截止日的净额”；如果要算“本月现金流”，应分别按本月付款和本月退款统计，退款可能对应上个月的订单。

## 日报：没有成交的日期也要出现

```sql
-- lab: daily_report
WITH daily AS (
  SELECT paid_day, COUNT(*) AS paid_orders, SUM(amount_cents) AS cents
  FROM orders WHERE status = 'paid'
  GROUP BY paid_day
)
SELECT c.day, COALESCE(d.paid_orders, 0) AS paid_orders,
       COALESCE(d.cents, 0) AS cents
FROM calendar c LEFT JOIN daily d ON d.paid_day = c.day
ORDER BY c.day;
```

7 天付款额依次为 150、250、0、320、0、100、0 元。日期表像空白日历，先保留每天，再填数字。没有日期的原始分组结果不能直接用于“前一天”和“最近七个自然日”的计算。

日期 × 城市可以用 CROSS JOIN 构造完整网格，但要先估算组合规模。缺失是零成交还是导入失败，需质量监控判断，不能一概补零。

## 多维统计与交叉报表

```sql
-- lab: category_report
SELECT p.category, SUM(i.quantity * i.unit_price_cents) AS gross_cents
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN products p ON p.product_id = i.product_id
WHERE o.status = 'paid'
GROUP BY p.category ORDER BY p.category;
```

外设 80000 分，配件 2000 分。这里应加总明细金额，不能把整笔订单额分配给每个商品。要按品类扣退款，必须知道退款对应哪些商品或有明确分摊规则；现有退款表只到订单粒度，不能凭空得出品类净额。

交叉报表“每行一个城市、每列一种状态”可用条件聚合实现。列是动态类别时，还需要应用层或产品专用的透视功能，不要假设 SQL 会自动生成任意新列。

以下为 **PostgreSQL 方言**，同时生成城市明细和总计：

```sql
SELECT c.city, GROUPING(c.city) AS is_total, SUM(o.amount_cents) AS cents
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'paid'
GROUP BY GROUPING SETS ((c.city), ());
```

`GROUPING SETS` 指定几套汇总层级；`ROLLUP` 常用来做层级小计。`GROUPING` 区分总计产生的空值和原始数据本身的 NULL。不是所有数据库都支持同样语法。

## 平均值、比例、中位数

- 总体平均客单价 = 总金额 ÷ 总订单数，不能直接平均各城市的平均值，除非各城市订单数相同。
- 总体转化率 = 合适的转化人数 ÷ 合适的到达人数，不能直接平均每天百分比。
- 去重人数不可随意相加：同一人可能连续两天付款。
- 中位数看排序后中间位置，比均值更不易被极端大额带偏；样例付款订单中位数为 120 元。

PostgreSQL 中位数例子：

```sql
SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY amount_cents) / 100.0
FROM orders WHERE status = 'paid';
```

这不是所有数据库都有的函数。金额严格计算仍应注意结果类型与舍入；此处只演示统计指标。

## 复购、留存、漏斗与同期比较

复购示例可定义为“本时间窗口内付款至少两次的买家数 ÷ 窗口内付款买家数”。样例 3/3 = 100%，但这不代表商店长期复购率；样本极小，定义也不同于“首次购买后 30 天再购买”。

留存通常先按首次发生行为的月份分组，再看后续月份是否继续活跃；需要足够观察期，不能把还没到第 30 天的人当流失。

漏斗如访问 → 加购 → 付款，需要用户标识、事件时间和顺序规则。订单表没有浏览事件，因此不能仅靠这份样例算真实访问转化率。

环比通常与上一相邻期间比，同比与去年相同期间比；增长率为 `(本期 - 对比期) / 对比期`。对比期为零、缺失、不完整月时要明确呈现规则。SQL 写法见 [[SQL窗口函数：排名、累计与同期比较]]。

## 报表交付还要考虑什么

**BI = Business Intelligence（商业智能，读作 B-I）**，指围绕数据整合、分析、可视化支持决策的一类能力与工具。图画得漂亮只是其中一环。

报表应写明指标定义、时区、更新时间、来源、权限和对账结果。实时仪表盘与结算报表可能采用不同刷新和冻结政策；迟到退款、补录订单会改变历史数据。

普通视图保存查询定义，不等于保存计算结果；物化视图或汇总表保存结果，需要刷新策略。重查询可进入分析库，避免影响在线下单。导出个人信息必须遵守访问范围，不要因为“只是 Excel”就绕过权限。

学习建议：先手算 7 天金额与 3 个客户金额，解释 JOIN 前后行数，再做累计和同比。所有优化都应保留同一业务口径。

关联：[[SQL数据清洗与质量校验]]、[[关系型数据库设计：建模、约束与范式]]、[[SQL索引、执行计划与性能优化]]。

## 参考资料

核对日期：2026-09-08。

- [PostgreSQL：聚合函数](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [PostgreSQL：分组、ROLLUP 与 GROUPING SETS](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-GROUPING-SETS)
- [PostgreSQL：物化视图](https://www.postgresql.org/docs/current/rules-materializedviews.html)
