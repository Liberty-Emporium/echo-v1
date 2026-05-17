# Redis Memory System — 跨 Session 短期记忆

开箱即用。运行安装脚本后无需任何配置，自动读写 Redis。

## 一键安装

```bash
chmod +x scripts/setup.sh
bash scripts/setup.sh
```

安装后自动：
- 每次 Session 启动 → 加载近期记忆
- 每小时整点 → 写入时间戳保底
- 对话结束 → 自动写入摘要

## 手动安装

```bash
# 1. 安装并启动 Redis
apt install redis-server -y     # 或 yum install redis
redis-server --daemonize yes

# 2. 验证
redis-cli PING   # → PONG

# 3. 使用脚本
chmod +x scripts/redis_memory.sh
bash scripts/redis_memory.sh set 用户名 2026-05-17 "今天聊了什么"
bash scripts/redis_memory.sh get 用户名
```

## ⚠️ Redis 持久化

**默认不保证持久化。** 如需重启不丢数据，修改 `/etc/redis/redis.conf`：

```conf
save 900 1
appendonly yes
```

不改也行——7 天过期，丢了就当自然遗忘。

## 安全

- 默认监听 127.0.0.1，仅本机可访问
- 数据存明文，**不要存密码或密钥**
- 7 天 TTL 自动过期，无需手动清理

## 文件

```
redis-memory-system/
├── README.md
├── SKILL.md
└── scripts/
    ├── setup.sh                   # 一键安装
    ├── redis_memory.sh            # 通用版
    └── redis_memory_isolated.sh   # 隔离版
```
