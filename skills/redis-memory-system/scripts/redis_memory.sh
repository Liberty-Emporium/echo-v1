#!/bin/bash
# 拾光记忆系统 - Redis 操作助手
# 用法: ./redis_memory.sh get <user> [date]
#        ./redis_memory.sh set <user> <date> <summary>
#        ./redis_memory.sh recent <user> [days]
#        ./redis_memory.sh action <date> <desc>
set -euo pipefail

[ $# -lt 1 ] && { echo "❌ 缺少参数
try: \`$0 get <user> [date]\` | \`$0 set <user> <date> <summary>\`" >&2; exit 1; }

ACTION=$1
USER=${2:-}
DATE=${3:-}

# action <date> <desc> 格式特殊处理
if [ "$ACTION" = "action" ]; then
    shift 2 2>/dev/null
    SUMMARY="$*"
else
    shift 3 2>/dev/null
    SUMMARY="$*"
fi

# 校验 date 参数格式（如果传了）
validate_date() {
    local d="$1"
    # 允许 action 无 date
    [ -z "$d" ] && return 0
    # YYYY-MM-DD
    if ! echo "$d" | grep -qxE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
        echo "❌ 日期格式错误: $d（需要 YYYY-MM-DD）" >&2
        exit 1
    fi
    # 检查日期是否真实存在（闰年等）
    if ! date -d "$d" >/dev/null 2>&1; then
        echo "❌ 无效日期: $d" >&2
        exit 1
    fi
}

case $ACTION in
    get)
        if [ "$USER" = "actions" ]; then
            redis-cli HGETALL "actions:system" 2>/dev/null
        elif [ -z "$DATE" ]; then
            # 获取最近3天
            for d in $(seq 0 3); do
                day=$(date -d "-$d days" +%Y-%m-%d 2>/dev/null)
                val=$(redis-cli HGET "memory:$USER" "$day" 2>/dev/null)
                [ -n "$val" ] && echo "[$day] $val"
            done
        else
            validate_date "$DATE"
            val=$(redis-cli HGET "memory:$USER" "$DATE" 2>/dev/null)
            [ -n "$val" ] && echo "[$DATE] $val" || echo "（无记录）"
        fi
        ;;
    set)
        [ -z "$DATE" ] && { echo "❌ 缺少日期参数" >&2; exit 1; }
        [ -z "$SUMMARY" ] && { echo "❌ 缺少摘要内容" >&2; exit 1; }
        validate_date "$DATE"
        redis-cli HSET "memory:$USER" "$DATE" "$SUMMARY" > /dev/null
        redis-cli EXPIRE "memory:$USER" 604800 > /dev/null  # 7天过期
        echo "✅ 已记录"
        ;;
    recent)
        if [ -n "$DATE" ]; then
            # days 参数可以是纯数字，也可以有正号
            if ! echo "$DATE" | grep -qxE '^\+?[0-9]+$'; then
                echo "❌ 天数参数错误: $DATE（需要正整数）" >&2
                exit 1
            fi
        fi
        days=${DATE:-3}
        for d in $(seq 0 $days); do
            day=$(date -d "-$d days" +%Y-%m-%d 2>/dev/null)
            val=$(redis-cli HGET "memory:$USER" "$day" 2>/dev/null)
            [ -n "$val" ] && echo "[$day] $val"
        done
        ;;
    action)
        validate_date "$DATE"
        [ -z "$SUMMARY" ] && { echo "❌ 缺少操作描述" >&2; exit 1; }
        redis-cli HSET "actions:system" "$DATE" "$SUMMARY" > /dev/null
        redis-cli EXPIRE "actions:system" 604800 > /dev/null
        echo "✅ 已记录操作"
        ;;
    *)
        echo "用法:"
        echo "  get <user> [date]       - 查记忆"
        echo "  set <user> <date> <msg> - 写记忆"
        echo "  recent <user> [days]    - 查最近"
        echo "  action <date> <desc>    - 记录系统操作"
        exit 1
        ;;
esac
