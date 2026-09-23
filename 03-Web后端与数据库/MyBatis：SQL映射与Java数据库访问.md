---
title: MyBatis：SQL映射与Java数据库访问
aliases:
  - MyBatis
  - SQL Mapper
tags:
  - Java
  - 数据库
  - MyBatis
created: 2026-09-23
updated: 2026-09-23
verified: 2026-09-23
---

# MyBatis：SQL映射与Java数据库访问

## 一句话解释

**MyBatis 是以 SQL 映射为核心的 Java 持久化框架：开发者掌握查询语句，它帮助绑定参数、执行数据库访问，并把查询结果转换成 Java 对象。**

MyBatis 近似读“麦巴蒂斯”，是项目名称，不是缩写。**SQL = Structured Query Language，结构化查询语言**，可读 S-Q-L，用于查询和修改关系型数据库中的数据。

“持久化”是让数据保存下来，而不是只留在程序运行时的临时内存中。MyBatis 帮助程序访问数据库，实际存储由数据库完成。生活类比：它像懂业务单据和数据库表格两套格式的办事员，不是存放账本的仓库。

## 它解决什么重复工作

Java 通常可通过 **JDBC = Java Database Connectivity，Java 数据库连接接口**（读 J-D-B-C）配合数据库驱动访问关系型数据库。直接使用时，开发者需要处理语句、参数和结果读取等细节。

MyBatis 在这些基础上提供映射机制，减少重复代码；语句和映射可以通过注解或配置描述。**XML = Extensible Markup Language，可扩展标记语言**，读 X-M-L，是一种用标签表达结构的文本格式，MyBatis 可用它编写映射配置。[MyBatis 官方介绍](https://mybatis.org/mybatis-3/index.html)

## 查询一个订单时发生什么

```text
业务代码调用 OrderMapper 的查询方法，传入订单编号
→ MyBatis 找到对应 SQL 和参数映射
→ 通过 JDBC 与数据库驱动发送查询
→ 数据库返回记录
→ MyBatis 按规则组装 Java 对象
→ 业务代码使用查询结果
```

**Mapper（映射器）**近似读“麦珀”，通常体现为接口与其关联的语句、映射规则；它不是数据库表，也不是负责接收网页请求的 Controller。

例如映射语句可以是：

```sql
SELECT id, status FROM orders WHERE id = #{id}
```

这是 **MyBatis 模板片段**，不是直接发给数据库执行的原始 SQL；`#{id}` 通常会被处理成预编译语句的参数占位，再绑定传入值。查询结果中的 `id`、`status` 可以映射到订单对象相应字段。[MyBatis 映射文件说明](https://mybatis.org/mybatis-3/sqlmap-xml.html)

本例仅解释机制：没有创建订单表、连接数据库或执行查询。完整项目还需要映射配置、对象定义、数据源和驱动。

## 与 ORM 有什么区别

**ORM = Object-Relational Mapping，对象关系映射**，逐字母读 O-R-M，详见 [[ORM]]。

- 较完整的 ORM 常围绕对象关系描述生成许多常见查询，并管理对象与数据库之间的关系。
- MyBatis 更强调开发者指定 SQL，再映射参数和结果；复杂查询的写法和优化仍主要由开发者掌握。
- 中文教程有时称它“半自动 ORM”，可用于入门类比，但“SQL 映射／持久化框架”更明确，不意味着它只会一半功能。

不能把 MyBatis 简单理解为“完全不用 SQL”，也不能认为用了它就自动创建业务表或维护表结构迁移。部分扩展工具会提供额外能力，应与 MyBatis 核心本身区分。

## 常见误区与边界

- **参数占位不是文本拼接**：`#{...}` 通常绑定参数值；`${...}` 属于直接文本替换，不能把不可信输入随意拼进去。表名、排序列等动态标识符需要受控映射或允许列表，不能只靠值参数绑定解决。
- MyBatis 不会替你设计正确的表结构、索引或事务边界，关联 [[关系型数据库设计：建模、约束与范式]]、[[SQL索引、执行计划与性能优化]]、[[SQL事务、锁与并发一致性]]。
- 数据库连接池、事务管理、权限检查需要正确配置和实现；不是接口能查询成功就说明生产环境安全可靠。
- MyBatis 可独立使用，也可整合进 Spring；它不是 Spring Boot 自带数据库的一部分。

## 学习建议与关联概念

先学基本 SQL，再理解 JDBC 的连接与参数化查询，最后学 Mapper、结果映射和事务整合。先写一条按编号查订单的语句，再对比它如何变成 Java 对象，避免一上来背大量配置。

整套协作见 [[Spring、Spring Boot、Spring MVC与SSM：Java后端框架关系]]；依赖获取和构建见 [[Maven：Java项目构建与依赖管理]]；数据库本身的区别见 [[SQLite、SQLCipher与PostgreSQL]]。

## 参考资料

核对日期：2026-09-23。

- [MyBatis Introduction](https://mybatis.org/mybatis-3/index.html)：框架定位。
- [Mapper XML Files](https://mybatis.org/mybatis-3/sqlmap-xml.html)：语句、参数与结果映射。
- [MyBatis-Spring](https://mybatis.org/spring/)与 [Spring Boot 集成](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/)：与 Spring 应用协作。
