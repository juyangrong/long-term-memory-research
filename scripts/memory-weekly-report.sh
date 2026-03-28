#!/bin/bash
# 定时任务周报生成脚本
# 每周一执行，汇总上周所有任务执行情况

set -e

LOG_DIR="/home/rskuser/.openclaw/workspace/memory/task-logs"
REPORT_DIR="/home/rskuser/.openclaw/workspace/memory/reports"
SCRIPTS_DIR="/home/rskuser/.openclaw/workspace/scripts"

mkdir -p "$REPORT_DIR"

# 计算上周的周数
LAST_WEEK=$(date -d "last week" '+%Y-W%W')
LAST_WEEK_START=$(date -d "last week monday" '+%Y-%m-%d')
LAST_WEEK_END=$(date -d "last week sunday" '+%Y-%m-%d')
TODAY=$(date '+%Y-%m-%d')

WEEKLY_LOG="$LOG_DIR/$LAST_WEEK.jsonl"
REPORT_FILE="$REPORT_DIR/weekly-report-$LAST_WEEK.md"

echo "=========================================="
echo "生成定时任务周报"
echo "报告周期：$LAST_WEEK_START 至 $LAST_WEEK_END"
echo "=========================================="
echo ""

# 检查日志文件是否存在
if [ ! -f "$WEEKLY_LOG" ]; then
    echo "⚠️  上周日志文件不存在：$WEEKLY_LOG"
    echo "   可能是第一周运行，创建空报告..."
    
    cat > "$REPORT_FILE" << EOF
# 定时任务周报 - $LAST_WEEK

**报告周期**: $LAST_WEEK_START 至 $LAST_WEEK_END  
**生成时间**: $TODAY

---

## ⚠️ 无执行记录

这是监控系统的第一个报告周期，暂无历史数据。

从本周开始，所有定时任务的执行记录将被自动记录。

---

## 📋 配置的定时任务

| 任务名称 | 频率 | 执行时间 | 状态 |
|----------|------|----------|------|
| 记忆健康监控 | 每周 | 周一 09:00 | 🟡 待监控 |
| 记忆备份 | 每周 | 周日 23:00 | 🟡 待监控 |
| 记忆维护 | 每月 | 1 号 10:00 | 🟡 待监控 |

---

*报告由 memory-weekly-report.sh 自动生成*
EOF
    
    echo "✅ 已创建空报告：$REPORT_FILE"
    exit 0
fi

# 统计任务执行情况
echo "📊 统计任务执行情况..."

# 解析 JSONL 日志
declare -A TASK_SUCCESS
declare -A TASK_FAILED
declare -A TASK_SKIPPED
declare -a ALL_TASKS
declare -a EXECUTION_LOG

while IFS= read -r line; do
    task=$(echo "$line" | jq -r '.task')
    status=$(echo "$line" | jq -r '.status')
    timestamp=$(echo "$line" | jq -r '.timestamp')
    message=$(echo "$line" | jq -r '.message')
    
    # 记录所有任务名称
    if [[ ! " ${ALL_TASKS[@]} " =~ " ${task} " ]]; then
        ALL_TASKS+=("$task")
    fi
    
    # 统计状态
    case "$status" in
        success)
            TASK_SUCCESS[$task]=$((${TASK_SUCCESS[$task]:-0} + 1))
            ;;
        failed)
            TASK_FAILED[$task]=$((${TASK_FAILED[$task]:-0} + 1))
            ;;
        skipped)
            TASK_SKIPPED[$task]=$((${TASK_SKIPPED[$task]:-0} + 1))
            ;;
    esac
    
    # 记录执行日志
    EXECUTION_LOG+=("$timestamp|$task|$status|$message")
done < "$WEEKLY_LOG"

# 计算总数
TOTAL_EXECUTIONS=${#EXECUTION_LOG[@]}
TOTAL_SUCCESS=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0

for task in "${ALL_TASKS[@]}"; do
    TOTAL_SUCCESS=$((TOTAL_SUCCESS + ${TASK_SUCCESS[$task]:-0}))
    TOTAL_FAILED=$((TOTAL_FAILED + ${TASK_FAILED[$task]:-0}))
    TOTAL_SKIPPED=$((TOTAL_SKIPPED + ${TASK_SKIPPED[$task]:-0}))
done

# 生成报告
echo "📝 生成周报..."

cat > "$REPORT_FILE" << EOF
# 定时任务周报 - $LAST_WEEK

**报告周期**: $LAST_WEEK_START 至 $LAST_WEEK_END  
**生成时间**: $TODAY $(date '+%H:%M:%S')

---

## 📊 执行摘要

| 指标 | 数值 | 百分比 |
|------|------|--------|
| 总执行次数 | $TOTAL_EXECUTIONS | 100% |
| ✅ 成功 | $TOTAL_SUCCESS | $(awk "BEGIN {printf \"%.1f\", ($TOTAL_SUCCESS/$TOTAL_EXECUTIONS)*100}")% |
| ❌ 失败 | $TOTAL_FAILED | $(awk "BEGIN {printf \"%.1f\", ($TOTAL_FAILED/$TOTAL_EXECUTIONS)*100}")% |
| ⏭️ 跳过 | $TOTAL_SKIPPED | $(awk "BEGIN {printf \"%.1f\", ($TOTAL_SKIPPED/$TOTAL_EXECUTIONS)*100}")% |

---

## 📋 任务详情

EOF

# 添加任务详情表格
echo "| 任务名称 | 成功 | 失败 | 跳过 | 成功率 |" >> "$REPORT_FILE"
echo "|----------|------|------|------|--------|" >> "$REPORT_FILE"

for task in "${ALL_TASKS[@]}"; do
    success=${TASK_SUCCESS[$task]:-0}
    failed=${TASK_FAILED[$task]:-0}
    skipped=${TASK_SKIPPED[$task]:-0}
    total=$((success + failed + skipped))
    
    if [ $total -gt 0 ]; then
        rate=$(awk "BEGIN {printf \"%.1f\", ($success/$total)*100}")
    else
        rate="N/A"
    fi
    
    # 状态图标
    if [ $failed -gt 0 ]; then
        status_icon="🔴"
    elif [ $skipped -gt 0 ]; then
        status_icon="🟡"
    else
        status_icon="🟢"
    fi
    
    echo "| $status_icon $task | $success | $failed | $skipped | $rate% |" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 添加详细执行日志
echo "## 📜 执行日志" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| 时间 | 任务 | 状态 | 备注 |" >> "$REPORT_FILE"
echo "|------|------|------|------|" >> "$REPORT_FILE"

for log_entry in "${EXECUTION_LOG[@]}"; do
    IFS='|' read -r timestamp task status message <<< "$log_entry"
    
    case "$status" in
        success) status_icon="✅" ;;
        failed) status_icon="❌" ;;
        skipped) status_icon="⏭️" ;;
        *) status_icon="❓" ;;
    esac
    
    echo "| $timestamp | $task | $status_icon $status | $message |" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 添加建议
echo "## 💡 建议与改进" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ $TOTAL_FAILED -gt 0 ]; then
    echo "### ⚠️ 需要关注" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "本周有 $TOTAL_FAILED 次任务执行失败，请检查以下内容：" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    for task in "${ALL_TASKS[@]}"; do
        if [ ${TASK_FAILED[$task]:-0} -gt 0 ]; then
            echo "- **$task**: 失败 ${TASK_FAILED[$task]} 次" >> "$REPORT_FILE"
        fi
    done
    echo "" >> "$REPORT_FILE"
else
    echo "### ✅ 运行正常" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    echo "所有定时任务执行正常，无需特别关注。" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

echo "*报告由 memory-weekly-report.sh 自动生成*" >> "$REPORT_FILE"

echo ""
echo "=========================================="
echo "✅ 周报生成完成"
echo "报告文件：$REPORT_FILE"
echo "=========================================="
echo ""

# 输出报告内容（用于推送）
echo "📤 准备推送内容..."
echo ""
cat "$REPORT_FILE"
