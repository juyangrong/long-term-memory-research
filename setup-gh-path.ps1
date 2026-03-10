# GitHub CLI 环境变量配置脚本
# 用途：将 GitHub CLI 添加到 PATH 环境变量

# 获取 GitHub CLI 路径
$ghPath = "C:\Program Files\GitHub CLI"

# 获取当前系统 PATH
$machinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")

# 检查是否已存在
if ($machinePath -notlike "*$ghPath*") {
    # 添加到系统 PATH
    [System.Environment]::SetEnvironmentVariable("Path", "$machinePath;$ghPath", "Machine")
    Write-Host "✓ 已将 GitHub CLI 添加到系统 PATH" -ForegroundColor Green
    Write-Host "⚠ 请重启 PowerShell 使更改生效" -ForegroundColor Yellow
} else {
    Write-Host "✓ GitHub CLI 已在 PATH 中" -ForegroundColor Green
}

# 为当前会话添加 PATH
$env:Path = $machinePath + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
Write-Host "✓ 当前会话已配置 GitHub CLI" -ForegroundColor Green
