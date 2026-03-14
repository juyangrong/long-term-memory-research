# 长期记忆研究资料 - 自动更新脚本

**最后更新**: 2026-03-14

---

## 快速开始

### 首次使用

```bash
# 1. 进入目录
cd /home/rskuser/.openclaw/workspace/memory-research

# 2. 设置执行权限
chmod +x update.sh

# 3. 干运行测试
./update.sh --dry-run

# 4. 执行更新
./update.sh

# 5. 设置定时任务 (每两天自动更新)
./update.sh --setup-cron
```

---

## 命令选项

| 选项 | 说明 |
|------|------|
| `--dry-run` | 干运行，不实际更新 (仅显示将更新什么) |
| `--force` | 强制更新 (忽略时间间隔检查) |
| `--setup-cron` | 设置 crontab 定时任务 |
| `-h, --help` | 显示帮助信息 |

---

## 定时任务配置

### 自动设置 (推荐)

```bash
./update.sh --setup-cron
```

### 手动设置

编辑 crontab:
```bash
crontab -e
```

添加以下行:
```cron
# 长期记忆研究资料更新 (每两天凌晨 2 点)
0 2 */2 * * /home/rskuser/.openclaw/workspace/venv/bin/python /home/rskuser/.openclaw/workspace/memory-research/scripts/update_research.py >> /tmp/memory_research_update.log 2>&1
```

### 验证定时任务

```bash
# 查看当前 crontab
crontab -l

# 查看系统日志
grep CRON /var/log/syslog | tail -20
```

---

## 更新内容

自动更新脚本会:

1. **搜索新论文**
   - arXiv 最新论文
   - 学术会议 (ICLR, ACL, NeurIPS 等)
   - 期刊文章

2. **监控项目更新**
   - GitHub Release
   - 版本更新
   - 新功能发布

3. **更新文档**
   - `03-全网资料深度探索/01-学术研究前沿.md`
   - `03-全网资料深度探索/02-工业界落地案例.md`
   - `03-全网资料深度探索/03-开源项目对比.md`

4. **生成报告**
   - 更新摘要
   - 详细变更列表
   - 下次更新时间

---

## 日志与状态

### 更新日志

位置：`.update_log.md`

内容示例:
```markdown
# 研究资料更新报告

**更新日期**: 2026-03-16 02:00
**更新类型**: 定期

## 更新摘要

- 新论文：2 篇
- 新项目更新：1 个
- 新案例：0 个

## 详细变更

### 论文更新
- Mem0 v2.0: Enhanced Graph Memory
- Letta 1.0 Release Notes

### 项目更新
- Mem0: v1.0 → v1.1

---
*下次自动更新：2026-03-18*
```

### 更新状态

位置：`.update_state.json`

内容示例:
```json
{
  "last_update": "2026-03-14T02:00:00",
  "update_count": 5,
  "papers_tracked": ["arXiv:2504.19413", "arXiv:2501.08765"],
  "projects_tracked": ["mem0ai/mem0", "cpacker/Letta"],
  "last_changes": {...}
}
```

---

## 手动更新

如需手动添加内容:

### 1. 添加新论文

编辑 `03-全网资料深度探索/01-学术研究前沿.md`:

```markdown
### 新论文标题
- **会议/期刊**: arXiv / ICLR / ACL / etc.
- **arXiv 编号**: 2XXX.XXXXX
- **机构**: 大学 / 研究机构
- **发布日期**: 2026-XX-XX
- **核心贡献**: 简述
- **链接**: https://...
```

### 2. 添加新案例

编辑 `03-全网资料深度探索/02-工业界落地案例.md`:

```markdown
### 案例 X: 公司名称
**公司**: 公司名  
**行业**: 行业  
**实施时间**: 2026-XX  
**用户规模**: XXX

**背景**: ...
**方案**: ...
**效果**: ...
```

### 3. 更新项目对比

编辑 `03-全网资料深度探索/03-开源项目对比.md`:

```markdown
### 项目名

**版本**: vX.X.X (更新日期)

**更新内容**:
- 新功能 1
- 新功能 2

**性能变化**: ...
```

---

## 故障排查

### 问题 1: 定时任务未执行

```bash
# 检查 cron 服务状态
systemctl status cron

# 查看 cron 日志
grep CRON /var/log/syslog | tail -50

# 检查脚本权限
ls -la update.sh scripts/update_research.py
```

### 问题 2: Python 环境错误

```bash
# 重新创建虚拟环境
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 问题 3: 更新失败

```bash
# 查看详细日志
cat /tmp/memory_research_update.log

# 强制更新
./update.sh --force
```

---

## 依赖

- Python 3.8+
- requests
- beautifulsoup4
- (可选) arxiv API 客户端

安装依赖:
```bash
pip install -r requirements.txt
```

---

## 最佳实践

1. **定期查看更新日志**
   ```bash
   cat .update_log.md | tail -50
   ```

2. **手动审核重要更新**
   - 新论文 → 评估是否值得跟踪
   - 项目更新 → 检查是否有破坏性变更
   - 工业案例 → 验证数据来源

3. **备份重要数据**
   ```bash
   # 每周备份
   tar -czf memory-research-backup-$(date +%Y%m%d).tar.gz memory-research/
   ```

4. **监控更新质量**
   - 检查是否有误报
   - 调整搜索关键词
   - 更新置信度阈值

---

## 扩展开发

### 添加新的数据源

编辑 `scripts/update_research.py`:

```python
def search_new_papers(self) -> List[Dict]:
    """搜索新论文"""
    # 添加新的 API 调用
    # 例如：arXiv API, Google Scholar, Semantic Scholar
    pass

def search_project_updates(self) -> List[Dict]:
    """搜索项目更新"""
    # 添加新的数据源
    # 例如：GitHub API, PyPI, npm
    pass
```

### 自定义更新逻辑

```python
def custom_update_logic(self):
    """自定义更新逻辑"""
    # 例如：发送通知邮件
    # 例如：更新内部数据库
    # 例如：生成周报
    pass
```

---

## 支持

如有问题，请查看:
- 更新日志：`.update_log.md`
- 更新状态：`.update_state.json`
- 系统日志：`/tmp/memory_research_update.log`

---

*最后更新：2026-03-14*
