---
title: Python接口自动化：Requests、pytest、unittest与Allure
aliases: [Requests, pytest, unittest, Allure, Fixture, conftest, parametrize, 数据驱动测试]
tags: [软件测试, Python, 自动化]
created: 2026-11-15
updated: 2026-11-15
verified: 2026-11-15
---

# Python接口自动化：Requests、pytest、unittest与Allure

## 一句话解释与类比

**Requests 负责发 HTTP 请求，pytest/unittest 负责组织和判断测试，Allure 负责展示测试证据与报告。**像考场：Requests 是送试卷的人，测试用例是题目与评分标准，测试框架是监考和判卷流程，报告工具是成绩单。

Python（常读“派森”）是语言，库和框架是别人写好供你调用的代码。安装库并不等于写好了测试；基础环境见 [[Anaconda与Python环境管理]]。

## 一、Requests：从请求到可检查的结果

下面假定你已在自己的本地练习服务实现 `/api/courses/42`，本笔记没有启动该服务：

```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/api/courses/42",
    params={"language": "zh-CN"},
    timeout=(3, 10),
)
response.raise_for_status()
course = response.json()
assert course["id"] == 42
```

`params` 编码 URL 查询参数；`timeout` 分别指定连接与读取超时。读取超时不是整个业务总耗时上限。`raise_for_status()` 检查 HTTP 错误，`json()` 解析响应，`assert` 检查业务事实。

`post(..., json=payload)` 发送 JSON；`data=` 常用于表单或原始内容；`files=` 用于文件上传，三者不能随意互换。`Session` 可以复用连接和保存 Cookie；认证令牌可通过 `headers` 传入。

网络失败、HTTP 错误、JSON 解析失败和业务断言失败应分别记录。不要 `except: pass` 吞掉错误，也不要把 `verify=False` 当成一般 HTTPS 使用方法。

## 二、pytest：发现用例、执行、汇总

pytest 常读“派泰斯特”。它可以发现 `test_` 命名的函数/文件，执行断言，并汇总结果。下面是只在内存中操作的完整教学用例，保存为 `test_quantity.py`：

```python
import pytest

def valid_quantity(value):
    return type(value) is int and 1 <= value <= 10

@pytest.mark.parametrize("value, expected", [
    (0, False), (1, True), (10, True), (11, False),
    (2.5, False), (None, False), (True, False),
])
def test_quantity(value, expected):
    assert valid_quantity(value) is expected
```

执行 `python -m pytest test_quantity.py -q` 会把 7 组输入分别作为用例执行。这里的函数是教学用被测对象；真实工程应导入业务代码，不能在测试中复制一份实现后声称真实应用通过。

特别检查 `True` 是因为 Python 中布尔值与整数有继承关系；明确规则才能知道布尔值是否允许当数量。

## 三、Fixture 与清理

Fixture（近似读“菲克斯彻”）负责准备测试需要的资源，并可以安排清理。例：每条测试获取一份独立列表：

```python
import pytest

@pytest.fixture
def cart():
    items = []
    yield items
    items.clear()

def test_add_item(cart):
    cart.append({"course_id": 42})
    assert len(cart) == 1
```

测试函数的参数名请求对应 Fixture；`yield` 前准备，后面清理。真实资源可能是临时目录、专属账号、数据库事务或客户端。清理必须只针对这次创建的对象，不能清空共享测试库。

Fixture 作用域可为 function、class、module、package、session。范围越大不一定越好：一个可修改的登录/购物车对象被全套用例共享，会产生顺序依赖和并行冲突。

`conftest.py` 可在目录层级共享 Fixture 和本地插件逻辑，pytest 自动发现；它不是一个无边界的全局变量仓库。准备阶段失败通常属于测试错误/环境问题，要和业务断言失败区别分析。

## 四、数据驱动不是把全部逻辑塞进表格

数据驱动是同一测试逻辑运行多组数据。简单数据可直接写参数化列表；更大集合可放 JSON、YAML、CSV 或 Excel，但要验证字段、类型和唯一用例 ID。

YAML（YAML Ain't Markup Language，一种可读的数据序列化格式，常读“亚摩”）不是 Python 代码。读取不可信 YAML 应使用安全加载接口，不能把单元格字符串交给 `eval()` 执行。

如果每一行都写不同 URL、循环、条件、SQL 和脚本，表格可能变成难维护的新编程语言。公共操作放代码，业务参数放数据，复杂场景仍用清晰函数表达。

## 五、unittest 仍是什么位置

unittest 是 Python 标准库测试框架，通常用 `TestCase` 类组织测试：

```python
import unittest

class PriceTest(unittest.TestCase):
    def test_total_in_cents(self):
        self.assertEqual(1990 * 2, 3980)

if __name__ == "__main__":
    unittest.main()
```

`setUp`/`tearDown` 可准备和清理。pytest 的函数、参数化和 Fixture 更便于许多场景，但不能据此宣称 unittest 已被淘汰；既有代码和依赖决定迁移成本，pytest 也能运行许多 unittest 测试。

## 六、怎样组织接口自动化工程

```text
tests/           业务用例与断言
clients/         HTTP客户端，统一地址、认证和超时
data/            非敏感测试数据
conftest.py      资源准备和回收
配置文件          标记、运行范围、日志策略
报告目录          执行时生成，不存真实凭据
```

不要在客户端层把所有响应都转换成“成功”；否则上层看不到错误。请求封装用于减少重复，业务断言仍应清楚表达“为什么这样才算对”。

同一测试账号被并行用例改密码，会导致随机失败；可使用每用例独立账号、独立数据命名空间，或对无法隔离的资源显式串行执行。

## 七、Allure 报告：展示什么才有用

Allure（近似读“阿卢尔”）通过测试适配器收集结果、步骤、参数、附件和耗时，再生成可浏览报告。它不是测试框架，也不替你证明预期正确。

pytest 配合适配器时可以生成 Allure 结果目录；报告渲染需对应的 Allure 工具，Allure 2/3 的安装和生成方式要按版本文档选择，不能混用教程命令。

最有价值的附件包括脱敏请求/响应、失败截图、浏览器轨迹、日志和版本信息。重试后通过也应保留首轮失败；把失败测试删掉会让报告好看，却失去质量证据。

常用通用运行方式：`python -m pytest -q --junitxml=report.xml` 输出 JUnit XML 结果，便于持续集成系统收集。命令名不证明全量，仍要检查过滤、标记和跳过数量。

## 八、哪些适合自动化

稳定且重复执行、预期明确、数据可控制的回归场景较合适。一次性需求、极快变化的页面或主观体验判断，可能先人工探索更有效。

投入产出要算“开发+维护+误报排查+运行资源”，而不仅是脚本运行时间。可记录人工回归耗时变化、真正拦截的缺陷、不稳定用例率和维护成本。

学习顺序：纯函数断言 → 参数化 → Fixture → 只读接口 → 带隔离数据的完整业务 → 报告与流水线。关联 [[接口测试与抓包：Postman、Apifox、Mock和HTTPS代理]]、[[持续集成测试：Jenkins、GitLab CI与版本回滚]]。

## 参考资料

核对日期：2026-11-15。示例为教学代码，没有安装依赖或调用生产服务。

- [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)。
- [pytest Fixture](https://docs.pytest.org/en/stable/how-to/fixtures.html)、[参数化](https://docs.pytest.org/en/stable/how-to/parametrize.html)。
- [Python unittest](https://docs.python.org/3/library/unittest.html)、[Allure pytest 集成](https://allurereport.org/docs/pytest/)。
