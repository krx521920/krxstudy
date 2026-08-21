---
title: TLS 与数字证书
aliases:
  - TLS
  - SSL
  - 数字证书
  - TLS握手
  - HTTPS证书
  - mTLS
tags:
  - 软件开发基础
  - 计算机网络
  - TLS
  - HTTPS
  - 数字证书
  - 网络安全
created: 2026-08-21
updated: 2026-08-21
verified: 2026-08-21
---

# TLS 与数字证书

> [!summary] 一句话结论
> **TLS（Transport Layer Security，传输层安全协议，逐字母读作“T-L-S”）是在客户端和服务器之间建立安全通信通道的协议。它通过握手协商密钥、验证身份，然后使用高效的对称加密保护后续数据，主要提供机密性、完整性和身份认证。HTTPS 就是受到 TLS 保护的 HTTP。**

最简单的关系是：

~~~text
HTTP：规定网页请求和响应怎样表达
TLS：给这些数据提供加密、完整性保护和身份认证
HTTPS：HTTP 运行在 TLS 保护的安全连接中
~~~

TLS 不只服务于网页。电子邮件、即时通信、数据库、API、DNS 和许多自定义协议都可以使用 TLS。

---

## 生活类比：TLS 像什么

假设你要给一家银行寄一份机密文件。

你需要解决三个问题：

1. 文件不能被路上的人直接看懂；
2. 文件不能在途中被偷偷修改；
3. 你必须确认收件方真的是银行，而不是冒充者。

TLS 可以类比成：

- 先检查银行出示的、由可信机构签发的身份证明；
- 双方通过安全方法协商出本次通信专用的密码；
- 后续文件装入只有双方能打开的加密箱；
- 每个箱子都带有防篡改校验；
- 一旦发现内容被改动，就拒绝继续通信。

这个类比只能帮助入门。真实 TLS 使用证书、数字签名、密钥交换、密钥派生和认证加密等密码学机制。

---

## TLS 主要提供什么

### 1. Confidentiality：机密性

**Confidentiality（机密性）**表示网络中间人即使截获了数据，也不应该直接读懂正文。

例如 HTTPS 正常工作时，旁路观察者不应直接看到：

- 登录密码；
- Cookie 或 Token；
- HTTP 请求正文；
- 网页返回正文；
- URL 中域名之后的路径和查询参数。

### 2. Integrity：完整性

**Integrity（完整性）**表示通信双方能够检测数据在传输途中是否被修改。

攻击者不能只把：

~~~text
转账 100 元
~~~

偷偷改成：

~~~text
转账 10000 元
~~~

然后仍让接收方把它当成合法的 TLS 数据。

### 3. Authentication：身份认证

**Authentication（身份认证）**表示通信方验证对方身份。

在普通 HTTPS 中，最常见的是：

- 浏览器验证服务器；
- 服务器不通过 TLS 证书验证普通用户；
- 用户身份通常再通过密码、Cookie、Token 等应用层机制验证。

TLS 也支持双方都提供证书，这叫 mTLS，后文会详细解释。

---

## TLS 不负责什么

TLS 很重要，但它不是“网站绝对安全”的保证。

TLS 不直接保证：

- 网站不是诈骗网站；
- 下载的文件没有恶意代码；
- 网站内部数据库不会泄漏；
- 服务器收到数据后一定妥善保存；
- 用户设备没有病毒或恶意扩展；
- 目标 IP、连接时间和流量大小完全不可见；
- [[DNS域名系统|DNS]] 查询一定被加密；
- 登录账号、Cookie 和浏览器指纹不会识别用户。

所以浏览器的小锁更接近表示：

> 你与当前证书所认证的域名之间建立了受到 TLS 保护的连接。

它不是“这家公司值得信任”或“这个网页内容一定真实”的质量认证。

---

## TLS、HTTP、HTTPS、TCP 和 QUIC 的关系

### 常见的 HTTPS over TCP

可以先用这个分层理解：

~~~mermaid
flowchart TD
    HTTP["HTTP：网页请求与响应规则"]
    TLS["TLS：加密、完整性、身份认证"]
    TCP["TCP：可靠有序地传输字节"]
    IP["IP：把数据送到目标设备"]
    HTTP --> TLS --> TCP --> IP
~~~

其中：

- TCP 负责可靠、有序地传输字节；
- TLS 在这个字节流上建立安全通道；
- HTTP 在安全通道中发送请求和响应。

### HTTP/3 与 QUIC

HTTP/3 通常运行在 QUIC 上。QUIC 使用 UDP 作为底层传输，并集成 TLS 1.3 握手。

这时不能简单画成：

~~~text
HTTP/3 → TLS记录层 → TCP
~~~

更准确的高层理解是：

~~~text
HTTP/3
→ QUIC（集成 TLS 1.3 握手与数据包保护）
→ UDP
→ IP
~~~

因此“HTTPS 一定使用 TCP”已经不准确；HTTP/1.1 和 HTTP/2 常见于 TCP + TLS，HTTP/3 则使用 QUIC + TLS 1.3。

完整的网络协议关系见 [[TCP、HTTP、HTTPS与WebSocket]]。

---

## SSL 和 TLS 是什么关系

**SSL（Secure Sockets Layer，安全套接层）**是 TLS 的历史前身。

日常仍会听到：

- SSL 证书；
- SSL 加密；
- SSL 错误；
- SSL/TLS。

很多时候人们实际上指的是现代 TLS。

当前不应再把 SSL 2.0、SSL 3.0、TLS 1.0 或 TLS 1.1 当作安全的新部署选择。旧版本因为设计缺陷和已知攻击已经被弃用。

一句话记忆：

> **SSL 是旧名字和旧协议家族；现代安全连接主要讨论 TLS。所谓“SSL 证书”通常其实是供 TLS 使用的 X.509 数字证书。**

---

## 2026 年怎样理解 TLS 版本

> [!important] 核对日期：2026-08-21
> TLS 1.3 当前由 RFC 9846 规范。RFC 9846 是对原 TLS 1.3 标准 RFC 8446 的兼容性小更新，并取代了 RFC 8446 与 TLS 1.2 的 RFC 5246。RFC 9852 进一步要求：新设计的、使用 TLS 的协议必须把 TLS 1.3 作为默认和必需支持；如部署确有需要，可以把 TLS 1.2 作为额外的非默认选项。

### TLS 1.3

TLS 1.3 是现代 TLS 的核心版本。它：

- 简化并收紧了可选算法；
- 移除多种脆弱或容易误配的旧机制；
- 加密更多握手内容；
- 默认使用提供前向保密性的现代密钥交换；
- 改善握手性能；
- 支持会话恢复和受限制使用的 0-RTT。

### TLS 1.2

TLS 1.2 在许多既有系统中仍然存在，而且正确配置时仍能提供较好的安全性。但截至 2026 年：

- TLS 1.2 已进入功能冻结；
- 新的 TLS 功能和后量子方向集中在 TLS 1.3 或更高版本；
- TLS 1.2 的多种旧密钥交换方式已被弃用；
- 新协议不应再把 TLS 1.2 作为默认版本。

“TLS 1.3 标准取代 TLS 1.2”不等于互联网上所有旧服务器会在同一天停止 TLS 1.2。标准状态、软件支持和现实部署是三个不同层面。

### TLS 1.0 和 TLS 1.1

它们已经被 IETF 弃用，不应为了兼容一台老旧服务器就随意在整个系统中重新启用。

---

## TLS 为什么同时需要多种密码学工具

初学者最容易误以为 TLS 从头到尾只使用“公钥加密”。实际上，现代 TLS 把不同工具组合起来。

### 非对称密码学

**Asymmetric Cryptography（非对称密码学）**使用一对相关密钥：

- Public Key（公钥）：可以公开；
- Private Key（私钥）：必须由持有者秘密保存。

在证书模式的 TLS 1.3 中，服务器通常使用私钥对握手信息进行数字签名，证明自己掌握与证书公钥对应的私钥。

### 数字签名

数字签名可以帮助验证：

- 信息确实由私钥持有者签署；
- 被签署的信息没有被修改。

数字签名不等于“用私钥把所有网页正文加密”。

### 密钥交换

现代 TLS 通常通过临时的 Diffie-Hellman 类密钥交换，让双方各自计算出相同的共享秘密，而不是在网络上直接发送最终的会话密钥。

常见的 ECDHE 中：

- EC 表示 Elliptic Curve，椭圆曲线；
- DHE 表示 Ephemeral Diffie-Hellman，临时 Diffie-Hellman；
- Ephemeral 表示使用临时密钥材料。

### 对称加密

**Symmetric Encryption（对称加密）**让双方使用相关的会话密钥高效保护大量数据。

它比直接对全部正文使用公钥密码学更适合持续传输网页、图片和 API 数据。

### AEAD

**AEAD（Authenticated Encryption with Associated Data，带关联数据的认证加密）**把加密和完整性认证结合起来。

TLS 1.3 使用 AEAD 算法保护记录或数据包，常见选择包括 AES-GCM 和 ChaCha20-Poly1305。

### 哈希与密钥派生

TLS 还使用哈希与 KDF：

- Hash（哈希）帮助形成握手记录摘要；
- KDF（Key Derivation Function，密钥派生函数）从共享秘密推导不同用途的密钥；
- 客户端和服务器使用不同方向、不同阶段的密钥；
- 握手结束后还可以更新流量密钥。

---

## 数字证书是什么

数字证书可以理解成：

> 把“某个服务身份”和“某个公钥”绑定起来，并由证书签发机构数字签名的数据文件。

HTTPS 常使用 X.509 证书。服务器证书通常包含：

- 适用的域名或其他服务身份；
- 服务器的公钥；
- 签发者；
- 有效期；
- 序列号；
- 允许用途；
- 签名算法；
- 证书签发机构的数字签名。

### 证书不包含什么

正常的公开服务器证书不应该包含服务器私钥。

通常：

~~~text
证书和公钥：可以发送给客户端
私钥：只应保存在服务器或安全密钥设备中
~~~

如果私钥泄漏，攻击者可能冒用服务器身份或破坏相应安全保证，因此私钥保护极其重要。

---

## CA 和证书信任链

**CA（Certificate Authority，证书颁发机构）**负责按规则验证申请者并签发证书。

常见证书链可以简化成：

~~~mermaid
flowchart TD
    Root["根 CA 证书<br/>存在于系统或浏览器信任库"]
    Intermediate["中间 CA 证书"]
    Leaf["网站叶子证书<br/>例如 www.example.com"]
    Root -->|签发或认证| Intermediate
    Intermediate -->|签发| Leaf
~~~

### 根证书

根证书是信任锚。操作系统、浏览器或应用预先信任一组根 CA。

根证书通常不需要由网站在每次连接中发送，因为客户端信任库已经保存它。

### 中间证书

根 CA 通常通过一个或多个中间 CA 签发网站证书，以降低根私钥直接参与日常签发的风险。

服务器通常需要发送叶子证书和必要的中间证书。如果漏发中间证书，某些客户端可能无法构造完整信任链。

### 叶子证书

叶子证书直接用于某个网站或服务，又叫 End-Entity Certificate（终端实体证书）。

---

## 浏览器怎样验证服务器证书

浏览器或 TLS 库通常需要检查多项条件。

### 1. 能否建立到可信根的证书链

客户端验证每一级证书签名，最终连接到本地信任的根证书。

### 2. 域名是否匹配

如果用户访问：

~~~text
https://api.example.com
~~~

证书必须包含与该服务身份匹配的标识。

现代规则主要检查证书的 `subjectAltName`（主题备用名称）扩展中的 DNS 名称，而不是依赖旧式 Common Name 文本。

### 3. 当前时间是否在有效期内

证书有开始和结束时间。电脑时间错误也可能导致：

- 证书尚未生效；
- 证书已经过期。

### 4. 证书用途是否合适

客户端会结合 Key Usage、Extended Key Usage 和应用协议规则判断证书是否适用于服务器身份认证。

### 5. 证书状态和策略

实现还可能结合：

- CRL（Certificate Revocation List，证书吊销列表）；
- OCSP（Online Certificate Status Protocol，在线证书状态协议）；
- OCSP Stapling；
- 浏览器或操作系统安全策略；
- 企业管理策略。

不同客户端对网络失败、吊销查询和本地策略的处理可能不同。

---

## TLS 1.3 握手怎样发生

**Handshake（握手）**是正式传输应用数据前，客户端与服务器协商参数、验证身份并生成会话密钥的过程。

下面是基于证书认证的一次简化 TLS 1.3 握手：

~~~mermaid
sequenceDiagram
    participant C as 客户端/浏览器
    participant S as 服务器

    C->>S: ClientHello：版本、算法、key share、SNI、ALPN 等
    S-->>C: ServerHello：选择版本、算法并返回 key share
    Note over C,S: 双方派生握手密钥
    S-->>C: EncryptedExtensions
    S-->>C: Certificate：证书链
    S-->>C: CertificateVerify：用私钥签名握手记录
    S-->>C: Finished：证明握手未被篡改
    C->>C: 验证证书链、域名、签名和 Finished
    C->>S: Finished
    Note over C,S: 双方使用应用流量密钥
    C->>S: 加密的应用数据，例如 HTTP 请求
    S-->>C: 加密的应用数据，例如 HTTP 响应
~~~

真实握手还会受到会话恢复、客户端证书、HelloRetryRequest、PSK、QUIC 和各类扩展影响。

### ClientHello

客户端告诉服务器自己支持什么，通常包括：

- 支持的 TLS 版本；
- 密码套件；
- 临时密钥共享；
- SNI；
- ALPN；
- 签名算法；
- 其他扩展。

### ServerHello

服务器选择双方共同支持的参数并提供自己的临时密钥共享。双方由此派生握手密钥。

### Certificate 和 CertificateVerify

服务器发送证书链，并用对应私钥签名握手记录。客户端不仅要“看到证书”，还要验证证书和签名。

### Finished

双方用握手派生出的秘密验证整个握手记录没有被中途修改。之后才进入正常的加密应用数据阶段。

---

## 密码套件是什么

**Cipher Suite（密码套件）**描述 TLS 使用的部分密码学算法组合。

TLS 1.3 的例子：

~~~text
TLS_AES_128_GCM_SHA256
~~~

可以粗略拆成：

- AES_128_GCM：用于认证加密；
- SHA256：用于哈希和密钥派生相关过程。

与 TLS 1.2 不同，TLS 1.3 的密码套件名称不再把证书签名和密钥交换算法全部塞进同一个长名字，它们通过其他握手参数协商。

普通用户通常不需要手工选择密码套件。错误地为了兼容旧设备开启弱算法，可能降低整个服务的安全性。

---

## SNI 和 ALPN 是什么

### SNI

**SNI（Server Name Indication，服务器名称指示）**让客户端在 TLS 握手时告诉服务器自己想访问哪个域名。

为什么需要它？因为一个 IP 地址上可能托管许多 HTTPS 网站，服务器需要先知道目标域名，才能选择合适的证书和配置。

传统 SNI 位于 ClientHello 中，可能被路径上的观察者看到。

### ECH

**ECH（Encrypted Client Hello，加密客户端问候）**用于加密 ClientHello 中的敏感内容，包括真实的服务器名称信息。

ECH 已在 RFC 9849 中标准化，但是否真正生效取决于：

- 浏览器或客户端支持；
- DNS 配置；
- 服务端和前置网络支持；
- 网络环境与回退行为。

因此不能因为“使用 TLS 1.3”就自动断言 SNI 一定已经隐藏。

### ALPN

**ALPN（Application-Layer Protocol Negotiation，应用层协议协商）**让双方在 TLS 握手中协商上层协议。

例如可能协商：

- `http/1.1`；
- `h2`，表示 HTTP/2；
- `h3`，用于 HTTP/3/QUIC 场景；
- 其他基于 TLS 的应用协议。

---

## TLS 加密后，别人还能看到什么

TLS 通常保护应用数据内容，但不会自动隐藏所有元数据。

网络路径上的设备仍可能看到：

- 客户端和目标的 IP 地址；
- 目标端口；
- 连接建立与结束时间；
- 数据包大小和流量方向；
- DNS 查询，取决于 DNS 配置；
- 未使用 ECH 时的 SNI 等部分握手信息；
- 连接的是某个代理、VPN 或 CDN 节点。

通常被 TLS 保护的 HTTP 内容包括：

- URL 路径；
- 查询参数；
- 请求头；
- Cookie、Authorization 等凭证；
- 请求体和响应体。

不过，域名也可能通过 DNS、目标 IP、SNI 或其他流量特征暴露，不能只看 URL 路径是否加密。

---

## 前向保密是什么

**Forward Secrecy（前向保密）**表示：即使服务器长期私钥在未来泄漏，攻击者也不应仅凭该私钥解密此前录下的正常会话。

现代 TLS 通过每次连接使用临时密钥交换材料来实现这一重要属性。

它可以类比为：

- 服务器证书私钥用于证明身份；
- 每次会话另行协商临时秘密；
- 一次会话的临时秘密不应长期重复使用；
- 长期身份证明泄漏不应自动打开过去的所有加密箱。

这不代表终端设备被入侵后数据仍绝对安全。攻击者如果在通信时直接控制客户端或服务器，仍可能读取端点上的明文。

---

## 会话恢复和 0-RTT

### 会话恢复

客户端再次连接服务器时，可以利用此前获得的会话恢复信息减少完整握手成本。

好处包括：

- 降低延迟；
- 减少部分计算；
- 加快重复访问。

### 0-RTT

TLS 1.3 在特定恢复场景中允许客户端非常早地发送应用数据，称为 **0-RTT Early Data（零往返早期数据）**。

它的主要风险是重放：攻击者可能复制早期数据并让服务器再次处理。

因此 0-RTT 不适合未经额外保护的非幂等操作，例如：

~~~text
付款
创建订单
删除数据
执行一次性操作
~~~

关于重复请求和安全业务设计，见 [[状态机与幂等性|幂等性]]。

一句话记忆：

> 0-RTT 用更少等待换取更复杂的重放风险控制，不是无条件的“免费加速”。

---

## mTLS 是什么

**mTLS（Mutual TLS，双向 TLS）**表示客户端和服务器双方都使用证书验证对方身份。

普通网站通常是：

~~~text
浏览器验证服务器证书
服务器通过账号、密码、Cookie 或 Token 验证用户
~~~

mTLS 则是：

~~~text
客户端验证服务器证书
服务器也验证客户端证书
~~~

常见用途包括：

- 企业内部服务；
- 微服务之间认证；
- 高安全 API；
- 设备身份认证；
- 零信任网络中的工作负载身份。

mTLS 不等于“完全不需要权限系统”。证书证明客户端身份后，服务器仍要判断这个身份能做什么。

---

## TLS 可以保护哪些协议

TLS 与具体应用协议相对独立。

| 用途 | 常见形式 | 常见端口示例 |
|---|---|---:|
| 网页 | HTTPS | 443 |
| 安全 WebSocket | WSS | 443 |
| DNS over TLS | DoT | 853 |
| 安全邮件提交 | SMTP + STARTTLS 或隐式 TLS | 587 / 465 |
| 安全 IMAP | IMAPS | 993 |
| 数据库 | 数据库协议 + TLS | 取决于数据库 |
| 自定义 API | 应用协议 + TLS | 由服务决定 |
| 远程 MCP | MCP over HTTPS / Streamable HTTP + TLS | 通常 443，也可自定义 |

端口只是惯例入口，TLS 本身并不只能运行在 443 端口。

### TLS 与 MCP 的关系

- 本地 `stdio` MCP Server 通过进程的标准输入输出通信，不建立远程 TLS 连接；安全主要依靠进程权限、文件权限和 Host 隔离。
- 远程 [[MCP模型上下文协议|MCP]] 通常通过 HTTPS 传输，TLS 负责验证远程服务身份，并保护 MCP 消息在网络中的机密性和完整性。
- TLS 只保护两个 TLS 端点之间的传输，不能代替 OAuth、账号权限、Tool 参数校验和用户批准。
- 企业也可以使用 mTLS 同时验证 MCP Client 与 Server，但认证成功后仍要继续判断这个身份能调用哪些工具。

---

## TLS 与系统代理、Clash 的关系

### 普通 HTTP CONNECT 隧道

应用通过 HTTP 代理访问 HTTPS 网站时，常先发送 CONNECT 请求：

~~~text
浏览器
→ 请求本地代理建立 example.com:443 隧道
→ 代理连接目标服务器
→ 浏览器和目标网站通过隧道进行 TLS 握手
~~~

在正常端到端 TLS 中：

- 代理负责转发加密字节；
- 浏览器验证目标网站证书；
- 代理通常不能直接阅读 HTTPS 正文；
- 代理仍可能知道目标主机、端口、连接时间和流量大小。

所以“流量经过代理”不等于“代理一定解密 HTTPS”。

### TLS Inspection / HTTPS 解密

**TLS Inspection（TLS 检查）**也常被称为 HTTPS Inspection 或 TLS Interception。

它通常需要：

1. 设备安装并信任代理机构的根证书；
2. 代理拦截浏览器发往网站的连接；
3. 代理动态生成一个浏览器会信任的网站证书；
4. 浏览器与代理建立第一条 TLS 连接；
5. 代理与真实网站建立第二条 TLS 连接；
6. 代理在两条连接之间解密、检查并重新加密数据。

路径变成：

~~~mermaid
flowchart LR
    Browser["浏览器"] -->|TLS 连接 1| Inspect["受信任的 TLS 检查代理"]
    Inspect -->|TLS 连接 2| Site["真实网站"]
~~~

这不是一条端到端的浏览器到网站 TLS 连接，而是两条分别终止的 TLS 连接。

企业受管设备可能出于合规和安全目的部署 TLS 检查；来源不明的软件要求安装根证书则是高风险信号。不要安装自己无法确认来源和用途的根证书。

### 为什么有些应用在代理下证书报错

可能因为：

- 应用不使用 Windows 证书信任库；
- 应用自带 CA 证书包；
- 应用使用 Certificate Pinning（证书或公钥固定）；
- 代理生成的证书域名不匹配；
- 企业根证书没有安装到正确的信任库；
- 中间证书缺失；
- 系统时间错误。

相关代理路径见 [[系统代理、VPN与端口]]。

---

## Certificate Pinning 是什么

**Certificate Pinning（证书固定或公钥固定）**表示应用除普通证书链验证外，还要求服务器证书或公钥符合应用内预先记录的预期值。

它可以降低某些错误签发或异常信任根带来的风险，但也增加：

- 证书轮换难度；
- 灾难恢复风险；
- 企业 TLS 检查兼容问题；
- 客户端版本管理成本。

使用证书固定的应用即使系统信任企业代理根证书，也可能拒绝 TLS 检查生成的证书。

---

## TLS 在 CDN、负载均衡和反向代理哪里结束

用户访问网站时，TLS 终点不一定是网站应用程序所在的最终机器。

常见架构：

~~~text
浏览器
→ TLS
→ CDN / 负载均衡器 / 反向代理
→ TLS 或内部明文连接
→ 应用服务器
~~~

**TLS Termination（TLS 终止）**表示某个组件完成 TLS 握手并解密流量。

因此“HTTPS 端到端”要先明确端点是谁：

- 浏览器到 CDN；
- 浏览器到负载均衡器；
- 浏览器到应用服务器；
- 服务之间是否再次使用 TLS。

TLS 只能保护两个 TLS 端点之间的传输。数据在端点解密后，需要依靠应用权限、主机安全、数据库加密和内部网络安全继续保护。

---

## 常见 TLS 和证书错误

| 现象 | 常见含义 | 优先检查 |
|---|---|---|
| Certificate expired | 证书已过期 | 证书日期、系统时间、服务器续期 |
| Certificate not yet valid | 证书尚未生效 | 系统时间、时区、证书生效时间 |
| Name mismatch | 证书身份与访问域名不匹配 | URL、SAN、SNI、代理 |
| Unknown CA / Untrusted issuer | 无法连接到受信任根 | 私有 CA、根证书、中间证书 |
| Incomplete chain | 服务器漏发中间证书 | 服务器证书链配置 |
| Handshake failure | 双方未能完成握手 | 版本、算法、客户端证书、SNI |
| Protocol version | 没有共同可用 TLS 版本 | 老旧客户端或服务器 |
| Connection reset | 连接被中断 | 防火墙、代理、服务器、协议不匹配 |
| 浏览器正常，Git/Python 失败 | 使用不同 TLS 库或信任库 | CA 包、Schannel、代理证书 |

### 为什么系统时间很重要

证书验证依赖当前时间。电脑时间严重错误时，大量正常网站会同时报告证书尚未生效或过期。

### 为什么直接访问 IP 容易证书错误

证书通常为域名签发。直接访问：

~~~text
https://203.0.113.10
~~~

客户端会检查证书是否适用于这个 IP；如果证书只有 `example.com`，身份就不匹配。另外，一台服务器可能依靠 SNI 在同一个 IP 上托管多个网站。

---

## Windows 上怎样查看和排查 TLS

先观察问题在哪一层，不要一看到证书错误就关闭验证。

### 第 1 步：确认 DNS 与端口

~~~powershell
Resolve-DnsName example.com
Test-NetConnection example.com -Port 443
~~~

如果域名无法解析或 443 端口完全不可达，应先排查 [[DNS域名系统|DNS]]、路由、防火墙或代理，而不是证书链。

### 第 2 步：查看系统时间

~~~powershell
Get-Date
~~~

确认日期、时间和时区正确。

### 第 3 步：让 curl 显示握手信息

Windows 自带或已安装 curl 时可以使用：

~~~powershell
curl.exe -v https://example.com/
~~~

可以观察：

- 连接的 IP；
- 是否使用代理；
- TLS 版本；
- 证书验证错误；
- HTTP 协议与响应。

`-v` 输出可能包含请求头或环境信息，公开分享前要删除 Cookie、Token 和其他敏感内容。

### 第 4 步：在浏览器查看证书

浏览器通常可以从地址栏的连接信息中查看：

- 证书适用域名；
- 签发者；
- 有效期；
- 证书链；
- 使用的连接协议。

不同浏览器版本入口会变化，不要只依赖固定按钮位置。

### 第 5 步：有 OpenSSL 时进一步检查

如果系统已经安装 OpenSSL：

~~~bash
openssl s_client -connect example.com:443 -servername example.com -showcerts
~~~

`-servername` 用于发送 SNI。这个命令适合观察服务器返回的证书链和握手信息。

不要为了测试来源不明的网站而导入它提供的根证书。

### 第 6 步：比较直连与代理路径

分别检查：

- 系统代理关闭；
- 系统代理开启；
- TUN/VPN 开启；
- 浏览器与命令行工具；
- 公司网络与可信的其他网络。

如果只有经过代理时证书签发者发生变化，应检查是否存在 TLS Inspection。

---

## 不要使用这些“快速修复”

### 不要长期使用 `--insecure` 或 `-k`

curl 的 `--insecure`/`-k` 会跳过重要的证书验证。它可能让命令暂时成功，但也可能把真正的中间人攻击伪装成“问题已解决”。

### 不要关闭程序的 TLS 验证

例如不要为了安装依赖而永久关闭：

- Git SSL 验证；
- Python/pip 证书验证；
- Node.js TLS 验证；
- 浏览器证书检查。

应先找出缺少的是哪条 CA 链、代理是否在检查 TLS，以及工具使用哪个信任库。

### 不要随意安装根证书

受信任根证书具有为大量网站签发“被本机信任证书”的能力。安装未知根证书等于授予很高的通信信任权限。

### 不要为了兼容一台旧设备全局启用旧 TLS

如果必须维护老系统，应把兼容范围限制在隔离环境或特定服务，而不是降低整台电脑或所有服务的默认安全级别。

---

## 常见误区

### 误区 1：HTTPS 是一种新的网页格式

不是。HTTPS 仍然传输 HTTP 语义，只是通信受到 TLS 保护。

### 误区 2：TLS 使用证书公钥加密所有网页正文

不是。现代 TLS 通过握手完成身份认证和密钥协商，之后主要使用高效的对称认证加密保护数据。

### 误区 3：证书就是私钥

不是。证书通常包含公钥和身份信息；私钥必须由服务端秘密保存。

### 误区 4：证书有效就说明网站不会骗人

不是。证书主要证明服务身份绑定和安全连接，不评价商品、内容或经营者诚信。

### 误区 5：TLS 会隐藏目标 IP

不会。IP 路由需要知道数据发往哪里。代理/VPN 可以让本地网络只直接看到代理节点 IP，但这是流量路径变化，不是 TLS 单独完成的。

### 误区 6：TLS 1.3 一定隐藏域名

不一定。域名还可能通过 DNS、IP、传统 SNI 等信息暴露。ECH 能改善 ClientHello 隐私，但需要完整部署支持。

### 误区 7：有系统代理，代理一定能看到 HTTPS 正文

不一定。普通 CONNECT 隧道只转发端到端 TLS 数据；只有 TLS 检查、受信任中间证书或终端被控制等情况下，代理才可能获得明文。

### 误区 8：TLS 只能用在 443 端口

不是。443 是 HTTPS 常用端口，TLS 可以保护许多协议并运行在其他端口。

### 误区 9：TLS 取代了 TCP

不是。经典 TLS 常运行在 TCP 上；QUIC 则以不同方式集成 TLS 1.3。它们解决的问题不同。

### 误区 10：TLS 1.2 还能连接，所以和 TLS 1.3 完全一样

不是。正确配置的 TLS 1.2 可以安全使用，但更容易受复杂配置和历史选项影响；截至 2026 年，新标准与新协议已经明确向 TLS 1.3 集中。

---

## 三个完整例子

### 例子 1：访问 HTTPS 网站

~~~text
DNS 查询 example.com
→ 得到 IP
→ 建立 TCP 或 QUIC 连接
→ TLS 握手并验证证书
→ 协商应用协议
→ 发送加密 HTTP 请求
→ 接收加密 HTTP 响应
~~~

任何一步都可能失败，所以“网站打不开”不一定是 TLS 问题。

### 例子 2：公司代理检查 HTTPS

~~~text
公司设备信任企业根证书
→ 浏览器连接检查代理
→ 代理为目标域名生成受信任证书
→ 浏览器与代理建立 TLS
→ 代理与网站再建立 TLS
→ 代理根据策略检查明文
~~~

此时浏览器看到的证书签发者可能是企业内部 CA，而不是网站原本使用的公共 CA。

### 例子 3：浏览器能打开，Python 请求失败

可能原因：

- 浏览器使用系统信任库；
- Python 环境使用自己的 CA 包；
- 公司代理根证书只安装到了 Windows；
- Python 不信任代理生成的证书；
- 浏览器和 Python 使用不同代理路径。

正确思路是统一并理解信任链，而不是直接关闭 Python 的证书验证。

---

## 最小记忆模型

~~~mermaid
flowchart LR
    DNS["DNS：找到目标地址"] --> Transport["TCP 或 QUIC：建立传输路径"]
    Transport --> Handshake["TLS 握手：协商参数、验证身份、生成密钥"]
    Handshake --> Secure["安全通道：机密性 + 完整性 + 身份认证"]
    Secure --> App["HTTP、WebSocket、邮件、API 等应用数据"]
~~~

记住五句话：

1. TLS 的目标是建立安全通信通道；
2. 证书把服务身份与公钥绑定，私钥不能公开；
3. 握手负责认证和协商，后续正文主要用对称加密；
4. HTTPS 是受到 TLS 保护的 HTTP；
5. TLS 保护传输，不保证端点和业务本身绝对安全。

---

## 推荐学习顺序

1. 先理解 [[DNS域名系统|DNS]]、IP 和端口；
2. 再理解 [[TCP、HTTP、HTTPS与WebSocket|TCP 与 HTTP]]；
3. 记住 TLS 的机密性、完整性和身份认证；
4. 理解公钥、私钥、数字签名与对称加密的分工；
5. 理解根 CA、中间 CA、叶子证书和信任链；
6. 阅读 TLS 1.3 简化握手流程；
7. 学习 SNI、ALPN、ECH 和会话恢复；
8. 最后理解 mTLS、证书固定、TLS 检查和服务端配置。

---

## 关联概念

- [[DNS域名系统]]：TLS 连接前通常先通过域名解析得到目标地址。
- [[TCP、HTTP、HTTPS与WebSocket]]：TLS 与 TCP、QUIC、HTTPS 和 WSS 的关系。
- [[系统代理、VPN与端口]]：CONNECT 隧道、TLS 检查、代理证书与流量路径。
- [[状态机与幂等性]]：TLS 1.3 0-RTT 的重放风险为什么要求业务谨慎处理重复请求。
- [[SDK与API]]：API 客户端通常通过 TLS 验证服务身份并保护请求。
- [[MCP模型上下文协议]]：远程 MCP 常由 HTTPS/TLS 保护传输；MCP 规定能力调用，TLS 保护网络通道。
- [[CMD、Bash与PowerShell]]：使用 curl、OpenSSL 和 PowerShell 分层排查连接。

---

## 参考资料

以下资料于 **2026-08-21** 核对：

- [RFC 9846：The Transport Layer Security Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc9846.html)
- [RFC 9852：New Protocols Using TLS Must Require TLS 1.3](https://www.rfc-editor.org/rfc/rfc9852.html)
- [RFC 9851：TLS 1.2 is in Feature Freeze](https://www.rfc-editor.org/rfc/rfc9851.html)
- [RFC 10015：Deprecating Obsolete Key Exchange Methods in TLS 1.2 and DTLS 1.2](https://www.rfc-editor.org/rfc/rfc10015.html)
- [RFC 9525：Service Identity in TLS](https://www.rfc-editor.org/rfc/rfc9525.html)
- [RFC 5280：Internet X.509 Public Key Infrastructure Certificate and CRL Profile](https://www.rfc-editor.org/rfc/rfc5280.html)
- [RFC 6066：TLS Extensions，包括 SNI](https://www.rfc-editor.org/rfc/rfc6066.html)
- [RFC 9849：TLS Encrypted Client Hello](https://www.rfc-editor.org/rfc/rfc9849.html)
- [RFC 9001：Using TLS to Secure QUIC](https://www.rfc-editor.org/rfc/rfc9001.html)
- [Microsoft Learn：Schannel Error Codes for TLS and SSL Alerts](https://learn.microsoft.com/windows/win32/secauthn/schannel-error-codes-for-tls-and-ssl-alerts)
- [Microsoft Learn：TLS inspection troubleshooting](https://learn.microsoft.com/entra/global-secure-access/troubleshoot-transport-layer-security)
