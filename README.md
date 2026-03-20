# 🤖 每日AI早报

自动聚合AI领域新闻，每天定时生成简报推送到社交媒体。**纯 GitHub Actions 托管版本**，完全免费运行在GitHub。

## ✨ 功能特性

- 🔄 **自动聚合** - 从多个AI资讯源RSS获取过去24小时新闻
- 🧠 **AI总结** - 使用OpenAI整理成清晰简报（需要你配置API Key）
- ⏰ **定时运行** - GitHub Actions 每天早上8点自动执行
- 📤 **多渠道推送** - 支持 Telegram / 飞书 / GitHub Issue
- 💾 **保存历史** - 历史简报保存到仓库

## 🚀 部署使用

### 1. Fork 这个仓库

```bash
# 或者克隆到本地
git clone https://github.com/你的用户名/daily-ai-news.git
cd daily-ai-news
```

### 2. 配置 Secrets

在你的 GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret:

| Secret | 说明 | 是否必填 |
|--------|------|----------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | 是（用于AI总结） |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 推送Telegram需要 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 推送Telegram需要 |
| `FEISHU_WEBHOOK_URL` | 飞书机器人Webhook | 推送飞书需要 |

### 3. 修改配置（可选）

编辑 `config.py` 自定义：

```python
# 修改推送方式
PUSH_METHOD = "telegram"  # github_issue / telegram / feishu / none

# 添加/修改RSS源
AI_NEWS_RSS = [
    "https://ai.googleblog.com/atom.xml",
    "https://openai.com/blog/rss.xml",
    # ... 添加你自己的源
]
```

### 4. 启用 Actions

在你的仓库 → Actions → 点击 `I understand my workflows, go ahead and enable them`

### 5. 手动触发测试

Actions → `Daily AI News` → `Run workflow` → 手动运行测试

## 📅 定时

默认每天 **北京时间 8:00** 运行。修改 `.github/workflows/daily.yml` 的 cron 表达式改变时间。

```yaml
# 北京时间 8:00 = UTC 0:00
on:
  schedule:
    - cron: '0 0 * * *'
```

## 🔧 本地测试

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python main.py
```

## 📝 默认RSS源

- Google AI Blog
- OpenAI Blog
- KDnuggets
- Towards Data Science
- IEEE Spectrum - AI

添加你自己喜欢的源！

## 💰 费用说明

- GitHub Actions 免费额度完全够用（每月2000分钟）
- OpenAI API 按调用量付费，每天一次调用费用大概几分钱
- 总体几乎零成本

## 📄 许可

MIT
