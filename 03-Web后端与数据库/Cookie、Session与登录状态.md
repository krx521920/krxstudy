---
title: Cookie、Session与登录状态
aliases:
  - Cookie
  - 设置Cookie
  - 浏览器Cookie
  - Session与Cookie
tags:
  - Web后端
  - 浏览器
  - 身份认证
  - Web安全
created: 2026-09-24
updated: 2026-09-24
verified: 2026-09-24
---

# Cookie、Session与登录状态

## 一句话解释

**Cookie 是浏览器保存、并在符合规则的请求中自动带回服务器的小段数据；开发时可以由后端用 `Set-Cookie` 设置，也可以由网页用 `document.cookie` 设置普通 Cookie。登录凭证应由后端在验证身份后，通过受保护的 Cookie 下发。**

Cookie 读作“库基”，本义是饼干，不是英文缩写。这里不是安装某个软件，也不是从其他网站复制一份登录信息，而是在自己的网站中设置浏览器状态。

生活类比：网站像酒店，Cookie 可以装一张“房卡编号”；服务器再查记录，判断这张卡属于谁、是否有效、可以开哪些门。Cookie 本身只是载体，不会自动证明身份，也不是所有 Cookie 都是房卡——它还可以记住语言和主题。

## 谁设置、谁保存、谁检查

**HTTP = Hypertext Transfer Protocol，超文本传输协议**，逐字母读 H-T-T-P；它规定浏览器与服务器怎样交换请求和响应。HTTP 本身不会自动记住“上一条请求已经登录”。

```text
浏览器请求网站
→ 后端响应中附带 Set-Cookie，要求保存一条数据
→ 浏览器按规则决定是否接受并保存
→ 后续符合条件的请求带上 Cookie
→ 后端读取并校验，决定返回什么
```

前端脚本也可以设置非 HttpOnly Cookie，但不能替服务器决定用户是否有权限。基础网络概念见 [[TCP、HTTP、HTTPS与WebSocket]]。[Cookie 入门](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)

## 方法一：前端设置普通偏好

在自己网站的前端 JavaScript 中，例如“切换深色主题”的按钮处理函数里，可以写：

```javascript
document.cookie = "theme=dark; Path=/; Max-Age=604800; SameSite=Strict; Secure";
```

这表示保存 `theme` 这个名字，对应值为 `dark`，有效期最多 7 天，适用路径从 `/` 开始。示例按安全的 HTTPS 网站编写。**HTTPS = Hypertext Transfer Protocol Secure，安全超文本传输协议**，读 H-T-T-P-S；具体加密机制见 [[TLS与数字证书]]。

这里的 `SameSite=Strict` 是同站教学场景下的保守选择；从外站链接首次进入时可能不携带，不能机械套用到第三方登录等流程。

注意：

- `document.cookie` 是浏览器提供的接口，React 项目同样可以调用，见 [[React组件化前端开发]]。
- 写入 Cookie 只保存数据，**不会自动把页面变成深色**；页面仍需读取偏好并应用相应样式。
- 同名、同域、同路径的普通 Cookie 可以更新；一次赋值不等于清空所有其他 Cookie。
- 前端不能设置 `HttpOnly`，也不能用 `document.cookie` 读取或覆盖已有的 HttpOnly Cookie。
- Cookie 数据不可信，不能把 `role=admin` 或 `isLogin=true` 当成服务端授权依据。
- 纯前端的无敏感偏好也可考虑 `localStorage`（浏览器本地键值存储）；它不会像 Cookie 一样自动随请求发给服务器。不要因此把登录凭证随意存进去。

代码是学习示例，本次没有在你的浏览器或网站上执行。[Document.cookie 官方说明](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)

## 方法二：后端在响应中设置 Cookie

后端的通用方式是发送一条**响应头**。响应头是服务器返回的数据之外的附加说明：

```http
Set-Cookie: server_theme=dark; Path=/; Max-Age=604800; HttpOnly; Secure; SameSite=Strict
```

这次用 `server_theme`，与前端例子的 `theme` 区分。它是给后端读取的主题偏好，因此示范设置 `HttpOnly`；如果确实需要网页脚本直接读取普通偏好，就要按用途调整，不能照搬登录凭证的策略。

下次符合规则的请求，浏览器可能自动带上：

```http
Cookie: server_theme=dark
```

**`Set-Cookie` 是服务器告诉浏览器“请保存”；`Cookie` 是浏览器告诉服务器“我带来了这些值”。** 后续请求不会把 `HttpOnly`、`SameSite` 等属性原样带回。协议基础参考 [HTTP 状态管理规范](https://www.rfc-editor.org/rfc/rfc6265)。

不能仅在响应正文中返回一段名为 `Set-Cookie` 的文字，就认为 Cookie 已设置；它必须成为真正的响应头。浏览器也不允许普通前端脚本手工设置请求中的 `Cookie` 头，或通过 `fetch` 响应头接口读取 `Set-Cookie`。[Set-Cookie 说明](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)

### Java / Spring Boot 怎么写

下面是**已有控制器方法中的核心片段**，不是完整项目，也不是登录接口。需要导入 `org.springframework.http` 包中的 `ResponseCookie`、`ResponseEntity`、`HttpHeaders`；所属方法的返回类型可以是 `ResponseEntity<String>`。

```java
ResponseCookie cookie = ResponseCookie.from("server_theme", "dark")
    .path("/")
    .maxAge(604800)
    .httpOnly(true)
    .secure(true)
    .sameSite("Strict")
    .build();

return ResponseEntity.ok()
    .header(HttpHeaders.SET_COOKIE, cookie.toString())
    .body("已保存主题偏好");
```

- 前一段构造 Cookie，`maxAge` 的这个重载以秒为单位；创建对象本身还没有发给浏览器。
- 后一段把它加入真实响应头，并返回一段提示文字。
- 如果发送多个 Cookie，要形成多条 `Set-Cookie` 响应头，不要把它们用逗号拼成一条。
- 当前仓库是笔记，不是 Spring Boot 应用；本次只核对了官方接口，未安装 Java 依赖或编译运行该片段。

框架背景见 [[Spring、Spring Boot、Spring MVC与SSM：Java后端框架关系]]；接口参考 [ResponseCookie 构造器](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/http/ResponseCookie.ResponseCookieBuilder.html) 和 [ResponseEntity 响应构造器](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/http/ResponseEntity.BodyBuilder.html)。

## 这些属性分别控制什么

| 属性 | 可以怎样理解 | 注意点 |
| --- | --- | --- |
| `Path=/` | 哪些请求路径可以携带 | 不是可靠的安全隔离机制，也不是电脑文件路径 |
| `Domain` | 可接收的主机范围 | 不写时限于设置它的主机；不能随意设置其他网站的域名，也不包含端口 |
| `Max-Age` | 从现在起最多保存多少秒 | `0` 用于立即过期；浏览器也可能提前清理 |
| `Expires` | 到哪个绝对时间过期 | 同时设置时通常以 `Max-Age` 为准 |
| `HttpOnly` | 不允许网页脚本直接访问该 Cookie | 浏览器仍可在符合条件的请求中自动携带；不等于杜绝所有脚本攻击 |
| `Secure` | 只通过安全连接发送 | 正式网站应使用 HTTPS；不是把 Cookie 值自身变成密文 |
| `SameSite` | 约束跨站场景下的携带 | 需结合业务、请求方式与浏览器策略选择 |

`SameSite` 常见值：`Strict` 严格限制为同站请求；`Lax` 还允许部分跨站顶级安全导航，例如从外站点链接打开；`None` 放开该属性的跨站限制，并要求 `Secure`，但不保证浏览器一定允许第三方 Cookie。

“会话 Cookie”是不设置 `Max-Age` 和 `Expires` 的 Cookie；不要保证“一关浏览器就一定没了”，浏览器的会话恢复可能保留它。Cookie 的保存期限与服务端登录会话期限，也不是同一回事。

## 登录 Cookie、Session 和 Token 是什么关系

**Session（会话，近似读“塞申”）**是应用用于连续识别多次交互的一组状态。常见方案是在服务器保存会话记录，浏览器 Cookie 只带一个难以猜测的会话标识。**Token（令牌，近似读“托肯”）**泛指某种凭证；可以放在 Cookie 中，也可能通过其他方式携带，二者不是互斥技术。

一次常见的登录流程：

1. 用户提交账号和密码，后端验证，不能仅相信前端显示“登录成功”。
2. 验证成功后，框架生成或轮换不可预测的会话标识，并在服务端记录身份与有效期。
3. 后端通过受保护的 Cookie 下发标识，不把密码或可随意修改的管理员权限放进去。
4. 访问订单等接口时，后端检查会话是否有效，并检查当前用户是否有权访问该订单。
5. 退出时，使服务端会话失效，同时删除浏览器中的相应 Cookie。

设置 Cookie 不等于完成登录系统。Java 项目通常应复用成熟的认证与会话框架，例如 Spring Security；它有登录后轮换会话标识等机制，不需要为学习 Cookie 从零拼装认证系统。[Spring Security 会话说明](https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html)

两个需要配套防护的风险：

- **XSS = Cross-Site Scripting，跨站脚本攻击**，读 X-S-S：不可信脚本在网页环境中执行。HttpOnly 减少直接窃取 Cookie 的途径，但恶意脚本仍可能发起用户权限下的请求。
- **CSRF = Cross-Site Request Forgery，跨站请求伪造**，读 C-S-R-F：恶意页面诱导浏览器带着现有凭证发起不该发生的操作。修改数据的请求需要框架提供的请求防伪令牌等防护，不能只依靠 SameSite，也不要为了消除报错随便关闭防护。

登录 Cookie 应视作敏感凭证，不要放进截图、日志、聊天或 Git 仓库。本篇只有虚构偏好值，不涉及真实登录凭证。会话管理依据 [OWASP 会话安全指南](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)，更多边界见 [[身份认证与授权：ACL、RBAC、MFA、OAuth、OIDC、SAML与SCIM]]、[[SSRF、DNS Rebinding与浏览器来源安全]]。

## 前后端分开部署，为什么 Cookie 没带过去

**来源（Origin）**由协议、主机和端口组成；任意一项不同就是跨来源。“同站”与“同来源”不同，例如 `https://app.example.com` 与 `https://api.example.com` 通常同站，但不同来源。

`fetch` 默认只为同来源请求携带凭证。若页面位于前者，要向自己的后端后者发送符合规则的 Cookie，可这样请求：

```javascript
fetch("https://api.example.com/me", {
  credentials: "include"
});
```

这里是读取个人信息的教学请求，不是修改数据的请求；`/me` 需要由自己的后端实现。`include` 不会绕过 Cookie 的域名、路径、SameSite、Secure 或浏览器隐私限制。[credentials 说明](https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials)

后端还需允许该前端来源读取带凭证的响应，例如：

```http
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Credentials: true
```

这是 **CORS = Cross-Origin Resource Sharing，跨来源资源共享**，常读“科尔斯”。带凭证时不能把允许来源简单写成 `*`，也不能不校验就回显任意来源；按请求动态选择允许来源时还应考虑 `Vary: Origin` 等缓存处理。复杂请求可能先发预检，需要完整配置。[CORS 官方说明](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)

跨来源不一定要求 `SameSite=None`：同站的不同子域可能不需要。反过来，真正跨站时即使配了 `None; Secure`，浏览器的第三方 Cookie 策略也可能阻止。不应为排错盲目关闭浏览器安全限制。

## 怎样确认设置成功

在自己的测试网站中，用 Chrome 开发者工具检查，不需要安装 Cookie 导出插件：

1. 按 `F12` 或 `Ctrl+Shift+I`，打开 **Network（网络）**，触发设置 Cookie 的操作。
2. 选中对应请求，在响应头中找 `Set-Cookie`；如果有阻止提示，先看具体原因。
3. 打开 **Application（应用）→ Storage（存储）→ Cookies → 对应网站**，检查是否保存了目标 Cookie。
4. 再发一次请求，查看请求头中的 `Cookie` 或 Cookies 子面板，确认是否携带。

“响应发出了”“浏览器保存了”“后续请求带上了”“服务器认可了”，是四个不同检查点。[Chrome 官方检查指南](https://developer.chrome.com/docs/devtools/application/cookies)

常见原因：选错前后端域名；路径不匹配；已过期；普通 HTTP 与 Secure 冲突；跨来源请求漏了凭证配置；跨站或隐私策略限制。HttpOnly 导致 `document.cookie` 看不到，是预期保护，不代表不存在。

开发时优先配置本地 HTTPS；`localhost` 在部分浏览器中有特殊处理，不代表任意内网 HTTP 地址也能设置 Secure Cookie。仅在明确的本地测试配置中按需调整安全属性，不把弱化配置带到生产，见 [[开发、测试、预发布与生产环境]]。

## 怎样删除

前端删除上面的普通偏好示例：

```javascript
document.cookie = "theme=; Path=/; Max-Age=0; SameSite=Strict; Secure";
```

后端删除上面的 HttpOnly 示例：

```http
Set-Cookie: server_theme=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Strict
```

需要匹配原 Cookie 的名称、域与路径；如果最初设置了 `Domain`，删除时也要匹配。这里示例均未设置 Domain。删除登录 Cookie 还要撤销服务端会话，否则已经泄漏的旧凭证可能仍有效。

## 初学者应记住什么

- Cookie 是状态存储与携带机制，不是数据库、密码管理器或万能登录方案。
- 普通无敏感偏好可以由前端设置；登录凭证由后端认证流程下发，并限制网页脚本访问。
- 不同 Cookie 不一定有相同安全需求，但服务器都不能盲信客户端提供的值。
- 不用先写完整登录系统：先练习设置一个主题值，再按四个检查点观察，最后学习会话与请求防伪。

## 参考资料

核对日期：2026-09-24。浏览器限制与框架接口可能变化，部署时按实际版本确认；本篇未读取真实 Cookie，也未运行应用代码。

- [MDN：Cookie 原理](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)、[Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)、[Document.cookie](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)。
- [RFC 6265](https://www.rfc-editor.org/rfc/rfc6265)：Cookie 基础协议；现代属性与浏览器策略另查对应文档。
- [Spring ResponseCookie](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/http/ResponseCookie.ResponseCookieBuilder.html)、[ResponseEntity](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/http/ResponseEntity.BodyBuilder.html)、[Spring Security 会话管理](https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html)。
- [MDN：credentials](https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials)、[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS)。
- [Chrome DevTools：检查 Cookie](https://developer.chrome.com/docs/devtools/application/cookies)。
- [OWASP：Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)。
