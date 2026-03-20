# 🤖 每日AI早报

自动聚合AI领域新闻，每天定时生成简报推送到社交媒体。**纯 GitHub Actions 托管版本**，支持多种国产大模型。

## ✨ 功能特性

- 🔄 **自动聚合** - 从多个AI资讯源RSS获取过去24小时新闻
- 🧠 **支持多模型** - 火山引擎/DeepSeek/智谱GLM/OpenAI 可任选其一配置
- ⏰ **定时运行** - GitHub Actions 每天早上8点自动执行（免费额度够用）
- 📤 **多渠道推送** - 支持 Telegram / 飞书 / GitHub Issue
- 💾 **保存历史** - 历史简报保存到仓库

## 🚀 部署

### 1. Fork / 克隆这个仓库

```bash
git clone https://github.com/你的用户名/daily-ai-news.git
cd daily-ai-news
```

### 2. 配置 Secrets 和 Variables

在你的 GitHub 仓库 → Settings → **Secrets and variables** → Actions:

**Secrets (加密密钥):**

| Secret | 说明 | 是否必填 |
|--------|------|----------|
| `AI_API_KEY` | 你的AI模型API密钥 | ✅ 必填 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 推送Telegram需要 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 推送Telegram需要 |
| `FEISHU_WEBHOOK_URL` | 飞书机器人Webhook | 推送飞书需要 |

**Variables (公开变量):**

| Variable | 示例 | 说明 |
|----------|------|------|
| `AI_MODEL` | `doubao-4k-chat` | 模型名称 |
| `AI_BASE_URL` | `https://aquasearch.volcengineapi.com/` | API Base URL |
| `PUSH_METHOD` | `telegram` | 推送方式: `github_issue` / `telegram` / `feishu` / `none` |

### 3. 选择你的模型配置

#### 🔹 **火山引擎 (字节跳动)**
```
AI_API_KEY: 你的密钥 (Secrets)
AI_MODEL: doubao-4k-chat (Variables)
AI_BASE_URL: https://aquasearch.volcengineapi.com/ (Variables)
```

#### 🔹 **DeepSeek**
```
AI_API_KEY: 你的密钥 (Secrets)
AI_MODEL: deepseek-chat (Variables)
AI_BASE_URL: https://api.deepseek.com/v1 (Variables)
```

#### 🔹 **智谱 GLM**
```
AI_API_KEY: 你的密钥 (Secrets)
AI_MODEL: glm-4 (Variables)
AI_BASE_URL: https://open.bigmodel.cn/api/paas/v4 (Variables)
```

#### 🔹 **OpenAI**
```
AI_API_KEY: 你的密钥 (Secrets)
AI_MODEL: gpt-3.5-turbo (Variables)
AI_BASE_URL: https://api.openai.com/v1 (Variables)
```

### 4. 修改RSS新闻源（可选）

编辑 `config.py` 中的 `AI_NEWS_RSS` 添加你喜欢的源：

```python
AI_NEWS_RSS = [
    "https://ai.googleblog.com/atom.xml",
    "https://openai.com/blog/rss.xml",
    "https://www.kdnuggets.com/feed",
    # ... 添加你自己的源
]
```

### 5. 启用 Actions

在你的仓库 → Actions → 点击 `I understand my workflows, go ahead and enable them`

### 6. 手动触发测试

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

# 配置环境变量
export AI_API_KEY=your-key
export AI_MODEL=doubao-4k-chat
export AI_BASE_URL=https://aquasearch.volcengineapi.com/

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

- GitHub Actions 免费额度完全够用（每月2000分钟，每天一次只用1分钟左右）
- AI API 费用由你使用的模型厂商收取，每天一次调用成本很低

## 📄 许可

MIT
