#!/usr/bin/env node

/**
 * OpenClaw 每日记忆日志自动提交脚本
 * 执行时间：每日凌晨 1:00
 * 用途：自动汇总当日记忆并上传到 GitHub
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = 'D:\\Users\\yr.ju.CN1\\.openclaw\\workspace';
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const LOG_FILE = path.join(WORKSPACE, 'logs', 'daily-memory.log');

// 日志函数
function log(message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] ${message}\n`;
    console.log(logMessage);
    
    // 确保日志目录存在
    const logDir = path.dirname(LOG_FILE);
    if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
    }
    
    fs.appendFileSync(LOG_FILE, logMessage);
}

// 获取今日日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
const memoryFile = path.join(MEMORY_DIR, `${dateStr}.md`);

log('========================================');
log('📅 OpenClaw 每日记忆日志自动提交任务');
log(`📝 日期：${dateStr}`);
log('========================================');

// 检查文件是否存在
if (!fs.existsSync(memoryFile)) {
    log(`ℹ️  今日记忆文件不存在：${memoryFile}`);
    log('✅ 任务完成 (无新记忆文件)');
    process.exit(0);
}

log(`✅ 找到记忆文件：${memoryFile}`);

try {
    // 切换到 workspace 目录
    process.chdir(WORKSPACE);
    log(`📂 工作目录：${WORKSPACE}`);
    
    // 设置 PATH (包含 GitHub CLI)
    const env = { ...process.env };
    try {
        const machinePath = execSync('powershell -Command "[System.Environment]::GetEnvironmentVariable(\'Path\',\'Machine\')"').toString().trim();
        const userPath = execSync('powershell -Command "[System.Environment]::GetEnvironmentVariable(\'Path\',\'User\')"').toString().trim();
        env.PATH = machinePath + ';' + userPath + ';' + env.PATH;
        log('✅ PATH 环境变量已配置');
    } catch (e) {
        log('⚠️  无法获取系统 PATH，使用当前环境变量');
    }
    
    // 检查 Git 状态
    try {
        execSync('git status', { env, stdio: 'pipe' });
        log('✅ Git 仓库可用');
    } catch (e) {
        throw new Error('Git 仓库不可用，请检查是否在正确的目录');
    }
    
    // Git 添加
    log('📝 执行：git add memory/' + dateStr + '.md');
    try {
        const addResult = execSync(`git add memory/${dateStr}.md`, { env, encoding: 'utf8' });
        if (addResult) log(addResult.trim());
        log('✅ Git add 完成');
    } catch (e) {
        log('⚠️  Git add 执行异常：' + e.message);
    }
    
    // 检查是否有变化需要提交
    log('📝 检查 Git 状态...');
    const statusResult = execSync('git status --porcelain', { env, encoding: 'utf8' });
    if (!statusResult.trim()) {
        log('ℹ️  没有新的变化需要提交 (文件可能已在之前提交)');
        log('✅ 任务完成 (无新变化)');
        process.exit(0);
    }
    
    log('📝 检测到变化：' + statusResult.trim().split('\n').length + ' 个文件');
    
    // Git 提交
    const commitMsg = `docs(memory): 每日记忆日志自动提交 - ${dateStr}`;
    log(`📝 执行：git commit -m "${commitMsg}"`);
    try {
        const commitResult = execSync(`git commit -m "${commitMsg}"`, { env, encoding: 'utf8' });
        log('✅ Git commit 成功');
    } catch (e) {
        throw new Error(`Git commit 失败：${e.message}`);
    }
    
    // Git 推送
    log('📝 执行：git push origin master');
    try {
        const pushResult = execSync('git push origin master', { env, encoding: 'utf8' });
        log('✅ Git push 成功');
    } catch (e) {
        throw new Error(`Git push 失败：${e.message}`);
    }
    
    log('========================================');
    log('✅ 记忆日志上传成功！');
    log('========================================');
    
} catch (error) {
    log(`❌ 执行失败：${error.message}`);
    if (error.stdout) log(`stdout: ${error.stdout}`);
    if (error.stderr) log(`stderr: ${error.stderr}`);
    log('========================================');
    log('❌ 任务失败，请检查日志');
    log('========================================');
    process.exit(1);
}
