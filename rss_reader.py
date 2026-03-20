# -*- coding: utf-8 -*-
"""RSS新闻阅读器 - 从多个AI资讯源聚合新闻"""

import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import time
import requests

import config

class RSSNewsReader:
    def __init__(self, rss_urls: List[str] = None):
        self.rss_urls = rss_urls or config.AI_NEWS_RSS
    
    def is_recent(self, published_time: float, hours: int = 24) -> bool:
        """判断是否是最近24小时内的新闻"""
        now = time.time()
        return (now - published_time) < (hours * 3600)
    
    def fetch_all(self) -> List[Dict]:
        """从所有RSS源获取最近24小时的新闻"""
        all_news = []
        
        for url in self.rss_urls:
            try:
                news = self._fetch_from_url(url)
                all_news.extend(news)
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")
                continue
        
        # 按时间倒序排序
        all_news.sort(key=lambda x: x.get('published_parsed', 0), reverse=True)
        return all_news
    
    def _fetch_from_url(self, url: str) -> List[Dict]:
        """从单个URL获取最近24小时新闻"""
        response = requests.get(url, timeout=10)
        feed = feedparser.parse(response.content)
        
        recent_news = []
        for entry in feed.entries:
            # 获取发布时间
            if hasattr(entry, 'published_parsed'):
                published_ts = time.mktime(entry.published_parsed)
                if self.is_recent(published_ts):
                    recent_news.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.get('summary', entry.get('description', '')),
                        'published': entry.get('published', ''),
                        'published_ts': published_ts,
                        'source': feed.feed.title if hasattr(feed, 'feed') and hasattr(feed.feed, 'title') else url
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
