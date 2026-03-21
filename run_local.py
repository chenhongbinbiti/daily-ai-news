#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日AI早报 - 本地运行版本
在 OpenClaw 本地运行，生成早报后推送到 GitHub 指定分支
"""

import os
import sys
import subprocess
from datetime import datetime

def run_git_command(cmd, cwd=None):
    """运行 git 命令"""
    print(f"📝 执行: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Git 命令失败: {result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True

def main():
    # 获取项目目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("🤖 每日AI早报 - 本地运行")
    print(f"⏰ 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 1. 运行主程序生成早报
    print("\n🔄 生成每日AI早报...")
    result = subprocess.run([sys.executable, "main.py"], capture_output=False)
    if result.returncode != 0:
        print("❌ 生成早报失败！")
        sys.exit(1)
    
    # 2. 检查并切换到目标分支
    target_branch = os.getenv("TARGET_BRANCH", "daily-news")
    print(f"\n🚀 准备推送到 GitHub 分支: {target_branch}")
    
    # 检查分支是否存在
    check_branch = subprocess.run(f"git branch --list {target_branch}", shell=True, capture_output=True, text=True)
    if check_branch.stdout.strip():
        # 分支已存在，切换过去
        if not run_git_command(f"git checkout {target_branch}"):
            print(f"❌ 切换到分支 {target_branch} 失败")
            sys.exit(1)
    else:
        # 创建新分支
        if not run_git_command(f"git checkout -b {target_branch}"):
            print(f"❌ 创建分支 {target_branch} 失败")
            sys.exit(1)
    
    # 3. 合并 main 分支的更新（可选）
    if not run_git_command("git checkout main -- news/"):
        print("⚠️  更新 news 目录失败，继续...")
    
    # 4. 添加并提交
    print("\n📦 提交更新...")
    if not run_git_command("git add news/"):
        print("❌ 添加文件失败")
        sys.exit(1)
    
    # 检查是否有更改需要提交
    status = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not status.stdout.strip():
        print("✅ 没有新的更改需要提交")
        print("\n🎉 运行完成！")
        sys.exit(0)
    
    today = datetime.now().strftime("%Y-%m-%d")
    commit_message = f"Update daily AI news - {today}"
    if not run_git_command(f'git commit -m "{commit_message}"'):
        print("❌ 提交失败")
        sys.exit(1)
    
    # 5. 推送到远程
    print(f"\n⬆️  推送到远程分支 {target_branch}...")
    remote = os.getenv("GIT_REMOTE", "origin")
    if not run_git_command(f"git push {remote} {target_branch}"):
        print("❌ 推送失败")
        sys.exit(1)
    
    print("\n🎉 运行完成！每日AI早报已成功推送到 GitHub。")
    print(f"📁 分支: {target_branch}")
    print(f"📅 日期: {today}")

if __name__ == "__main__":
    main()
