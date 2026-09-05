@echo off
chcp 65001 >nul
title 一键推送桌宠到 GitHub
cd /d "%~dp0"

echo ========================================
echo   一键推送桌宠到 GitHub（触发云端打包）
echo ========================================
echo.

REM ---- 1. 仓库地址：改成你自己的 ----
set "REPO=https://github.com/你的用户名/桌宠.git"
REM 示例: https://github.com/zhangsan/zhuochong.git
REM       或 SSH:  git@github.com:zhangsan/zhuochong.git

if "%REPO%"=="https://github.com/你的用户名/桌宠.git" (
    echo [提示] 请先用记事本打开本文件，把顶部 REPO= 改成你的仓库地址。
    echo 还没建仓库？先在 GitHub 网页点 New repository 建一个空仓库，再回来改。
    echo.
    pause
    exit /b 1
)

echo [1/4] 检查是否已初始化 git 仓库...
if not exist ".git" (
    echo   初始化...
    git init -b main
)

echo [2/4] 配置提交者信息（可改成你自己的名字/邮箱）...
git config user.name "pet-dev"
git config user.email "pet-dev@local"

echo [3/4] 提交代码...
git add -A
git commit -m "桌宠 v1.0"

echo [4/4] 推送并设置远程仓库...
git remote remove origin 2>nul
git remote add origin "%REPO%"
git push -u origin main

if errorlevel 1 (
    echo.
    echo [错误] 推送失败。常见原因：
    echo   - 仓库地址填错了
    echo   - 没登录 GitHub（会弹出窗口，按提示登录授权）
    echo   - 仓库里已有内容（把 GitHub 上建的空仓库，不要勾选任何初始化选项）
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 推送成功！
echo   现在去 GitHub 仓库页面 -> Actions 标签，
echo   云端会自动打包，完成后在 Artifacts 下载桌宠.app
echo ========================================
pause
