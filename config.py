# -*- coding: utf-8 -*-
"""配置文件 - GitHub Actions 版本，支持多模型可配置"""

import os
from typing import Optional

# 定时设置 (GitHub Actions cron 配置在 .github/workflows/daily.yml)
DAILY_TIME = "08:00"  # 每天推送时间 (UTC+8)
TIMEZONE = "Asia/Shanghai"

# 搜索配置
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "artificial intelligence AI news today latest updates")
MAX_RESULTS = int(os.getenv("MAX_RESULTS", "15"))

# AI 总结配置 - 支持多种国产模型
# 所有模型都通过环境变量配置，不用改代码
# 通用配置
AI_API_KEY: Optional[str] = os.getenv("AI_API_KEY")  # 统一API密钥变量
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")  # 模型名称
AI_BASE_URL: Optional[str] = os.getenv("AI_BASE_URL")  # API base URL

# 各厂商配置说明：
#
# 1. 火山引擎 (字节跳动) - 兼容OpenAI格式
# AI_API_KEY=your-volcengine-key
# AI_BASE_URL=https://aquasearch.volcengineapi.com.cn/
# AI_MODEL=doubao-4k-chat
#
# 2. DeepSeek
# AI_API_KEY=your-deepseek-key
# AI_BASE_URL=https://api.deepseek.com/v1
# AI_MODEL=deepseek-chat
#
# 3. 智谱 GLM
# AI_API_KEY=your-zhipu-key
# AI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
# AI_MODEL=glm-4
#
# 4. OpenAI (原始)
# AI_API_KEY=your-openai-key
# AI_BASE_URL=https://api.openai.com/v1
# AI_MODEL=gpt-3.5-turbo

SUMMARY_MIN_LENGTH = int(os.getenv("SUMMARY_MIN_LENGTH", "300"))
SUMMARY_MAX_LENGTH = int(os.getenv("SUMMARY_MAX_LENGTH", "800"))

# 推送配置
PUSH_METHOD = os.getenv("PUSH_METHOD") or "github_issue"  # github_issue / telegram / feishu / none，如果环境变量为空则使用默认值

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
