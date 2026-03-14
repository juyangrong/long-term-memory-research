#!/bin/bash
# 长期记忆研究资料 - 更新脚本
# 使用方式：./update.sh [--dry-run] [--force] [--setup-cron]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
VENV_PYTHON="${WORKSPACE_ROOT}/venv/bin/python"
UPDATE_SCRIPT="${SCRIPT_DIR}/update_research.py"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  长期记忆研究资料更新工具${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查 Python 环境
if [ ! -f "$VENV_PYTHON" ]; then
    echo -e "${YELLOW}⚠️  虚拟环境不存在，创建中...${NC}"
    cd "$WORKSPACE_ROOT"
    python3 -m venv venv
    source venv/bin/activate
    pip install -q requests beautifulsoup4
    echo -e "${GREEN}✅ 虚拟环境已创建${NC}"
fi

# 解析参数
DRY_RUN=""
FORCE=""
SETUP_CRON=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        --force)
            FORCE="--force"
            shift
            ;;
        --setup-cron)
            SETUP_CRON="--setup-cron"
            shift
            ;;
        -h|--help)
            echo "使用方式：$0 [选项]"
            echo ""
            echo "选项:"
            echo "  --dry-run    干运行，不实际更新"
            echo "  --force      强制更新 (忽略时间间隔)"
            echo "  --setup-cron 设置定时任务 (每两天)"
            echo "  -h, --help   显示帮助"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 未知选项：$1${NC}"
            exit 1
            ;;
    esac
done

# 执行更新
if [ -n "$SETUP_CRON" ]; then
    echo -e "${YELLOW}⚙️  设置定时任务...${NC}"
    $VENV_PYTHON "$UPDATE_SCRIPT" --setup-cron --workspace "$WORKSPACE_ROOT" --python "$VENV_PYTHON"
else
    echo -e "${YELLOW}🚀 开始更新...${NC}"
    echo ""
    $VENV_PYTHON "$UPDATE_SCRIPT" $DRY_RUN $FORCE --workspace "$WORKSPACE_ROOT"
    echo ""
    echo -e "${GREEN}✅ 更新完成!${NC}"
fi

echo ""
echo "查看更新日志：${SCRIPT_DIR}/../.update_log.md"
echo "查看更新状态：${SCRIPT_DIR}/../.update_state.json"
