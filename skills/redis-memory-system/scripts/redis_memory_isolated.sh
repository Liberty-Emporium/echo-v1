#!/bin/bash
# 隔离版 Redis 记忆脚本 - 硬编码 memory:<用户名>
# 用法: ./redis_memory_isolated.sh get [date]
#        ./redis_memory_isolated.sh set <date> <summary>
#        ./redis_memory_isolated.sh recent [days]
#
# 使用前必须先设定 REDIS_MEMORY_USER 环境变量
set -euo pipefail

USERNAME="${REDIS_MEMORY_USER:-}"
[ -z "$USERNAME" ] && { echo "❌ 请设置 REDIS_MEMORY_USER 环境变量" >&2; exit 1; }

KEY="memory:${USERNAME}"

[ $# -lt 1 ] && { echo "❌ 缺少参数
try: \`$0 get [date]\` | \`$0 set <date> <summary>\`" >&2; exit 1; }

ACTION=$1
DATE=${2:-}
shift 2 2>/dev/null
SUMMARY="$*"

validate_date() {
    local d="$1"
    [ -z "$d" ] && return 0
    if ! echo "$d" | grep -qxE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
        echo "❌ 日期格式错误: $d（需要 YYYY-MM-DD）" >&2
        exit 1
    fi
    if ! date -d "$d" >/dev/null 2>&1; then
        echo "❌ 无效日期: $d" >&2
        exit 1
    fi
}

case $ACTION in
    get)
        if [ -z "$DATE" ]; then
            for d in $(seq 0 3); do
                day=$(date -d "-$d days" +%Y-%m-%d 2>/dev/null)
                val=$(redis-cli HGET "$KEY" "$day" 2>/dev/null)
                [ -n "$val" ] && echo "[$day] $val"
            done
        else
            validate_date "$DATE"
            val=$(redis-cli HGET "$KEY" "$DATE" 2>/dev/null)
            [ -n "$val" ] && echo "[$DATE] $val" || echo "（无记录）"
        fi
        ;;
    set)
        [ -z "$DATE" ] && { echo "❌ 缺少日期参数" >&2; exit 1; }
        [ -z "$SUMMARY" ] && { echo "❌ 缺少摘要内容" >&2; exit 1; }
        validate_date "$DATE"
        redis-cli HSET "$KEY" "$DATE" "$SUMMARY" > /dev/null
        redis-cli EXPIRE "$KEY" 604800 > /dev/null
        echo "✅ 已记录（${USERNAME}）"
        ;;
    recent)
        if [ -n "$DATE" ]; then
            if ! echo "$DATE" | grep -qxE '^\+?[0-9]+$'; then
                echo "❌ 天数参数错误: $DATE（需要正整数）" >&2
                exit 1
            fi
        fi
        days=${DATE:-3}
        for d in $(seq 0 $days); do
            day=$(date -d "-$d days" +%Y-%m-%d 2>/dev/null)
            val=$(redis-cli HGET "$KEY" "$day" 2>/dev/null)
            [ -n "$val" ] && echo "[$day] $val"
        done
        ;;
    *)
        echo "隔离版 Redis 记忆系统 (${USERNAME}):"
        echo "  get [date]       - 查记忆"
        echo "  set <date> <msg> - 写记忆"
        echo "  recent [days]    - 查最近"
        echo ""
        echo "环境变量: REDIS_MEMORY_USER=<用户名>（必填）"
        exit 1
        ;;
esac
