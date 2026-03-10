# ⚠️ 需要手动导入定时任务

**原因**: 导入 Windows 任务计划需要管理员权限

---

## 🔧 手动导入步骤

### 方法 1: 使用 PowerShell 脚本 (推荐)

**步骤**:

1. **右键点击 PowerShell** → 选择 **"以管理员身份运行"**

2. **复制并执行以下命令**:

```powershell
& "D:\Users\yr.ju.CN1\.openclaw\workspace\scripts\import-daily-task.ps1"
```

3. **等待导入完成**，看到以下输出表示成功：

```
========================================
📅 OpenClaw 每日记忆日志定时任务导入
========================================

✅ XML 文件存在：D:\Users\yr.ju.CN1\.openclaw\workspace\OpenClaw 每日记忆日志.xml
✅ 已删除旧任务
📝 正在导入任务...
✅ 任务导入成功！

任务详情:
  名称：OpenClaw 每日记忆日志
  路径：\OpenClaw 每日记忆日志
  触发器：每天凌晨 1:00

任务状态：Ready
下次运行时间：2026-03-11T01:00:00

========================================
✅ 定时任务配置完成！
========================================
```

---

### 方法 2: 使用任务计划程序 GUI

**步骤**:

1. **打开任务计划程序**:
   - 按 `Win + R`
   - 输入 `taskschd.msc`
   - 按回车

2. **导入任务**:
   - 点击右侧 **"操作"** 面板
   - 选择 **"导入任务..."**
   - 浏览并选择文件：
     ```
     D:\Users\yr.ju.CN1\.openclaw\workspace\OpenClaw 每日记忆日志.xml
     ```
   - 点击 **"打开"**

3. **确认设置**:
   - 名称：`OpenClaw 每日记忆日志`
   - 触发器：`每天凌晨 1:00`
   - 操作：`启动程序 (node.exe)`
   - 勾选 **"不管用户是否登录都要运行"**
   - 勾选 **"使用最高权限运行"**
   - 点击 **"确定"**

4. **输入管理员密码** (如果需要)

---

## ✅ 验证导入

**导入后执行以下命令验证**:

```powershell
# 查看任务状态
Get-ScheduledTask -TaskName "OpenClaw 每日记忆日志"

# 查看任务详情
Get-ScheduledTask -TaskName "OpenClaw 每日记忆日志" | Select-Object TaskName,State,NextRunTime

# 手动测试运行
Start-ScheduledTask -TaskName "OpenClaw 每日记忆日志"

# 等待 10 秒后查看日志
Start-Sleep -Seconds 10
Get-Content "D:\Users\yr.ju.CN1\.openclaw\workspace\logs\daily-memory.log" -Tail 20
```

---

## 📊 预期输出

**成功导入后**:

```
TaskName    State NextRunTime
--------    ----- -----------
OpenClaw 每... Ready 2026-03-11T01:00:00
```

**日志文件位置**:
```
D:\Users\yr.ju.CN1\.openclaw\workspace\logs\daily-memory.log
```

---

## 🚨 常见问题

### 问题 1: "拒绝访问"

**解决**: 确保以管理员身份运行 PowerShell

### 问题 2: "找不到文件"

**解决**: 检查路径是否正确，使用完整路径

### 问题 3: 任务已存在

**解决**: 脚本会自动删除旧任务，或手动删除：
```powershell
Unregister-ScheduledTask -TaskName "OpenClaw 每日记忆日志" -Confirm:$false
```

---

## 📝 导入后确认

导入完成后，请告诉我，我会帮您验证任务状态！

**确认内容**:
- [ ] 任务已成功导入
- [ ] 任务状态为 `Ready`
- [ ] 下次运行时间为 `2026-03-11T01:00:00` (或下一个凌晨 1:00)

---

*导入完成后，每日凌晨 1:00 会自动执行记忆日志的汇总和上传！*
