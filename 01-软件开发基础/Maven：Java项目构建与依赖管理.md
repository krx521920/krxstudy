---
title: Maven：Java项目构建与依赖管理
aliases:
  - Maven
  - Apache Maven
  - pom.xml
tags:
  - Java
  - 构建工具
  - 依赖管理
created: 2026-09-23
updated: 2026-09-23
verified: 2026-09-23
---

# Maven：Java项目构建与依赖管理

## 一句话解释

**Maven 是常用于 Java 项目的构建与依赖管理工具，帮助获取依赖，并按统一规则编译、测试和打包代码；它不是编程语言、数据库或处理网页请求的服务器。**

Maven 近似读“梅文”，是项目名称，不是缩写。生活类比：它像项目的物料采购与生产流程管理工具，既知道需要哪些零件，也知道怎样把源码加工成可交付文件。[Maven 官方介绍](https://maven.apache.org/what-is-maven.html)

## 依赖管理：别人写好的代码怎样进入项目

项目可能依赖 Spring、MyBatis 和数据库驱动。Maven 根据声明从配置的仓库解析和获取它们，也处理这些包继续需要的**传递依赖**。

Java 库常以 **JAR = Java Archive，Java 归档文件**形式分发，读“加尔”；可把它理解为装着字节码、资源和元数据的包。不是每个 JAR 都能直接启动运行。

常见依赖坐标包含三部分：

| 字段 | 含义 | 虚构示例 |
| --- | --- | --- |
| groupId | 项目或组织分组标识 | `com.example` |
| artifactId | 具体制品名称 | `course-tools` |
| version | 所选版本 | `1.2.3` |

**Artifact（制品）**指构建或发布出来的产物。坐标用于定位制品，不是对发布者信誉或代码安全的认证。

Maven 使用本地仓库保存获取或本地安装的制品，也可以连接公共或企业内部仓库。发生版本冲突时，有对应的解析和管理规则，不是简单“永远选最新”。[依赖机制](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)

## pom.xml 是什么

**POM = Project Object Model，项目对象模型**，可读“坡姆”或逐字母读 P-O-M；`pom.xml` 是 Maven 项目的核心描述文件。

**XML = Extensible Markup Language，可扩展标记语言**，读 X-M-L。`pom.xml` 用这种文本格式描述项目坐标、依赖、插件、构建配置等，也可以继承父项目配置。[POM 官方介绍](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html)

需要区分：

- `dependencies`：声明项目需要的依赖。
- `dependencyManagement`：集中规定依赖采用哪些版本等规则，单独写在这里通常不会自动把依赖加入项目。
- 构建插件：在编译、测试、打包等阶段执行具体工作，与业务运行依赖不是完全相同的角色。

Spring Boot 可提供一组协调过的依赖版本管理，但不是所有第三方库都自动受其管理，也不表示可以任意混搭版本。

## 构建：把源码变成可交付产物

Maven 通过生命周期阶段和绑定的插件任务组织工作。常见顺序可简化为：

```text
检查项目 → 编译源码 → 测试 → 打包 → 验证 → 安装到本地仓库 → 发布到远程制品仓库
```

执行某个阶段，通常会先执行该生命周期中它之前的阶段及相应绑定任务；是否跳过测试等取决于配置和命令参数。不是每个项目都需要运行到最后一步。[构建生命周期](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)

| 常见命令 | 含义 |
| --- | --- |
| `mvn compile` | 编译项目主代码及相应前置处理 |
| `mvn test` | 运行测试阶段及前置处理；实际测试取决于配置 |
| `mvn package` | 执行到打包阶段，生成项目定义的产物 |
| `mvn install` | 执行到本地安装阶段，把项目制品放进本地 Maven 仓库 |
| `mvn deploy` | 执行到发布阶段，向配置的远程制品仓库发布 |

**`install` 不是把网站安装到操作系统里，`deploy` 也不是自动把网站上线运行。**制品发布和应用部署是不同流程。

另一个常见命令 `mvn clean` 属于清理生命周期，会清理配置的构建输出，通常包括 `target` 目录，不是只读检查。本节命令只用于解释，本次没有执行构建、清理、下载依赖或发布制品。

## 它与 Spring Boot、pnpm 的关系

- [[Spring、Spring Boot、Spring MVC与SSM：Java后端框架关系|Spring Boot]] 主要帮助组织、配置和运行应用；Maven 主要管理这个项目怎样获取依赖和完成构建。
- 一个 Boot 项目可以使用 Maven，也可以使用其他兼容构建工具，例如 Gradle，并非必须用 Maven。
- [[Node.js与pnpm|pnpm]] 与 Maven 都涉及依赖管理，但配置格式、版本解析、构建模型等不同。Maven 的 `pom.xml` 更接近项目描述，而不是简单等同于 `pnpm-lock.yaml`。
- 线上程序通常运行已构建的应用产物，不需要每个请求都先调用 Maven。

## 常见误区、安全与学习建议

`pom.xml` 和项目来源需要审查：构建插件、测试和依赖都可能执行代码；构建成功不证明依赖安全。固定版本、受控仓库和依赖风险检查仍重要，参见 [[软件供应链：代码签名、SBOM与发布门禁]]。

不要为了消除报错就盲目更新全部依赖或复制陌生仓库配置。先确认 [[Java SE、JDK与JVM：Java基础平台|JDK]] 与项目兼容，再看项目声明、插件和依赖树。

建议先认识 `pom.xml`、`src/main/java` 主代码目录、`src/test/java` 测试目录和 `target` 构建目录，再学习父项目、多模块和更复杂的插件配置。完整技术栈见 [[Spring、Spring Boot、Spring MVC与SSM：Java后端框架关系]]。

## 参考资料

核对日期：2026-09-23。具体命令行为受项目和插件配置影响。

- [What is Maven](https://maven.apache.org/what-is-maven.html)：工具职责。
- [Introduction to the POM](https://maven.apache.org/guides/introduction/introduction-to-the-pom.html)：项目描述。
- [Build Lifecycle](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html)：构建阶段和插件任务。
- [Dependency Mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)：依赖解析和版本管理。
