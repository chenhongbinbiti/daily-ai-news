# -*- coding: utf-8 -*-
"""RSS新闻阅读器 - 从多个AI资讯源聚合新闻"""

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import time
import requests
from urllib.parse import quote

import config

class RSSNewsReader:
    def __init__(self, rss_urls: List[str] = None):
        self.rss_urls = rss_urls or config.AI_NEWS_RSS
    
    def is_recent(self, published_time: float, hours: int = 24) -> bool:
        """判断是否是最近24小时内的新闻"""
        now = time.time()
        return (now - published_time) < (hours * 3600)
    
    def _get_rss_url(self, original_url: str) -> str:
        """获取最终的RSS URL，支持RSSHub反代"""
        if config.RSSHUB_BASE_URL:
            # 使用RSSHub反代: https://rsshub.app/url?url=original_url
            rsshub_base = config.RSSHUB_BASE_URL.rstrip('/')
            return f"{rsshub_base}/{quote(original_url)}"
        return original_url
    
    def fetch_all(self) -> List[Dict]:
        """从所有RSS源获取最近24小时的新闻"""
        all_news = []
        self.stats = []  # 保存每个源的统计信息
        
        total_sources = len(self.rss_urls)
        success_count = 0
        
        print(f"🔍 开始从 {total_sources} 个RSS源获取新闻...")
        if config.RSSHUB_BASE_URL:
            print(f"🌐 使用RSSHub反代: {config.RSSHUB_BASE_URL[:50]}...")
        
        for url in self.rss_urls:
            try:
                news = self._fetch_from_url(url)
                # 获取源名称 - 顺序很重要，从具体到通用
                if "googleblog" in url:
                    name = "Google AI Blog"
                elif "openai.com" in url:
                    name = "OpenAI Blog"
                elif "towardsdatascience" in url:
                    name = "Towards Data Science"
                elif "spectrum.ieee" in url:
                    name = "IEEE Spectrum"
                elif "kdnuggets" in url.lower():
                    name = "KDnuggets"
                elif "ruanyifeng" in url:
                    name = "阮一峰-科技爱好者周刊"
                elif "qbitai" in url:
                    name = "量子位-AI资讯"
                elif "jiqizhixin" in url:
                    name = "机器之心"
                elif "sspai" in url:
                    name = "少数派"
                elif "36kr" in url:
                    name = "36氪-AI专栏"
                elif "zhihu" in url:
                    name = "知乎"
                else:
                    name = url.split('/')[2]
                
                self.stats.append({
                    "url": url,
                    "name": name,
                    "success": len(news) > 0,
                    "recent_count": len(news),
                    "error": None
                })
                
                if news:
                    success_count += 1
                    all_news.extend(news)
            except Exception as e:
                error_msg = str(e)[:100]
                self.stats.append({
                    "url": url,
                    "name": name if 'name' in locals() else url.split('/')[2],
                    "success": False,
                    "recent_count": 0,
                    "error": error_msg
                })
                print(f"⚠️  获取失败跳过: {url[:60]}... 错误: {error_msg}")
                continue
        
        print(f"✅ 完成: {success_count}/{total_sources} 个RSS源成功获取，共找到 {len(all_news)} 条新闻")
        
        # 按时间倒序排序
        all_news.sort(key=lambda x: x.get('published_ts', 0), reverse=True)
        return all_news
    
    def _fetch_from_url(self, original_url: str) -> List[Dict]:
        """从单个URL获取最近24小时新闻"""
        url = self._get_rss_url(original_url)
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        
        recent_news = []
        for entry in feed.entries:
            # 获取发布时间
            if hasattr(entry, 'published_parsed'):
                published_ts = time.mktime(entry.published_parsed)
            elif hasattr(entry, 'updated_parsed'):
                published_ts = time.mktime(entry.updated_parsed)
            else:
                # 如果没有时间，默认为最近新闻
                published_ts = time.time()
            
            if self.is_recent(published_ts):
                source_name = feed.feed.title if (hasattr(feed, 'feed') and hasattr(feed.feed, 'title')) else original_url
                recent_news.append({
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.get('summary', entry.get('description', '')),
                    'published': entry.get('published', entry.get('updated', '')),
                    'published_ts': published_ts,
                    'source': source_name
                })
        
        return recent_news
    
    def format_for_summary(self, news_list: List[Dict]) -> str:
        """格式化为AI总结文本"""
        if not news_list:
            return "没有找到今日AI新闻。"
        
        text = f"今日AI新闻汇总 ({len(news_list)} 条，来自{len(self.rss_urls)}个资讯源):\n\n"
        
        for i, item in enumerate(news_list[:config.MAX_RESULTS], 1):
            text += f"--- {i} ---\n"
            text += f"标题: {item['title']}\n"
            text += f"来源: {item['source']}\n"
            text += f"发布时间: {item['published']}\n"
            text += f"链接: {item['link']}\n"
            if item['summary']:
                # 截断太长的摘要
                summary = item['summary'][:300]
                text += f"摘要: {summary}...\n"
            text += "\n"
        
        return text
