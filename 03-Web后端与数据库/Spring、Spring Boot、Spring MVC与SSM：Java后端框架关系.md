---
title: Spring、Spring Boot、Spring MVC与SSM：Java后端框架关系
aliases:
  - Spring
  - Spring Boot
  - SpringBoot
  - Spring MVC
  - SpringMVC
  - SSM
  - SSM框架
tags:
  - Java
  - Web后端
  - Spring
  - 技术栈
created: 2026-09-23
updated: 2026-09-23
verified: 2026-09-23
---

# Spring、Spring Boot、Spring MVC与SSM：Java后端框架关系

## 一句话解释

**Spring 提供应用组件管理等基础能力，Spring MVC 处理 Web 请求，Spring Boot 简化 Spring 应用的配置和启动；SSM 则通常指 Spring、Spring MVC、MyBatis 这三个框架的组合，而不是第四个独立框架。**

Spring 近似读“斯普林”，Boot 读“布特”。它们是项目名称，不需要按缩写展开。先理解 [[Java SE、JDK与JVM：Java基础平台]]。

## 把整套 Java 技术放到正确位置

| 名称 | 所在层次 | 回答的问题 |
| --- | --- | --- |
| Java SE | 基础平台 | 用什么基础语言与标准能力写程序 |
| Spring Framework | 应用基础框架 | 对象怎样创建、装配，事务等通用能力怎样接入 |
| Spring MVC | Web 框架，属于 Spring Framework | 请求由谁接收，参数怎样处理，结果怎样返回 |
| Spring Boot | 简化配置、启动与运维接入的框架 | 怎样方便地组装和运行 Spring 应用 |
| MyBatis | 数据访问框架 | 怎样执行 SQL 并将结果映射为 Java 对象 |
| Maven | 构建与依赖管理工具 | 依赖如何获取，代码如何编译、测试和打包 |
| SSM | 框架组合称呼 | Spring、Spring MVC、MyBatis 怎样协作 |

生活类比：Java SE 是基础工具，Spring 是组织人员和设备的管理系统，Spring MVC 是接待窗口，MyBatis 是访问账本的工作人员，Spring Boot 是一套省去重复准备工作的开业方案，Maven 是物料采购与构建工具。类比只帮助记忆，不表示框架会自动完成业务。

## 一、Spring：先理解被 Boot 和 MVC 共用的基础

这里的 Spring 主要指 **Spring Framework**，而不是整个 Spring 项目家族。其核心能力之一是管理对象之间的关系。

例如订单业务对象需要一个数据库访问对象。程序可以到处自己创建对象，也可以把创建与装配交给 Spring：

- **IoC = Inversion of Control，控制反转**，读 I-O-C：对象创建等控制职责由容器统一承担，而不是每个业务对象自己找齐所有依赖。
- **DI = Dependency Injection，依赖注入**，读 D-I：容器把某对象需要的协作对象交给它，例如通过构造方法传入。
- **Bean**，读“宾”：在 Spring 中指由容器创建、装配和管理的对象，不是数据库里的记录。

Spring 还提供事务管理等能力，但业务逻辑、权限规则和事务边界仍要开发者定义。这个容器是应用内部的对象管理机制，不是 Docker 那种进程隔离容器。[Spring 容器说明](https://docs.spring.io/spring-framework/reference/core/beans/introduction.html)，关联 [[Docker容器与DI容器：运行隔离和对象装配]]。

## 二、Spring MVC：接收和响应 Web 请求

**MVC = Model–View–Controller，模型—视图—控制器**，逐字母读 M-V-C，是一种职责划分思想，不是 Java 专属。

- **Model（模型）**：用于业务处理或展示的数据及相关模型，不应简单等同于数据库本身。
- **View（视图）**：把结果呈现给用户的部分，例如服务端生成的网页。
- **Controller（控制器）**：接收请求、处理输入、调用业务逻辑，再决定怎样返回结果。

Spring MVC 是基于 Servlet 的 Web 框架。Servlet 可先理解为 Java 服务端处理 Web 请求的标准组件；Tomcat 等 Servlet 容器负责承载它。Spring MVC 用 `DispatcherServlet` 作为统一请求入口，再根据路径等条件找到实际控制器。[Spring MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html)、[DispatcherServlet](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html)

例如浏览器请求 `GET /orders/1001`：GET 表示读取资源，路径表示查询编号为 1001 的订单。这里使用 **HTTP = Hypertext Transfer Protocol，超文本传输协议**，读 H-T-T-P，详见 [[TCP、HTTP、HTTPS与WebSocket]]。

控制器把编号交给业务层处理，再返回结果。前后端分离时，常返回 **JSON = JavaScript Object Notation，JavaScript 对象表示法**，常读“杰森”；它是一种跨语言数据格式，不要求服务端使用 JavaScript：

```json
{"id": 1001, "status": "PAID"}
```

这表示订单编号与已支付状态。Spring MVC 可以通过消息转换器把对象写成 JSON 响应；这种方式不需要服务端页面模板，也不等于使用了前端 React。[Boot 文档中的消息转换与 MVC 说明](https://docs.spring.io/spring-boot/reference/web/servlet.html)

## 三、Spring Boot：减少搭建 Spring 应用的重复工作

Spring Boot 基于 Spring 生态，主要帮助：

1. 用 **Starter（起步依赖组合）**集中引入某类功能所需的常见依赖。
2. 根据已有依赖、配置和组件等条件进行**自动配置**，并允许开发者替换或调整。
3. 简化应用启动；Web 应用可以使用内嵌服务器，不必每次都单独安装和配置外部容器。
4. 组织外部配置，并提供可按需接入的健康检查、指标等运行管理能力。

“内嵌服务器”不是没有服务器，而是相关服务组件随应用一起启动。“自动配置”不是读懂需求后自动写订单系统；数据库地址、业务逻辑、权限、测试和生产部署仍要自己处理。[Spring Boot](https://spring.io/projects/spring-boot/)、[自动配置](https://docs.spring.io/spring-boot/reference/using/auto-configuration.html)

**Spring Boot 没有取代 Spring MVC。**一个 Boot Web 项目完全可以用 MVC 处理请求，并用 MyBatis 访问数据库。Boot 也不限于 MVC Web 项目，不必在每个 Boot 应用中引入数据库。[Boot 对 MVC 的自动配置](https://docs.spring.io/spring-boot/reference/web/servlet.html)

## 四、SSM：三个框架组成的技术栈

**SSM = Spring + Spring MVC + MyBatis**，逐字母读 S-S-M。这是常见组合简称，不是带统一版本号的第四个框架。

- Spring：管理组件，整合事务等基础能力。
- Spring MVC：处理 Web 请求与响应。
- MyBatis：处理 SQL 与对象映射，详见 [[MyBatis：SQL映射与Java数据库访问]]。

“传统 SSM 项目”往往指开发者显式整合这几部分的项目；但不能把它定义成“只能用配置文件”，也不能说必须全部手工编写大量配置。Spring 支持多种配置方式，MyBatis 也有与 Spring 集成的组件。[MyBatis-Spring](https://mybatis.org/spring/)

Spring Boot 可以简化这些组件的整合，因此“SSM 被 Boot 完全替换”不准确：Boot 项目里仍可能使用这三者，只是配置和启动方式改变。MyBatis 官方也提供 [Spring Boot 集成组件](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/)。

## 五、一次查询订单请求，谁负责哪一段

```text
浏览器或手机发起请求
→ 服务端接收请求，例如内嵌 Tomcat
→ Spring MVC 找到 OrderController（请求入口）
→ OrderService 执行业务逻辑与必要的权限检查
→ MyBatis 的 OrderMapper 执行参数化查询
→ 数据库查找订单并返回记录
→ MyBatis 映射结果，业务层整理数据
→ Spring MVC 返回 JSON
→ 前端显示订单
```

Controller、Service、Mapper 是常见分层叫法，不是三台服务器，也不要求每个简单项目都机械地拆成三层。

Spring 管理其中需要的组件及其装配；Spring Boot 帮助应用配置和启动；Java 平台提供基础运行能力。**Maven 主要在构建阶段工作，不是每次订单请求都要经过的业务中间站。**

数据库才负责实际保存和查询数据。订单是否存在、用户是否有权查看、返回哪些字段，都不能仅靠装上框架自动保证。

## 六、学习路线与常见误区

建议路线：[[Java SE、JDK与JVM：Java基础平台|Java 基础]] → [[Maven：Java项目构建与依赖管理|Maven 基本使用]] → HTTP 与 [[SQL与关系型数据库学习地图|SQL 基础]] → 理解 Spring 的依赖注入 → 用 Boot 做一个 MVC 接口 → 用 MyBatis 接入数据库 → 补事务、测试、权限与部署。

这条路线是入门建议，不是必须的课程标准。可以先用 Boot 跑通小例子，再逐步理解底层；不必先背完所有旧式 SSM 配置。

- Spring Boot 不是编程语言，也不是专门负责画网页的工具。
- MVC 不等于 Controller、Service、Mapper 三层；这是两种不同的划分角度。
- MyBatis 不是数据库，Maven 也不是 Web 服务器。
- 用了 Boot 不会自动获得高并发、安全和完整运维，关联 [[Java为什么适合高并发]]、[[开发、测试、预发布与生产环境]]。
- 版本不能随意混搭：JDK、Spring Boot、Spring Framework、MyBatis 集成组件应满足各自的兼容要求。

## 参考资料

核对日期：2026-09-23。本文解释职责，不指定“最新版本”；具体依赖名称和兼容矩阵以所用版本文档为准。

- [Spring Framework 概览](https://docs.spring.io/spring-framework/reference/overview.html)与 [容器介绍](https://docs.spring.io/spring-framework/reference/core/beans/introduction.html)。
- [Spring MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html)与 [请求分发入口](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html)。
- [Spring Boot](https://spring.io/projects/spring-boot/)、[自动配置](https://docs.spring.io/spring-boot/reference/using/auto-configuration.html)、[Servlet Web 应用](https://docs.spring.io/spring-boot/reference/web/servlet.html)。
- [MyBatis-Spring](https://mybatis.org/spring/)与 [MyBatis Spring Boot Starter](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/)。
