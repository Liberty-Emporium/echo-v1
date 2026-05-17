#!/bin/bash
# redis-memory-system 一键安装脚本
# 运行一次，自动配置自动读写
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SCRIPTS_DIR="$WORKSPACE/scripts"

echo "🔧 正在安装 redis-memory-system..."

# 1. 检查 Redis
if ! command -v redis-cli &>/dev/null; then
    echo "安装 Redis..."
    apt install -y redis-server 2>/dev/null || yum install -y redis 2>/dev/null
fi
redis-server --daemonize yes 2>/dev/null || true
redis-cli PING >/dev/null 2>&1 || { echo "❌ Redis 启动失败"; exit 1; }
echo "✅ Redis 运行中"

# 2. 拷贝脚本
mkdir -p "$SCRIPTS_DIR"
cp "$(dirname "$0")/redis_memory.sh" "$SCRIPTS_DIR/"
cp "$(dirname "$0")/redis_memory_isolated.sh" "$SCRIPTS_DIR/"
chmod +x "$SCRIPTS_DIR"/redis_memory*.sh
echo "✅ 脚本已安装到 $SCRIPTS_DIR"

# 3. 生成 BOOTSTRAP.md（每次 session 启动自动读 Redis）
BOOTSTRAP="$WORKSPACE/.bootstrap"
mkdir -p "$BOOTSTRAP"
cat > "$BOOTSTRAP/redis-memory.md" << 'BOOTSTRAPEOF'
# Redis Memory Auto-Load
本文件由 redis-memory-system 自动生成。

每次 session 启动时，先执行以下命令获取近期记忆：

```bash
bash scripts/redis_memory.sh get <用户名>
bash scripts/redis_memory.sh get actions
```

如果 Redis 中有近期记录，阅读后作为对话上下文。
如果 Redis 中无记录，说明是新用户或数据已过期。
BOOTSTRAPEOF
echo "✅ 启动自动加载已配置 (.bootstrap/redis-memory.md)"

# 4. 注册系统 cron（每小时写入保底）
CRON_SCRIPT="$SCRIPTS_DIR/cron_memory_ping.sh"
cat > "$CRON_SCRIPT" << 'CRONEOF'
#!/bin/bash
# redis-memory-system heartbeat ping
set -euo pipefail
TIMESTAMP=$(date '+%Y-%m-%d %H:00')
redis-cli HSET "memory:$(whoami)" "cron:$TIMESTAMP" "auto ping at $TIMESTAMP" > /dev/null
redis-cli EXPIRE "memory:$(whoami)" 604800 > /dev/null
CRONEOF
chmod +x "$CRON_SCRIPT"

# 去除旧的redis memory cron行，添加新的
(crontab -l 2>/dev/null | grep -v "redis_memory\|cron_memory_ping"; echo "0 * * * * $CRON_SCRIPT") | crontab -
echo "✅ 系统 cron 已注册（每小时自动写入）"

# 5. 写入一条安装记录
"$SCRIPTS_DIR/redis_memory.sh" set "$(whoami)" "$(date +%Y-%m-%d)" "redis-memory-system 已安装 ✅"

echo ""
echo "🎉 redis-memory-system 安装完成！"
echo ""
echo "自动读写链路："
echo "  📖 启动时 → .bootstrap 自动加载 Redis 记忆"
echo "  ✍️ 每小时 → cron 自动写入时间戳"
echo "  ✍️ 对话结束 → 在 SKILL.md 规则中自动写入摘要"
echo ""
echo "用户名: $(whoami)"
echo "Redis key: memory:$(whoami)"
echo ""
echo "试试: bash scripts/redis_memory.sh get $(whoami)"
