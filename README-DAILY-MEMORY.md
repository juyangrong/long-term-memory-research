# OpenClaw 每日记忆日志定时任务

**创建日期**: 2026 年 3 月 10 日  
**执行时间**: 每日凌晨 1:00 (Asia/Shanghai)  
**用途**: 自动汇总当日记忆并上传到 GitHub

---

## 📋 任务说明

**独立执行**: 此任务在日常会话之外独立运行，不干扰正常对话

**执行内容**:
1. 检查 `memory/YYYY-MM-DD.md` 是否存在
2. 如果存在，提交并推送到 GitHub
3. 记录执行日志

---

## 🔧 配置步骤

### 方法 1: 使用提供的 XML 文件 (推荐)

```powershell
# 1. 以管理员身份打开 PowerShell
# 2. 导入任务计划
Import-ScheduledTask -XmlPath "D:\Users\yr.ju.CN1\.openclaw\workspace\OpenClaw 每日记忆日志.xml" -TaskName "OpenClaw 每日记忆日志"

# 3. 验证任务
Get-ScheduledTask -TaskName "OpenClaw 每日记忆日志"
```

### 方法 2: 手动创建任务

#### 创建任务

```powershell
# 1. 打开任务计划程序
taskschd.msc

# 2. 创建基本任务
# 名称：OpenClaw 每日记忆日志
# 触发器：每天凌晨 1:00
# 操作：启动程序
```

#### 程序设置

**程序/脚本**:
```
C:\Program Files\nodejs\node.exe
```

**添加参数**:
```
"D:\Users\yr.ju.CN1\.openclaw\workspace\scripts\daily-memory-commit.js"
```

**起始于**:
```
D:\Users\yr.ju.CN1\.openclaw\workspace
```

#### 高级设置

- [x] 不管用户是否登录都要运行
- [x] 使用最高权限运行
- [x] 如果任务失败，重新启动间隔：5 分钟
- [ ] 仅在计算机使用交流电源时启动此任务 (笔记本取消勾选)

---

### 方法 2: 使用 cron (Linux/Mac)

```bash
# 编辑 crontab
crontab -e

# 添加每日凌晨 1:00 执行
0 1 * * * cd /path/to/workspace && node scripts/daily-memory-commit.js >> logs/daily-memory.log 2>&1
```

---

## 📝 脚本说明

### daily-memory-commit.js

```javascript
#!/usr/bin/env node

/**
 * OpenClaw 每日记忆日志自动提交脚本
 * 执行时间：每日凌晨 1:00
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = 'D:\\Users\\yr.ju.CN1\\.openclaw\\workspace';
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const LOG_FILE = path.join(WORKSPACE, 'logs', 'daily-memory.log');

// 获取今日日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
const memoryFile = path.join(MEMORY_DIR, `${dateStr}.md`);

// 日志函数
function log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}\n`;
    console.log(logMessage);
    fs.appendFileSync(LOG_FILE, logMessage);
}

// 检查文件是否存在
if (!fs.existsSync(memoryFile)) {
    log(`❌ 今日记忆文件不存在：${memoryFile}`);
    process.exit(0);
}

log(`✅ 找到记忆文件：${memoryFile}`);

try {
    // 切换到 workspace 目录
    process.chdir(WORKSPACE);
    
    // 设置 PATH (包含 GitHub CLI)
    const env = { ...process.env };
    const machinePath = execSync('powershell -Command "[System.Environment]::GetEnvironmentVariable(\'Path\',\'Machine\')"').toString().trim();
    const userPath = execSync('powershell -Command "[System.Environment]::GetEnvironmentVariable(\'Path\',\'User\')"').toString().trim();
    env.PATH = machinePath + ';' + userPath + ';' + env.PATH;
    
    // Git 添加
    log('📝 执行：git add memory/' + dateStr + '.md');
    execSync(`git add memory/${dateStr}.md`, { env, stdio: 'pipe' });
    
    // Git 提交
    const commitMsg = `docs(memory): 每日记忆日志自动提交 - ${dateStr}`;
    log(`📝 执行：git commit -m "${commitMsg}"`);
    execSync(`git commit -m "${commitMsg}"`, { env, stdio: 'pipe' });
    
    // Git 推送
    log('📝 执行：git push origin master');
    execSync('git push origin master', { env, stdio: 'pipe' });
    
    log('✅ 记忆日志上传成功！');
    
} catch (error) {
    log(`❌ 执行失败：${error.message}`);
    if (error.stdout) log(`stdout: ${error.stdout.toString()}`);
    if (error.stderr) log(`stderr: ${error.stderr.toString()}`);
    process.exit(1);
}
```

---

## 📁 文件结构

```
workspace/
├── scripts/
│   └── daily-memory-commit.js    # 自动提交脚本
├── memory/
│   └── YYYY-MM-DD.md             # 每日记忆日志
├── logs/
│   └── daily-memory.log          # 执行日志
└── README-DAILY-MEMORY.md        # 本文档
```

---

## 🔍 验证与监控

### 手动测试

```powershell
# 测试脚本
cd D:\Users\yr.ju.CN1\.openclaw\workspace
node scripts\daily-memory-commit.js

# 查看执行日志
Get-Content logs\daily-memory.log -Tail 20
```

### 查看任务状态

```powershell
# 查看任务计划
Get-ScheduledTask -TaskName "OpenClaw 每日记忆日志"

# 查看任务历史
Get-ScheduledTaskInfo -TaskName "OpenClaw 每日记忆日志"
```

### 日志检查

```powershell
# 查看最近执行日志
Get-Content logs\daily-memory.log -Tail 50

# 实时监控日志
Get-Content logs\daily-memory.log -Wait -Tail 10
```

---

## ⚙️ 配置选项

### 修改执行时间

**任务计划程序**:
1. 打开任务属性
2. 触发器 → 编辑
3. 修改时间为所需时间

**cron**:
```bash
# 每日凌晨 2:00
0 2 * * * ...

# 每日凌晨 3:30
30 3 * * * ...
```

### 修改日志目录

编辑脚本中的 `LOG_FILE` 路径：
```javascript
const LOG_FILE = path.join(WORKSPACE, 'logs', 'daily-memory.log');
```

---

## 🚨 故障排查

### 问题 1: 任务未执行

**检查**:
- 任务计划程序服务是否运行
- 用户权限是否正确
- 路径是否正确

### 问题 2: Git 推送失败

**检查**:
- GitHub 认证是否有效
- 网络连接是否正常
- 仓库是否存在

### 问题 3: 文件不存在

**说明**: 如果当日没有记忆日志，脚本会正常退出，这是预期行为

---

## 📊 执行记录

| 日期 | 状态 | 说明 |
|------|------|------|
| 2026-03-10 | 配置完成 | 创建脚本和定时任务 |

---

## 🎯 注意事项

1. **独立执行**: 此任务在日常会话之外运行，不干扰正常对话
2. **仅在有文件时提交**: 如果当日没有记忆日志，不会执行提交
3. **日志记录**: 所有执行记录保存到 `logs/daily-memory.log`
4. **错误处理**: 执行失败时会记录详细错误信息

---

*本定时任务配置文档作为 OpenClaw 记忆日志自动化指南*
