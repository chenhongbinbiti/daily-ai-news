# -*- coding: utf-8 -*-
"""配置文件 - GitHub Actions 版本"""

import os
from typing import Optional

# 定时设置 (GitHub Actions cron 配置在 .github/workflows/daily.yml)
DAILY_TIME = "08:00"  # 每天推送时间 (UTC+8)
TIMEZONE = "Asia/Shanghai"

# 搜索配置
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "artificial intelligence AI news today latest updates")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", "15"))

# AI 总结配置
# 在ArkClaw环境中使用内置免费模型，不需要付费API
# 如果配置了OPENAI_API_KEY则优先使用OpenAI
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
SUMMARY_MIN_LENGTH = int(os.getenv("SUMMARY_MIN_LENGTH", "300"))
SUMMARY_MAX_LENGTH = int(os.getenv("SUMMARY_MAX_LENGTH", "800"))

# 推送配置
PUSH_METHOD = os.getenv("PUSH_METHOD", "github_issue")  # github_issue / telegram / feishu / none

# Telegram 推送
TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")

# 飞书推送
FEISHU_WEBHOOK_URL: Optional[str] = os.getenv("FEISHU_WEBHOOK_URL")

# GitHub Issue 推送 (默认推送到当前仓库的 Issue)
GITHUB_REPO = os.getenv("GITHUB_REPO", "")  # owner/repo

# RSS 新闻源 - AI领域常用资讯源
AI_NEWS_RSS = [
    "https://ai.googleblog.com/atom.xml",
    "https://openai.com/blog/rss.xml",
    "https://www.kdnuggets.com/feed",
    "https://towardsdatascience.com/feed",
    "https://spectrum.ieee.org/section/artificial-intelligence/feed",
]

# 是否保存历史到本地
SAVE_HISTORY = True
HISTORY_DIR = "news"
