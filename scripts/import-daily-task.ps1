# OpenClaw 每日记忆日志定时任务 - 导入脚本
# 用途：将定时任务导入到 Windows 任务计划程序
# 执行：以管理员身份运行此脚本

$taskName = "OpenClaw 每日记忆日志"
$taskXmlPath = "D:\Users\yr.ju.CN1\.openclaw\workspace\OpenClaw 每日记忆日志.xml"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📅 OpenClaw 每日记忆日志定时任务导入" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 XML 文件是否存在
if (-not (Test-Path $taskXmlPath)) {
    Write-Host "❌ 错误：XML 文件不存在：$taskXmlPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ XML 文件存在：$taskXmlPath" -ForegroundColor Green

# 检查任务是否已存在
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "⚠️  任务已存在，正在删除..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "✅ 已删除旧任务" -ForegroundColor Green
}

# 导入任务
Write-Host "📝 正在导入任务..." -ForegroundColor Yellow
try {
    $taskXml = [Xml.XmlDocument]::new()
    $taskXml.Load($taskXmlPath)
    
    $taskPath = "\OpenClaw 每日记忆日志"
    Register-ScheduledTask -Xml $taskXml.OuterXml -TaskName $taskName -TaskPath $taskPath -Force
    
    Write-Host "✅ 任务导入成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "任务详情:" -ForegroundColor Cyan
    Write-Host "  名称：$taskName" -ForegroundColor White
    Write-Host "  路径：$taskPath" -ForegroundColor White
    Write-Host "  触发器：每天凌晨 1:00" -ForegroundColor White
    Write-Host ""
    
    # 显示任务信息
    $task = Get-ScheduledTask -TaskName $taskName
    Write-Host "任务状态：$($task.State)" -ForegroundColor Cyan
    Write-Host "下次运行时间：$($task.TaskInfo.NextRunTime)" -ForegroundColor Cyan
    
} catch {
    Write-Host "❌ 导入失败：$($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ 定时任务配置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "验证命令:" -ForegroundColor Yellow
Write-Host "  Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host ""
Write-Host "手动测试:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
Write-Host ""
Write-Host "查看日志:" -ForegroundColor Yellow
Write-Host "  Get-Content 'D:\Users\yr.ju.CN1\.openclaw\workspace\logs\daily-memory.log' -Tail 20" -ForegroundColor Gray
Write-Host ""
