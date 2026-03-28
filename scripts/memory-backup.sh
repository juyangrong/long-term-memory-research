#!/bin/bash
# 记忆备份脚本 - 每周执行一次
# 功能：导出记忆文件到备份目录，支持 Git 版本控制

set -e

MEMORY_DIR="/home/rskuser/.openclaw/workspace/memory"
BACKUP_DIR="/home/rskuser/.openclaw/workspace/memory/backups"
WORKSPACE_ROOT="/home/rskuser/.openclaw/workspace"
WEEKS_TO_KEEP=${WEEKS_TO_KEEP:-12}  # 默认保留 12 周备份

# 先创建备份目录（在写入日志之前）
mkdir -p "$BACKUP_DIR"
LOG_FILE="$BACKUP_DIR/backup-$(date +%Y-%m-%d).log"

echo "========================================" | tee -a "$LOG_FILE"
echo "记忆备份任务开始：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1. 创建备份目录
echo "📁 步骤 1: 创建备份目录" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "  ✅ 创建备份目录：$BACKUP_DIR" | tee -a "$LOG_FILE"
else
    echo "  ✅ 备份目录已存在：$BACKUP_DIR" | tee -a "$LOG_FILE"
fi

# 创建周备份子目录
WEEK_NUM=$(date +%Y-W%W)
WEEKLY_BACKUP="$BACKUP_DIR/$WEEK_NUM"

if [ ! -d "$WEEKLY_BACKUP" ]; then
    mkdir -p "$WEEKLY_BACKUP"
    echo "  ✅ 创建周备份目录：$WEEKLY_BACKUP" | tee -a "$LOG_FILE"
else
    echo "  ℹ️  周备份目录已存在：$WEEKLY_BACKUP" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"

# 2. 备份记忆文件
echo "📦 步骤 2: 备份记忆文件" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

BACKUP_COUNT=0
TOTAL_SIZE=0

# 备份所有 .md 文件（排除备份目录和日志文件）
for file in "$MEMORY_DIR"/*.md; do
    [ -f "$file" ] || continue
    filename=$(basename "$file")
    
    # 跳过备份目录和日志文件
    if [[ "$filename" == "compact-"* ]] || [[ "$filename" == "backup-"* ]] || [[ "$filename" == "diagnostic-"* ]]; then
        continue
    fi
    
    # 复制到周备份目录
    cp "$file" "$WEEKLY_BACKUP/"
    
    file_size=$(stat -c%s "$file" 2>/dev/null || echo "0")
    TOTAL_SIZE=$((TOTAL_SIZE + file_size))
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    
    echo "  📄 $filename ($(numfmt --to=iec-i --suffix=B $file_size 2>/dev/null || echo "${file_size}B"))" | tee -a "$LOG_FILE"
done

echo "" | tee -a "$LOG_FILE"
echo "共备份 $BACKUP_COUNT 个文件，总大小 $(numfmt --to=iec-i --suffix=B $TOTAL_SIZE 2>/dev/null || echo "${TOTAL_SIZE}B")" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 3. 创建恢复点标签
echo "🏷️  步骤 3: 创建恢复点标签" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
cat > "$WEEKLY_BACKUP/BACKUP_INFO.md" << EOF
# 记忆备份信息

**备份时间**: $TIMESTAMP  
**备份周期**: $WEEK_NUM  
**文件数量**: $BACKUP_COUNT  
**总大小**: $(numfmt --to=iec-i --suffix=B $TOTAL_SIZE 2>/dev/null || echo "${TOTAL_SIZE}B")  
**保留策略**: 最近 $WEEKS_TO_KEEP 周

## 恢复说明

1. 停止 OpenClaw Gateway（可选）
2. 从备份目录复制文件到 memory/ 目录
3. 重启 Gateway

## 备份文件列表

$(ls -1 "$WEEKLY_BACKUP"/*.md 2>/dev/null | xargs -I {} basename {} | sed 's/^/- /')
EOF

echo "  ✅ 创建备份信息文件：BACKUP_INFO.md" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 4. 清理过期备份
echo "🗑️  步骤 4: 清理过期备份（超过 $WEEKS_TO_KEEP 周）" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

DELETED_COUNT=0

# 查找并删除超过保留周期的备份目录
for dir in "$BACKUP_DIR"/2026-W*; do
    [ -d "$dir" ] || continue
    
    dir_name=$(basename "$dir")
    # 提取周数（简化处理：直接比较日期）
    dir_date=$(echo "$dir_name" | grep -oP '\d{4}-W\d{2}' | head -1)
    [ -z "$dir_date" ] && continue
    
    # 转换为日期进行比较（简化：删除超过 3 个月的备份）
    cutoff_week=$(date -d "$WEEKS_TO_KEEP weeks ago" +%Y-W%W)
    
    if [[ "$dir_name" < "$cutoff_week" ]]; then
        echo "  🗑️  删除过期备份：$dir_name" | tee -a "$LOG_FILE"
        rm -rf "$dir"
        DELETED_COUNT=$((DELETED_COUNT + 1))
    fi
done

echo "" | tee -a "$LOG_FILE"
if [ $DELETED_COUNT -gt 0 ]; then
    echo "已删除 $DELETED_COUNT 个过期备份" | tee -a "$LOG_FILE"
else
    echo "✅ 无需清理，所有备份都在保留期内" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"

# 5. Git 提交（可选）
echo "📝 步骤 5: Git 提交（可选）" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

if git -C "$WORKSPACE_ROOT" rev-parse --git-dir > /dev/null 2>&1; then
    cd "$WORKSPACE_ROOT"
    
    # 检查是否有变更
    if ! git diff --quiet || git ls-files --others --exclude-standard | grep -q "memory/backups"; then
        git add memory/backups/
        git commit -m "chore(memory): 自动备份 - $WEEK_NUM ($BACKUP_COUNT 个文件)"
        echo "  ✅ Git 提交成功" | tee -a "$LOG_FILE"
    else
        echo "  ℹ️  无变更，跳过提交" | tee -a "$LOG_FILE"
    fi
else
    echo "  ⚠️  不在 Git 仓库中，跳过提交" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "记忆备份任务完成：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "备份位置：$WEEKLY_BACKUP" | tee -a "$LOG_FILE"
echo "日志文件：$LOG_FILE" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
