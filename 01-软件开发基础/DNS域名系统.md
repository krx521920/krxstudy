---
title: DNS 域名系统
aliases:
  - DNS
  - 域名系统
  - 域名解析
  - DNS解析
tags:
  - 软件开发基础
  - 计算机网络
  - DNS
  - 域名
created: 2026-08-21
updated: 2026-08-21
verified: 2026-08-21
---

# DNS 域名系统

> [!summary] 一句话结论
> **DNS（Domain Name System，域名系统，逐字母读作“D-N-S”）是互联网的分布式名称查询系统。它最常见的用途是把人容易记忆的域名转换成计算机联网需要的 IP 地址，但它还负责邮件服务器、权威服务器、服务发现等信息。**

如果没有 DNS，访问网站时可能需要记住一串 IP 地址。DNS 让我们可以使用：

~~~text
www.example.com
~~~

而不是直接记忆：

~~~text
93.184.216.34
~~~

上面的 IP 仅用于帮助理解；网站地址可能随时间、地区和网络环境变化。

---

## 生活类比：DNS 像什么

可以先把 DNS 想成“互联网通讯录”：

~~~text
姓名：某家餐厅
电话号码：12345678

域名：www.example.com
IP 地址：服务器的网络地址
~~~

但这个类比并不完整。DNS 更像一个由许多机构分工维护、可以缓存结果的全球分级查询系统：

- 根服务器告诉你某个顶级域应该去哪里问；
- 顶级域服务器告诉你某个域名由谁管理；
- 权威 DNS 服务器给出最终记录；
- 递归解析器替普通用户完成多轮询问；
- 各级缓存减少重复查询。

因此不存在一台保存“全世界所有域名”的万能 DNS 服务器。

---

## DNS 解决了什么问题

### 1. 域名比 IP 地址容易记

人更容易记住 `github.com`，而不是一串 IPv4 或 IPv6 地址。

### 2. 域名与服务器可以分离

网站更换服务器、机房或 CDN 节点时，可以修改 DNS 记录，而不必让每个用户记住新的 IP。

### 3. 同一域名可以返回多个地址

这样可以用于：

- 负载均衡；
- 容灾；
- IPv4 与 IPv6 并存；
- 根据地区返回较近的 CDN 节点；
- 灰度发布和流量调度。

### 4. DNS 不只保存网站地址

它还可以描述：

- 哪台服务器接收某个域名的邮件；
- 哪些服务器对某个 DNS 区域具有权威；
- 域名所有权验证信息；
- 某种服务的位置和端口；
- IP 地址反向对应的名称。

---

## 域名、URL、IP 和端口不是一回事

以这个地址为例：

~~~text
https://www.example.com:443/docs?id=1
~~~

| 部分 | 示例 | 作用 |
|---|---|---|
| 协议 | `https` | 规定应用怎样通信 |
| 域名 | `www.example.com` | 给人和程序使用的名称 |
| 端口 | `443` | 标识目标设备上的网络服务入口 |
| 路径 | `/docs` | 指定网站内部资源 |
| 查询参数 | `id=1` | 向服务器传递额外参数 |

DNS 通常只负责查询域名相关记录。它不会替浏览器下载网页，也不会处理 `/docs?id=1`。

常见顺序是：

~~~text
域名
→ DNS 查询得到 IP
→ 应用连接 IP 和端口
→ 建立 TCP/QUIC 与 TLS 等连接
→ 发送 HTTP 请求
→ 接收网页数据
~~~

这与 [[TCP、HTTP、HTTPS与WebSocket]] 中的网络协议共同完成一次网页访问。

---

## 输入网址后，DNS 查询怎样发生

为了容易理解，先看简化流程：

~~~mermaid
flowchart LR
    App["浏览器"] --> Stub["操作系统中的存根解析器"]
    Stub --> Recursive["递归 DNS 解析器"]
    Recursive --> Root["根服务器"]
    Root --> TLD["顶级域服务器，例如 .com"]
    TLD --> Auth["example.com 的权威 DNS"]
    Auth --> Recursive
    Recursive --> Stub
    Stub --> App
    App --> Site["根据 IP 连接网站"]
~~~

实际过程可能因为缓存、浏览器加密 DNS、VPN、代理或企业网络而有所不同。

### 第 1 步：浏览器需要解析域名

用户输入：

~~~text
https://www.example.com
~~~

浏览器需要知道应该连接哪个 IP 地址。

### 第 2 步：先检查已有结果

系统可能依次检查：

- 浏览器自己的 DNS 缓存；
- 操作系统 DNS 缓存；
- `hosts` 文件中的静态映射；
- 本地网络组件或代理软件的缓存；
- 已配置的 DNS 解析器。

具体顺序由操作系统、浏览器和应用实现决定，不能把上面的列表当成所有设备都完全一致的固定顺序。

如果已经有尚未过期的结果，就可能直接使用，不再向外查询。

### 第 3 步：询问递归解析器

普通电脑通常不会自己完整询问根、顶级域和权威服务器，而是把问题交给递归解析器。

递归解析器可能来自：

- 家用路由器转发；
- 运营商；
- 公司或学校；
- 用户手动填写的公共 DNS 服务；
- VPN 或 TUN 客户端；
- 浏览器设置的 DoH 服务。

问题可以理解为：

~~~text
请告诉我 www.example.com 的 A 或 AAAA 记录。
~~~

### 第 4 步：递归解析器查找答案

如果递归解析器没有缓存，它通常沿 DNS 层级询问：

1. 根服务器：`.com` 应该去哪里问？
2. `.com` 顶级域服务器：`example.com` 应该去哪里问？
3. `example.com` 权威服务器：`www.example.com` 的目标记录是什么？
4. 把最终结果返回给用户，并按 TTL 缓存。

这是一种概念化流程。真实查询还可能包含 CNAME 跳转、DNSSEC 验证、多服务器重试、IPv4/IPv6 查询和缓存命中。

### 第 5 步：应用使用查询结果联网

DNS 返回地址以后，浏览器才会继续：

1. 选择合适的 IPv4 或 IPv6 地址；
2. 连接目标端口；
3. 建立 TLS 安全连接；
4. 发送 HTTPS 请求；
5. 获取网页内容。

所以 DNS 正常不代表网站一定能打开。DNS 之后还可能发生路由、端口、防火墙、TLS、代理或服务器故障。

---

## 查询过程中有哪些参与者

| 参与者 | 作用 | 生活类比 |
|---|---|---|
| 应用 | 提出域名查询需求 | 想找某家店的顾客 |
| 存根解析器 | 操作系统中替应用发出简单查询的组件 | 顾客身边的助理 |
| 递归解析器 | 替用户追踪完整答案并缓存 | 帮你逐级打电话查询的客服 |
| 根服务器 | 指向相应顶级域服务器 | 总目录 |
| 顶级域服务器 | 指向具体域名的权威服务器 | `.com`、`.cn` 分目录 |
| 权威 DNS 服务器 | 保存某个 DNS 区域的正式记录 | 最终档案管理处 |

### 存根解析器

**Stub Resolver（存根解析器）**通常位于用户设备中。它能力较简单，主要把应用的请求交给配置好的递归 DNS 解析器。

### 递归解析器

**Recursive Resolver（递归解析器）**负责尽力给客户端返回最终答案或错误，而不是只告诉客户端“你再去问另一台服务器”。

### 权威 DNS 服务器

**Authoritative Name Server（权威域名服务器）**保存并回答它所负责区域的正式 DNS 数据。权威服务器不等于网站服务器，它们承担的是不同工作。

### 根服务器

DNS 根区是域名层级的最高处。人们常说“13 个根服务器”，更准确的说法是 13 个命名权威标识；借助 Anycast 等部署方式，实际服务实例分布在全球许多地点，并不只有 13 台物理机器。

---

## 递归查询和迭代查询

### 递归查询

客户端的意思是：

> 请你替我查到底，最后给我答案或错误。

普通电脑向递归解析器发出的请求通常接近这种关系。

### 迭代查询

服务器如果不知道最终答案，可能返回一个更接近答案的服务器地址：

> 我不知道最终 IP，但你可以去问 `.com` 的服务器。

递归解析器在权威层级之间查找答案时，通常会处理这种转介。

一句话区分：

~~~text
递归：你替我一直问到有结果
迭代：我告诉你下一步该问谁
~~~

---

## DNS 为什么是树状结构

完整域名可以从右向左理解：

~~~text
www.example.com.
~~~

| 部分 | 含义 |
|---|---|
| 最后的 `.` | DNS 根，平时通常省略 |
| `com` | 顶级域名 TLD |
| `example` | `com` 下面注册的域 |
| `www` | 该域下面的主机名或子域标签 |

**TLD（Top-Level Domain，顶级域名）**包括 `.com`、`.org`、`.cn` 等。

**FQDN（Fully Qualified Domain Name，完全限定域名）**表示从具体名称一直写到根的完整名称。日常书写时经常省略最后的点。

### Zone 是什么

**Zone（区域）**是由某组权威 DNS 服务器负责管理的一部分 DNS 名称空间。

“域名”和“区域”相关，但不完全相同：

- 域名强调树状名称；
- 区域强调由谁管理哪一部分数据；
- 一个组织可以把子域委派给另一组权威服务器管理。

---

## 常见 DNS 记录

DNS 返回的不是单一类型的“地址”，而是 **Resource Record（资源记录，简称 RR）**。

| 记录 | 英文含义 | 主要用途 | 简化示例 |
|---|---|---|---|
| A | Address | 域名对应 IPv4 地址 | `example.com → 192.0.2.10` |
| AAAA | IPv6 Address | 域名对应 IPv6 地址 | `example.com → 2001:db8::10` |
| CNAME | Canonical Name | 把一个名称设为另一个名称的别名 | `www → site.example.net` |
| NS | Name Server | 指定区域的权威 DNS 服务器 | `example.com → ns1...` |
| MX | Mail Exchange | 指定接收邮件的服务器 | `example.com → mail...` |
| TXT | Text | 保存验证和策略等文本 | 域名验证、SPF 等 |
| SOA | Start of Authority | 描述区域的权威起点与管理参数 | 序列号、刷新时间等 |
| PTR | Pointer | 常用于从 IP 反向查询名称 | `IP → hostname` |
| SRV | Service | 描述某服务的主机和端口 | 即时通信、目录服务等 |
| CAA | Certification Authority Authorization | 声明允许哪些证书机构签发证书 | `issue "ca.example"` |
| SVCB/HTTPS | Service Binding | 提供现代服务连接参数和替代端点信息 | HTTPS 服务参数 |

示例中的 `192.0.2.0/24` 和 `2001:db8::/32` 属于文档示例地址范围，不应把它们当成真实网站地址。

### A 和 AAAA

- A 记录返回 IPv4 地址；
- AAAA 记录返回 IPv6 地址；
- 同一个域名可以同时拥有两类记录；
- 应用可能并行查询并根据连接情况选择。

### CNAME

CNAME 表示“这个名称是另一个名称的别名”。解析器需要继续查询目标名称的地址，所以一次看似简单的查询可能产生多轮 DNS 请求。

### MX

MX 告诉邮件发送系统应该把发往 `user@example.com` 的邮件交给哪些邮件服务器。它不是网页服务器记录。

### TXT

TXT 可以保存文本，经常用于域名所有权验证、邮件策略和服务配置。TXT 不是可以随意存放大量私密信息的安全数据库，其内容通常可以被公开查询。

---

## TTL 和 DNS 缓存

**TTL（Time To Live，生存时间）**表示 DNS 记录可以被缓存多长时间，通常以秒为单位。

例如：

~~~text
TTL = 300
~~~

表示解析器通常可以把这条记录缓存约 300 秒，然后需要重新确认。

### 为什么要缓存

缓存可以：

- 加快访问速度；
- 减少递归解析器压力；
- 减少根、顶级域和权威服务器查询量；
- 在一定程度上提升可用性。

### 缓存带来的现象

修改 DNS 记录以后，有人马上看到新结果，有人仍看到旧结果，常见原因就是不同缓存的剩余 TTL 不同。

所谓“DNS 全球生效”并不通常是一条更新主动推送到全世界，而更接近：

> 权威记录已经修改，但各处旧缓存要在过期后重新查询。

浏览器、操作系统、路由器、递归解析器和应用都可能有自己的缓存策略，因此实际更新时间不一定只由一个 TTL 数字决定。

### 错误结果也可能缓存

`NXDOMAIN` 表示查询的域名不存在。DNS 支持对这类否定回答进行一定时间的缓存，这称为 **Negative Caching（否定缓存）**。

所以刚创建一个此前不存在的名称时，某些解析器仍可能短暂返回“不存在”。

---

## DNS 使用什么协议和端口

经典 DNS 通常使用：

| 方式 | 常见端口 | 说明 |
|---|---:|---|
| DNS over UDP | UDP 53 | 开销较小，经典查询常见 |
| DNS over TCP | TCP 53 | 响应较大、重试、区域传送等场景会用到；TCP 是 DNS 的有效且必须支持的传输方式 |
| DoT | TCP 853 | 在 TLS 加密连接中传输 DNS |
| DoH | TCP/QUIC 443 | 把 DNS 查询映射到 HTTPS 交换 |

不要记成“DNS 永远只使用 UDP 53”。现代 DNS 可能使用 TCP、TLS、HTTPS，具体取决于系统和应用配置。

### 为什么 UDP 和 TCP 都有

UDP 不需要先建立连接，开销较小；TCP 能可靠传输更大数据并处理一些 UDP 不适合的情况。现代标准明确要求 DNS 实现正确支持 TCP，而不是把它当成可有可无的例外。

---

## 普通 DNS、DoH、DoT 和 DNSSEC

这些概念经常被混在一起。

### 普通 DNS

传统 UDP/TCP DNS 查询通常没有为查询内容提供传输层加密。同一路径上的网络设备可能观察或干预查询。

### DoH

**DoH（DNS over HTTPS，通过 HTTPS 传输 DNS）**把 DNS 查询与响应放进 HTTPS 交换，常用 443 端口。

它主要保护“设备到所选 DoH 解析器”这一段的机密性和完整性，但 DoH 服务提供者仍然需要处理你的查询。

### DoT

**DoT（DNS over TLS，通过 TLS 传输 DNS）**使用 TLS 保护设备与 DNS 解析器之间的查询，常用 853 端口。

### DNSSEC

**DNSSEC（Domain Name System Security Extensions，域名系统安全扩展）**通过数字签名帮助验证 DNS 数据来源和完整性。

DNSSEC 主要解决：

- 回答是不是来自可信的 DNS 数据链；
- 数据在传递过程中是否被篡改；
- 某个名称或记录不存在的回答能否被验证。

DNSSEC 不等于加密 DNS：

- DNSSEC 主要验证数据真实性和完整性；
- DoH/DoT 主要加密设备到解析器之间的传输；
- DNSSEC 本身不负责隐藏查询名称；
- DoH/DoT 本身也不保证域名所有者配置的数据一定正确。

| 技术 | 主要解决的问题 | 是否隐藏查询内容 |
|---|---|---|
| 普通 DNS | 名称查询 | 通常不隐藏 |
| DoH/DoT | 设备到解析器的加密传输 | 对链路观察者隐藏，但解析器仍能看到 |
| DNSSEC | 验证数据来源与完整性 | 不以保密为目标 |

---

## Windows 从哪里得到 DNS 服务器

Windows 使用的 DNS 服务器地址可能来自：

- 路由器通过 DHCP 自动下发；
- 用户在网卡中手动设置；
- 公司或学校网络配置；
- VPN 或 TUN 虚拟网卡；
- 安全软件；
- 浏览器自己的 DoH 配置。

**DHCP（Dynamic Host Configuration Protocol，动态主机配置协议）**可以自动给设备分配 IP、网关和 DNS 服务器等网络参数。

路由器显示为 DNS 服务器时，它可能只是把查询转发给运营商或上游解析器，并不一定独立完成全部递归查询。

### hosts 文件

Windows 的 `hosts` 文件通常位于：

~~~text
C:\Windows\System32\drivers\etc\hosts
~~~

它可以手工写入名称与 IP 的静态映射，例如开发测试时把一个名称临时指向本机。

注意：

- 修改通常需要管理员权限；
- 错误内容可能导致网站打不开或连错服务器；
- 它不是公共 DNS 记录，只对读取这份文件的本机解析流程生效；
- 某些使用独立 DoH 或自带解析机制的应用行为可能不同。

---

## DNS 与系统代理、Clash、TUN 和 VPN 的关系

DNS 决定“域名怎样得到地址”，代理或 VPN 决定“网络流量接下来怎样走”。两者不同，但会互相影响。

### 情况 1：应用先在本地解析

~~~text
应用
→ 本地 DNS 得到 IP
→ 把 IP 和端口交给代理
→ 代理连接目标
~~~

此时 DNS 查询可能没有经过远程代理。

### 情况 2：应用把域名交给代理

~~~text
应用
→ 把 example.com:443 交给本地代理
→ 代理或远程节点解析域名
→ 连接目标
~~~

HTTP 代理、SOCKS 配置和具体应用可能采取不同策略，不能只看“系统代理已打开”就判断 DNS 一定在哪里解析。

### 情况 3：TUN/VPN 接管 DNS

TUN 或 VPN 客户端可能：

- 给虚拟网卡设置专用 DNS；
- 截获传统 DNS 查询；
- 按域名进行分流；
- 把 DNS 查询送入隧道；
- 在客户端内部维护域名和连接的映射。

实现取决于具体软件与配置。

### 情况 4：浏览器使用自己的 DoH

浏览器可能绕过 Windows 默认解析器，直接连接自己配置的 DoH 服务。因此会出现：

~~~text
nslookup 得到一个结果
浏览器却得到另一个结果
~~~

排查时要同时检查浏览器的安全 DNS 设置。

这些关系已经在 [[系统代理、VPN与端口]] 中进一步讨论。

---

## DNS 泄漏是什么

**DNS Leak（DNS 泄漏）**通常指用户希望流量和 DNS 查询都通过代理/VPN 保护路径，但 DNS 查询却从本地网络、运营商解析器或另一个意外路径发出。

例如：

~~~text
网页流量 → VPN 隧道
DNS 查询 → 本地运营商 DNS
~~~

可能产生的影响：

- 本地网络仍能观察到查询的域名；
- 本地和远程解析结果不一致；
- 域名分流规则判断错误；
- 返回对当前出口不可达或不合适的地址；
- 用户误以为所有相关流量都经过同一路径。

但看到某个 DNS 服务不等于一定存在安全漏洞。首先要明确自己的预期路径，再比较实际路径。

---

## DNS 与隐私、安全有什么关系

### DNS 能看到什么

递归 DNS 服务通常至少需要知道：

- 查询的域名或记录；
- 查询时间；
- 请求来源的一些网络信息；
- 返回结果和错误。

服务的日志、保留时间和隐私政策取决于提供者。

### 加密 DNS 不是完全匿名

DoH 或 DoT 保护设备到解析器的查询链路，但：

- DNS 解析器仍处理查询；
- 目标网站仍能看到连接；
- 网络仍可能看到目标 IP、连接时间和流量特征；
- 账号、Cookie 和浏览器指纹仍可能识别用户；
- 恶意 DNS 结果仍可能把用户导向错误地址，HTTPS 证书验证是另一层保护。

### 常见攻击或故障概念

- **DNS Spoofing（DNS 欺骗）**：伪造 DNS 回答；
- **Cache Poisoning（缓存投毒）**：让解析器缓存错误数据；
- **DNS Hijacking（DNS 劫持）**：通过修改配置、网络拦截等方式把查询或结果导向非预期位置；
- **Domain Hijacking（域名劫持）**：攻击域名注册或管理账户，和单纯 DNS 查询劫持不完全相同。

DNSSEC、加密 DNS、HTTPS 证书、账号保护各自解决不同层面的问题，不能互相完全替代。

---

## 常见 DNS 错误

| 现象或错误 | 大致含义 | 常见方向 |
|---|---|---|
| NXDOMAIN | 域名不存在 | 拼写、记录未创建、否定缓存 |
| SERVFAIL | 解析器无法成功完成查询 | 权威服务器、DNSSEC、上游故障 |
| Timeout | 查询超时 | 网络、53/853/443 端口、防火墙、解析器不可达 |
| 有 IP 但网站打不开 | DNS 已完成，后续连接失败 | 路由、端口、TLS、代理、服务器 |
| 只有一个设备不行 | 本机缓存或配置问题 | hosts、浏览器 DoH、VPN、网卡 DNS |
| 不同网络结果不同 | 缓存、CDN 或分流不同 | TTL、地区解析、运营商、代理出口 |
| IPv4 能开，IPv6 不能 | AAAA 或 IPv6 路径问题 | IPv6 路由、DNS、代理支持 |

### “能 ping 域名”不能证明网站完全正常

`ping` 可以帮助观察域名是否解析出地址以及 ICMP 是否有响应，但：

- 网站可能禁止 ICMP；
- ping 通不代表 TCP 443 可用；
- ping 不验证 HTTPS 证书和 HTTP 服务；
- CDN 返回的地址可能因环境而异。

---

## Windows 上怎样查看和排查 DNS

以下命令可在 PowerShell 或 CMD 中使用。先观察，再修改。

### 1. 查看网卡和 DNS 配置

~~~powershell
ipconfig /all
~~~

PowerShell 也可以查看各网络接口的 DNS 服务器：

~~~powershell
Get-DnsClientServerAddress
~~~

### 2. 查询域名

~~~powershell
Resolve-DnsName example.com
~~~

查询指定记录类型：

~~~powershell
Resolve-DnsName example.com -Type AAAA
Resolve-DnsName example.com -Type MX
~~~

兼容性更广的工具：

~~~text
nslookup example.com
~~~

向指定 DNS 解析器查询：

~~~text
nslookup example.com <DNS服务器IP>
~~~

这有助于比较“默认解析器”和“另一台解析器”的结果，但结果不同不一定代表某一方遭到攻击，也可能是缓存、CDN 或地区调度。

### 3. 查看 Windows DNS 缓存

~~~text
ipconfig /displaydns
~~~

### 4. 清理 Windows DNS 客户端缓存

~~~text
ipconfig /flushdns
~~~

PowerShell 也可以使用：

~~~powershell
Clear-DnsClientCache
~~~

清理缓存只会让本机重新查询，它不会：

- 修改权威 DNS 记录；
- 强迫全球解析器刷新；
- 修复错误的域名配置；
- 清理所有浏览器、代理、路由器或上游解析器缓存。

### 5. 检查 DNS 之后的目标端口

~~~powershell
Test-NetConnection example.com -Port 443
~~~

如果名称能解析但端口测试失败，应继续检查 [[TCP、HTTP、HTTPS与WebSocket|TCP/HTTPS]]、防火墙、路由和 [[系统代理、VPN与端口|代理设置]]，而不是反复更换 DNS。

---

## 推荐排查顺序

### 第 1 步：明确故障范围

- 只有一个网站还是所有网站？
- 只有浏览器还是所有应用？
- 只有当前电脑还是同一网络所有设备？
- 直连、系统代理和 TUN/VPN 的结果是否不同？

### 第 2 步：确认域名没有写错

尤其注意：

- 字母拼写；
- 多余空格；
- 子域名；
- 把 URL 路径误当成域名；
- 相似字符和钓鱼域名。

### 第 3 步：查询默认 DNS

使用 `Resolve-DnsName` 或 `nslookup`，观察：

- 是否返回 A/AAAA；
- 是否返回 NXDOMAIN 或 SERVFAIL；
- 使用了哪台 DNS 服务器；
- 响应是否超时。

### 第 4 步：比较不同解析路径

检查：

- Windows DNS；
- 浏览器 DoH；
- VPN/TUN 提供的 DNS；
- `hosts` 文件；
- 指定解析器查询结果。

### 第 5 步：必要时清理本机缓存

只在怀疑本机缓存过期或错误时使用 `ipconfig /flushdns`。不要把它当成修复所有网络问题的万能命令。

### 第 6 步：确认 DNS 之后的连接

DNS 已返回地址后，继续检查：

- 目标端口；
- TCP/QUIC；
- TLS 证书；
- HTTP 状态；
- 防火墙；
- 代理规则；
- IPv4/IPv6 路径。

---

## 常见误区

### 误区 1：DNS 就是把域名转换成 IP

这是最常见用途，但 DNS 还保存 MX、NS、TXT、SOA、PTR 等多类记录。

### 误区 2：DNS 是一台全球服务器

不是。DNS 是分布式、分层、可缓存的系统。

### 误区 3：根服务器知道所有网站 IP

根区主要负责顶级域委派。根服务器通常告诉解析器下一步应该询问哪个顶级域服务器，而不是保存每个网站的最终 A 记录。

### 误区 4：世界上只有 13 台根服务器

更准确地说是 13 个命名权威标识，背后有分布在许多国家和地区的大量服务实例。

### 误区 5：修改 DNS 会提高宽带速度

DNS 较快可能缩短首次解析等待，但不会直接提高文件下载带宽。网页慢还可能由服务器、线路、TLS、图片和程序性能造成。

### 误区 6：换 DNS 等于开代理或 VPN

不是。DNS 主要回答名称信息；代理/VPN 改变流量路径。换 DNS 通常不会自动改变网站看到的公网出口 IP。

### 误区 7：DoH 就是匿名上网

不是。DoH 加密设备到解析器之间的 DNS 查询，但解析器和目标网站仍参与通信，其他网络元数据也可能可见。

### 误区 8：DNSSEC 会加密域名查询

不是。DNSSEC 主要验证数据来源与完整性，不以隐藏查询名称为目标。

### 误区 9：清空 DNS 缓存一定能修好网络

不是。它只清理 Windows DNS 客户端缓存，不能修复服务器宕机、端口阻断、错误权威记录或代理故障。

### 误区 10：直接用 IP 打开网站可以完全绕过 DNS

不一定。许多 HTTPS 网站共享 IP，需要域名选择站点并验证证书；直接访问 IP 可能得到错误站点或证书错误。

---

## 三个具体例子

### 例子 1：访问网页

~~~text
浏览器查询 www.example.com
→ DNS 返回 A/AAAA
→ 浏览器连接相应 IP 的 443 端口
→ TLS 验证网站证书
→ 发送 HTTPS 请求
~~~

### 例子 2：发送邮件

~~~text
发送方查询 example.com 的 MX 记录
→ 得到邮件服务器名称
→ 再查询邮件服务器的地址
→ 连接邮件服务
~~~

### 例子 3：代理开启后浏览器与 nslookup 结果不同

可能原因：

- 浏览器启用了自己的 DoH；
- Clash/TUN 接管了浏览器流量；
- `nslookup` 仍向 Windows 配置的 DNS 查询；
- 两边缓存不同；
- 两个解析器根据出口地区返回不同 CDN 节点。

这时应该分别确认两条查询路径，而不是只说“DNS 坏了”。

---

## 最小记忆模型

~~~mermaid
flowchart TD
    Name["域名：人容易记的名称"] --> DNS["DNS：查询名称相关记录"]
    DNS --> IP["IP：定位网络中的目标"]
    IP --> Port["端口：定位目标上的服务"]
    Port --> Protocol["TCP/QUIC + TLS + HTTP：真正传输数据"]
~~~

记住这四句话：

1. DNS 主要负责“问路”，不是负责“运送网页”；
2. 递归解析器替用户逐级查找并缓存答案；
3. 权威服务器提供自己负责区域的正式记录；
4. DNS 成功后，网络连接仍可能在后续步骤失败。

---

## 学习建议

建议按这个顺序掌握：

1. 域名、IP 地址和端口的区别；
2. A、AAAA、CNAME、MX、NS 记录；
3. 存根解析器、递归解析器和权威服务器；
4. 根、TLD、区域和委派；
5. TTL 与缓存；
6. UDP/TCP 53、DoH 和 DoT；
7. DNSSEC 与加密 DNS 的区别；
8. 系统代理、TUN/VPN 与 DNS 路径；
9. 使用 Windows 命令进行分层排查。

---

## 关联概念

- [[TCP、HTTP、HTTPS与WebSocket]]：DNS 得到地址以后，应用怎样建立连接并传输网页。
- [[系统代理、VPN与端口]]：代理、TUN、VPN 怎样影响 DNS 查询路径和出口。
- [[CMD、Bash与PowerShell]]：使用命令查看、查询和清理 DNS 缓存。
- [[SDK与API]]：程序也会通过操作系统或网络库调用名称解析接口。

---

## 参考资料

以下资料于 **2026-08-21** 核对：

- [RFC 1034：Domain Names - Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034.html)
- [RFC 1035：Domain Names - Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035.html)
- [RFC 7766：DNS Transport over TCP](https://www.rfc-editor.org/rfc/rfc7766.html)
- [RFC 7858：DNS over TLS](https://www.rfc-editor.org/rfc/rfc7858.html)
- [RFC 8484：DNS Queries over HTTPS](https://www.rfc-editor.org/rfc/rfc8484.html)
- [RFC 4033：DNS Security Introduction and Requirements](https://www.rfc-editor.org/rfc/rfc4033.html)
- [RFC 2308：Negative Caching of DNS Queries](https://www.rfc-editor.org/rfc/rfc2308.html)
- [IANA：Root Zone Management](https://www.iana.org/domains/root)
- [IANA：Root Name Servers](https://www.iana.org/domains/root/servers)
- [Microsoft Learn：ipconfig](https://learn.microsoft.com/windows-server/administration/windows-commands/ipconfig)
- [Microsoft Learn：Troubleshooting DNS clients](https://learn.microsoft.com/windows-server/networking/dns/troubleshoot/troubleshoot-dns-client)
