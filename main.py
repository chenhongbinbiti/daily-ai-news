#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日AI早报生成工具 - GitHub Actions 版本
每天早上8点生成AI领域新闻并推送到社交媒体
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional, List, Dict

import config
from rss_reader import RSSNewsReader

class DailyAINews:
    def __init__(self):
        self.rss_reader = RSSNewsReader()
    
    def fetch_daily_news(self) -> List[Dict]:
        """获取今日AI新闻"""
        print("🔍 从RSS源获取今日AI新闻...")
        news = self.rss_reader.fetch_all()
        print(f"📝 找到 {len(news)} 条最近24小时内的新闻")
        return news
    
    def format_for_ai(self, news: List[Dict]) -> str:
        """格式化供AI总结"""
        return self.rss_reader.format_for_summary(news)
    
    def get_ai_summary(self, news_text: str) -> str:
        """使用AI生成总结
        纯GitHub Actions版本，支持多种国产模型：
        火山引擎/DeepSeek/智谱GLM/OpenAI，都通过统一配置
        所有模型都兼容OpenAI API格式
        """
        prompt = self._build_prompt(news_text)
        
        if not config.AI_API_KEY:
            print("⚠️ 未配置AI_API_KEY，返回原始格式")
            return prompt
        
        # 调用AI API - 兼容OpenAI格式，支持所有国产模型
        try:
            from openai import OpenAI
            
            # 通用配置，支持所有兼容OpenAI格式的API
            client_kwargs = {"api_key": config.AI_API_KEY}
            if config.AI_BASE_URL:
                client_kwargs["base_url"] = config.AI_BASE_URL
            
            client = OpenAI(**client_kwargs)
            
            response = client.chat.completions.create(
                model=config.AI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个新闻编辑助手，请整理AI新闻成清晰简洁的每日早报。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.SUMMARY_MAX_LENGTH * 2,
                temperature=0.7
            )
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            print(f"❌ AI API调用失败: {e}")
            return prompt
    
    def _build_prompt(self, news_text: str) -> str:
        return f"""
请将以下今日AI领域新闻整理成一份清晰的每日早报。

要求：
1. 按重要性排序，最重要的放前面
2. 每条新闻保留核心信息：标题、关键要点、来源
3. 分类：可以分为「大模型/技术」、「产业/融资」、「政策/事件」等类别
4. 语言简洁，适合社交媒体推送
5. 如果新闻条数少于3条，如实列出即可，不要编造内容
6. 格式使用 Markdown

--- 新闻原文 ---
{news_text}

--- 请输出总结 ---
"""
    
    def format_output(self, summary: str) -> str:
        """最终格式化输出"""
        from datetime import datetime
        today = datetime.now().strftime("%Y年%m月%d日")
        header = f"🤖 **每日AI早报** ({today})\n\n"
        footer = "\n---\n由GitHub Actions + AI自动生成"
        return header + summary + footer
    
    def save_to_file(self, summary: str) -> str:
        """保存到历史文件"""
        if not config.SAVE_HISTORY:
            return ""
        
        os.makedirs(config.HISTORY_DIR, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{config.HISTORY_DIR}/{today}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"💾 保存到: {filename}")
        return filename
    
    def push_to_telegram(self, text: str) -> bool:
        """推送到Telegram"""
        if not (config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_CHAT_ID):
            print("⚠️ 未配置Telegram推送")
            return False
        
        import requests
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': config.TELEGRAM_CHAT_ID,
            'text': text,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=data)
        return response.ok
    
    def push_to_feishu(self, text: str) -> bool:
        """推送到飞书"""
        if not config.FEISHU_WEBHOOK_URL:
            print("⚠️ 未配置飞书webhook，请检查GitHub Secrets中的FEISHU_WEBHOOK_URL")
            return False
        
        import requests
        print(f"🚀 正在推送到飞书... webhook地址: {config.FEISHU_WEBHOOK_URL[:30]}...")
        data = {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        response = requests.post(config.FEISHU_WEBHOOK_URL, json=data)
        if response.ok:
            print("✅ 飞书推送成功！")
        else:
            print(f"❌ 飞书推送失败！状态码: {response.status_code}, 响应: {response.text}")
        return response.ok
    
    def push_to_github_issue(self, text: str) -> bool:
        """推送到GitHub Issue"""
        if not config.GITHUB_REPO or not os.getenv("GITHUB_TOKEN"):
            print("⚠️ 未配置GitHub Issue推送，需要GITHUB_REPO和GITHUB_TOKEN")
            return False
        
        import requests
        today = datetime.now().strftime("%Y年%m月%d日")
        title = f"🤖 每日AI早报 - {today}"
        
        headers = {
            "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "title": title,
            "body": text,
            "labels": ["daily-news", "ai"]
        }
        
        url = f"https://api.github.com/repos/{config.GITHUB_REPO}/issues"
        print(f"🚀 正在创建GitHub Issue... 仓库: {config.GITHUB_REPO}")
        response = requests.post(url, json=data, headers=headers)
        
        if response.ok:
            issue_url = response.json()["html_url"]
            print(f"✅ GitHub Issue 创建成功！{issue_url}")
            return True
        else:
            print(f"❌ GitHub Issue 创建失败！状态码: {response.status_code}, 响应: {response.text}")
            return False
    
    def push_to_email(self, text: str) -> bool:
        """使用SMTP推送邮件通知"""
        if not (config.SMTP_SERVER and config.SMTP_USERNAME and config.SMTP_PASSWORD and config.SMTP_FROM and config.SMTP_TO):
            print("⚠️ 未配置完整的邮件推送信息，请检查SMTP配置")
            return False
        
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header
        
        today = datetime.now().strftime("%Y年%m月%d日")
        subject = f"🤖 每日AI早报 - {today}"
        
        # 创建邮件
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = config.SMTP_FROM
        msg['To'] = config.SMTP_TO
        msg['Subject'] = Header(subject, 'utf-8')
        
        try:
            print(f"🚀 正在发送邮件通知... 收件人: {config.SMTP_TO}")
            # 连接SMTP服务器
            if config.SMTP_PORT == 465:
                # SSL连接
                server = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT)
            else:
                # STARTTLS
                server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
                server.starttls()
            
            # 登录
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            
            # 发送
            server.sendmail(config.SMTP_FROM, config.SMTP_TO.split(','), msg.as_string())
            server.quit()
            
            print("✅ 邮件发送成功！")
            return True
        except Exception as e:
            print(f"❌ 邮件发送失败！错误: {str(e)}")
            return False
    
    def run(self) -> str:
        """运行完整流程"""
        # 1. 获取新闻
        news = self.fetch_daily_news()
        
        if not news:
            summary = "今天没有找到AI领域新发布的重要新闻。"
        else:
            # 2. 格式化
            formatted = self.format_for_ai(news)
            
            # 3. AI总结
            summary = self.get_ai_summary(formatted)
            
            # 如果配置了API，这里实际会得到AI总结
            # 否则直接用原格式
            if config.AI_API_KEY:
                # 已经在 get_ai_summary 中处理了
                pass
        
        # 4. 最终格式化
        final_output = self.format_output(summary)
        
        # 5. 保存历史
        if config.SAVE_HISTORY:
            self.save_to_file(final_output)
        
        # 6. 推送
        print(f"📢 当前推送方式: {config.PUSH_METHOD}")
        if config.PUSH_METHOD == 'telegram':
            self.push_to_telegram(final_output)
        elif config.PUSH_METHOD == 'feishu':
            self.push_to_feishu(final_output)
        elif config.PUSH_METHOD == 'github_issue':
            self.push_to_github_issue(final_output)
        elif config.PUSH_METHOD == 'email':
            self.push_to_email(final_output)
        else:
            print(f"⚠️ 未知的推送方式: {config.PUSH_METHOD}，未执行推送")
        
        print("\n=== 生成完成 ===")
        print(final_output)
        
        return final_output

if __name__ == "__main__":
    generator = DailyAINews()
    result = generator.run()
    sys.exit(0)
