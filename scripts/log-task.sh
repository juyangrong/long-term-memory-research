#!/bin/bash
# 定时任务执行日志记录器
# 用法：./log-task.sh <task_name> <status> [message]

set -e

LOG_DIR="/home/rskuser/.openclaw/workspace/memory/task-logs"
mkdir -p "$LOG_DIR"

TASK_NAME="$1"
STATUS="$2"  # success, failed, skipped
MESSAGE="$3"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y-%m-%d')
WEEK_NUM=$(date '+%Y-W%W')

if [ -z "$TASK_NAME" ] || [ -z "$STATUS" ]; then
    echo "用法：$0 <task_name> <status> [message]"
    echo "示例：$0 memory-backup success '备份完成'"
    exit 1
fi

# 写入周日志文件
WEEKLY_LOG="$LOG_DIR/$WEEK_NUM.jsonl"

cat >> "$WEEKLY_LOG" << EOF
{"timestamp":"$TIMESTAMP","date":"$DATE","week":"$WEEK_NUM","task":"$TASK_NAME","status":"$STATUS","message":"$MESSAGE"}
EOF

echo "✅ 任务日志已记录：$TASK_NAME - $STATUS"

# 同时写入今日汇总
TODAY_LOG="$LOG_DIR/$DATE.md"
if [ ! -f "$TODAY_LOG" ]; then
    cat > "$TODAY_LOG" << EOF
# 任务执行日志 - $DATE

| 时间 | 任务 | 状态 | 备注 |
|------|------|------|------|
EOF
fi

echo "| $TIMESTAMP | $TASK_NAME | $STATUS | $MESSAGE |" >> "$TODAY_LOG"
