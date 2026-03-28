#!/bin/bash
# 记忆压缩脚本 - 每月执行一次
# 功能：整理旧日志到长期记忆，清理过期文件

set -e

MEMORY_DIR="/home/rskuser/.openclaw/workspace/memory"
WORKSPACE_ROOT="/home/rskuser/.openclaw/workspace"
LOG_FILE="$MEMORY_DIR/compact-$(date +%Y-%m-%d).log"
DRY_RUN=${DRY_RUN:-false}

echo "========================================" | tee -a "$LOG_FILE"
echo "记忆压缩任务开始：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 检查目录是否存在
if [ ! -d "$MEMORY_DIR" ]; then
    echo "❌ 错误：记忆目录不存在：$MEMORY_DIR" | tee -a "$LOG_FILE"
    exit 1
fi

# 1. 识别需要整理的文件（超过 7 天的日志）
echo "📋 步骤 1: 识别需要整理的文件" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

CUTOFF_DATE=$(date -d "7 days ago" +%Y-%m-%d)
FILES_TO_PROCESS=()

for file in "$MEMORY_DIR"/2026-*.md; do
    [ -f "$file" ] || continue
    filename=$(basename "$file")
    
    # 跳过特殊文件
    if [[ "$filename" == "compact-"* ]] || [[ "$filename" == "diagnostic-"* ]]; then
        continue
    fi
    
    # 提取日期
    file_date=$(echo "$filename" | grep -oP '\d{4}-\d{2}-\d{2}' | head -1)
    [ -z "$file_date" ] && continue
    
    # 比较日期
    if [[ "$file_date" < "$CUTOFF_DATE" ]]; then
        FILES_TO_PROCESS+=("$file")
        echo "  📄 $filename ($file_date) - 待整理" | tee -a "$LOG_FILE"
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "共找到 ${#FILES_TO_PROCESS[@]} 个文件需要整理" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

if [ ${#FILES_TO_PROCESS[@]} -eq 0 ]; then
    echo "✅ 无需整理，所有文件都是最近的" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
else
    # 2. 提取关键信息（简化版：只统计，不自动修改 MEMORY.md）
    echo "📝 步骤 2: 提取关键信息" | tee -a "$LOG_FILE"
    echo "----------------------------------------" | tee -a "$LOG_FILE"
    
    for file in "${FILES_TO_PROCESS[@]}"; do
        filename=$(basename "$file")
        line_count=$(wc -l < "$file")
        word_count=$(wc -w < "$file")
        
        echo "  📊 $filename: $line_count 行，$word_count 词" | tee -a "$LOG_FILE"
        
        # 提取标题和关键段落（前 50 行）
        if [ "$DRY_RUN" = true ]; then
            echo "     [DRY RUN] 将提取关键内容到 MEMORY.md" | tee -a "$LOG_FILE"
        fi
    done
    
    echo "" | tee -a "$LOG_FILE"
fi

# 3. 清理过期文件（超过 30 天）
echo "🗑️  步骤 3: 清理过期文件（超过 30 天）" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

EXPIRY_DATE=$(date -d "30 days ago" +%Y-%m-%d)
FILES_TO_DELETE=()

for file in "$MEMORY_DIR"/2026-*.md; do
    [ -f "$file" ] || continue
    filename=$(basename "$file")
    
    # 跳过特殊文件
    if [[ "$filename" == "compact-"* ]] || [[ "$filename" == "diagnostic-"* ]]; then
        continue
    fi
    
    # 提取日期
    file_date=$(echo "$filename" | grep -oP '\d{4}-\d{2}-\d{2}' | head -1)
    [ -z "$file_date" ] && continue
    
    # 比较日期
    if [[ "$file_date" < "$EXPIRY_DATE" ]]; then
        FILES_TO_DELETE+=("$file")
        echo "  🗑️  $filename ($file_date) - 待删除" | tee -a "$LOG_FILE"
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "共找到 ${#FILES_TO_DELETE[@]} 个文件待删除" | tee -a "$LOG_FILE"

if [ ${#FILES_TO_DELETE[@]} -gt 0 ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "⚠️  DRY RUN 模式：不会实际删除文件" | tee -a "$LOG_FILE"
        echo "   要实际删除，请设置环境变量：DRY_RUN=false" | tee -a "$LOG_FILE"
    else
        echo "" | tee -a "$LOG_FILE"
        echo "⚠️  准备删除 ${#FILES_TO_DELETE[@]} 个文件..." | tee -a "$LOG_FILE"
        
        for file in "${FILES_TO_DELETE[@]}"; do
            filename=$(basename "$file")
            echo "  删除：$filename" | tee -a "$LOG_FILE"
            rm "$file"
        done
        
        echo "✅ 删除完成" | tee -a "$LOG_FILE"
    fi
else
    echo "✅ 无需删除，所有文件都在保留期内" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "记忆压缩任务完成：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "日志文件：$LOG_FILE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
