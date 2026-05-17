---
name: redis-memory-system
description: Redis-based cross-session memory system for OpenClaw agents. One-command setup, zero config. Automatically reads recent memory at session start (via bootstrap) and writes hourly summaries (via system cron). 7-day TTL, multi-user isolation via dual scripts. Use when agents need short-term memory that survives session resets without manual configuration, or when implementing multi-account memory isolation.
---

# Redis 记忆系统

跨 session 短期记忆。所有数据 7 天自动过期，不撑磁盘。

## 适用场景 ✅

- **跨 session 记忆保持** — Agent 会话被回收后（04:00重置/空闲120分钟/24h无交互），醒来能记得之前聊了什么
- **多账号隔离** — 同一 Redis 实例服务多个用户，每人数据互不可见
- **短期记忆保底** — 对话意外中断时，Heartbeat 自动写入防止丢记忆
- **系统操作审计** — 记录下载文件、安装软件等后台操作，避免"谁干的"这类问题

## 不适用场景 ❌

- **单轮/单条对话查询** — 本技能只存**每日摘要**，不存逐条对话记录。想查某句话说过没有？这不适合你
- **永久记忆** — 数据 7 天自动过期。要永久保留请配合 MEMORY.md
- **实时消息同步** — 这不是消息队列，不是 WebSocket 替代品
- **大规模数据存储** — 每条记忆建议 < 2KB，存大文件请用正经数据库
- **没有 Redis 的环境** — 如果机器没装 Redis，这个技能没用

## 一句话架构

```
Session → Redis（7天短期） → Heartbeat（自动续写） → MEMORY.md（长期提炼）
```

## 一键安装（推荐）

```bash
# 一条命令配好所有
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

安装完成后自动生效：
- ✅ **每次 session 启动** → .bootstrap 自动加载近期记忆
- ✅ **每小时整点** → 系统 cron 自动写入时间戳
- ✅ **对话结束时** → 自动按规则写入摘要

## 手动配置

```bash
# 1️⃣ 确保 Redis 运行
redis-server --daemonize yes
redis-cli PING

# 2️⃣ 设置脚本
chmod +x scripts/*.sh

# 3️⃣ 写入记忆
bash scripts/redis_memory.sh set aaa 2026-05-17 "今天聊了什么"

# 4️⃣ 查记忆
bash scripts/redis_memory.sh get aaa
```

## 脚本

### `scripts/redis_memory.sh` — 通用版

多用户，用 `memory:<用户名>` 的 hash 结构隔离。

```bash
bash scripts/redis_memory.sh get aaa              # 查最近3天
bash scripts/redis_memory.sh get aaa 2026-05-17   # 查某天
bash scripts/redis_memory.sh set aaa 2026-05-17 "聊了xxx"
bash scripts/redis_memory.sh recent aaa 7         # 查最近7天
bash scripts/redis_memory.sh action 2026-05-17    # 记录系统操作
```

### `scripts/redis_memory_isolated.sh` — 单用户隔离版

硬编码 key 为固定用户名，通过环境变量指定用户，杜绝跨账号误操作。

```bash
REDIS_MEMORY_USER=aaa bash scripts/redis_memory_isolated.sh get           # 查最近3天
REDIS_MEMORY_USER=aaa bash scripts/redis_memory_isolated.sh set 2026-05-17 "摘要"
```

## 核心设计

### 存储结构

```
memory:<用户名>          → Redis Hash（用户记忆）
  └─ 2026-05-16          → "今天的摘要内容"
  └─ 2026-05-17          → "今天的摘要内容"

actions:system           → Redis Hash（系统操作记录）
  └─ 2026-05-16          → "下载了什么文件"
```

KEY 级 TTL = 7 天（604800 秒）。写入即刷新。

### 会话回收临界点

- **04:00 每日重置**（框架层）
- **120分钟空闲重置**（框架层）
- **24小时无交互**（微信/消息平台层）

这些时刻之后 session 会丢失上下文，Redis 是唯一的找回路径。

### 自动读取（一键安装后自动生效）

一键安装会在 workspace 创建 `.bootstrap/redis-memory.md`，每次 session 启动时自动加载 Redis 查询指令。无需配置 SOUL.md 铁律。

### 手动写入规则（Agent 行为）

Agent 在以下时刻应主动写入 Redis：
1. **对话结束时** — 用户说「睡了/拜拜/晚安」
2. **空闲时** — 检测到用户已离线（>30分钟无响应）
3. **重要事件** — 下载文件、安装软件、做决策

### Heartbeat 自动写入（HEARTBEAT.md）

Heartbeat 中加一段自动检查逻辑，做保底写入：

```markdown
## 🧠 Redis 记忆写入（每轮心跳执行）

1. 查今天是否已写过 Redis
2. 判断是否有新对话
3. 有更新就写入
4. 超过4小时无互动则跳过
```

这样即使会话意外中断，下一次 Heartbeat 也会把记忆存好。

## 多用户隔离方案

| 场景 | 方案 |
|------|------|
| 单用户 | 直接用 `redis_memory.sh` |
| 多用户但互信 | 共用 `redis_memory.sh`，按用户名读写 |
| **多用户需完全隔离** | 每人一个隔离版脚本 + SOUL.md 铁律 |

隔离版脚本（`redis_memory_isolated.sh`）要求通过 `REDIS_MEMORY_USER` 环境变量指定用户，从技术层面杜绝硬编码错误。配合 SOUL.md 的铁律禁止跨账号读取，形成**技术 + 行为**双重保障。

### SOUL.md 隔离铁律范本

```markdown
## 🔴 Redis 隔离铁律（跨账号记忆保护）

| 用户 | 脚本 | 数据key |
|------|------|---------|
| 用户A | `scripts/redis_memory_a.sh` | `memory:用户A` |
| 用户B | `scripts/redis_memory_b.sh` | `memory:用户B` |

### 对话中的选择规则
- **用户A的 session** → 只用 `redis_memory_a.sh`
- **用户B的 session** → 只用 `redis_memory_b.sh`

### ❌ 绝对禁止
- 在用户A的对话里读取用户B的Redis记忆
- 用A的脚本查B的数据
- 主动告诉任何一方对方在Redis里存了什么
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Redis host | localhost | 可通过环境变量 `REDIS_HOST` 配置 |
| Redis port | 6379 | 可通过环境变量 `REDIS_PORT` 配置 |
| TTL | 604800 (7天) | 可通过脚本内 `EXPIRE` 命令调整 |
| 查询窗口 | 最近3天 | `get` 默认查3天；`recent N` 可调 |

## 磁盘占用预估

每条记忆约 500 字节 - 2 KB。4个用户每天对话，一年的数据量 < 5 MB。
内存占用同理——7天窗口在 Redis 里不过几十 KB。
