#!/usr/bin/env python3
"""
Blogger to eBook Converter (Web Scraping Version)
Fetches posts from a Blogger blog via web scraping and compiles them into an ebook
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pathlib import Path
import re
from typing import List, Dict
import html
import time

class BloggerToEbook:
    def __init__(self, blog_url: str):
        """
        Initialize the converter
        
        Args:
            blog_url: Your Blogger blog URL (e.g., 'https://myblog.blogspot.com')
        """
        self.blog_url = blog_url.rstrip('/')
        self.posts = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_feed_url(self) -> str:
        """Get the Blogger JSON feed URL"""
        return f"{self.blog_url}/feeds/posts/default?alt=json&max-results=999"
    
    def fetch_posts_via_feed(self) -> List[Dict]:
        """Fetch all posts using Blogger's JSON feed"""
        feed_url = self.get_feed_url()
        print(f"Fetching posts from feed: {feed_url}")
        
        try:
            response = self.session.get(feed_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'feed' not in data or 'entry' not in data['feed']:
                print("No posts found in feed")
                return []
            
            entries = data['feed']['entry']
            print(f"Found {len(entries)} posts")
            
            posts = []
            for entry in entries:
                post = self.parse_feed_entry(entry)
                if post:
                    posts.append(post)
            
            self.posts = posts
            return posts
            
        except Exception as e:
            print(f"Error fetching feed: {e}")
            print("Trying alternative method...")
            return self.fetch_posts_via_scraping()
    
    def parse_feed_entry(self, entry: Dict) -> Dict:
        """Parse a single feed entry into a post dict"""
        try:
            # Extract title
            title = entry.get('title', {}).get('$t', 'Untitled')
            
            # Extract content
            content = entry.get('content', {}).get('$t', '')
            if not content:
                content = entry.get('summary', {}).get('$t', '')
            
            # Extract published date
            published = entry.get('published', {}).get('$t', '')
            
            # Extract URL
            url = ''
            for link in entry.get('link', []):
                if link.get('rel') == 'alternate':
                    url = link.get('href', '')
                    break
            
            return {
                'title': title,
                'content': content,
                'published': published,
                'url': url
            }
        except Exception as e:
            print(f"Error parsing entry: {e}")
            return None
    
    def fetch_posts_via_scraping(self) -> List[Dict]:
        """Alternative method: scrape the blog directly"""
        print("Using web scraping method...")
        posts = []
        
        # Try to get posts from archive page
        archive_url = f"{self.blog_url}/search?max-results=999"
        
        try:
            response = self.session.get(archive_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all post articles
            articles = soup.find_all(['article', 'div'], class_=lambda x: x and 'post' in x.lower())
            
            if not articles:
                # Try alternative selector
                articles = soup.find_all('div', class_='blog-post')
            
            print(f"Found {len(articles)} posts via scraping")
            
            for article in articles:
                post = self.parse_article(article)
                if post:
                    posts.append(post)
            
            self.posts = posts
            return posts
            
        except Exception as e:
            print(f"Error scraping blog: {e}")
            return []
    
    def parse_article(self, article) -> Dict:
        """Parse an article element into a post dict"""
        try:
            # Find title
            title_elem = article.find(['h1', 'h2', 'h3'], class_=lambda x: x and 'title' in x.lower())
            if not title_elem:
                title_elem = article.find(['h1', 'h2', 'h3'])
            title = title_elem.get_text(strip=True) if title_elem else 'Untitled'
            
            # Find content
            content_elem = article.find(['div', 'section'], class_=lambda x: x and ('content' in str(x).lower() or 'body' in str(x).lower()))
            if not content_elem:
                content_elem = article.find('div', class_='post-body')
            if not content_elem:
                content_elem = article
            
            content = str(content_elem) if content_elem else ''
            
            # Find date
            date_elem = article.find(['time', 'abbr', 'span'], class_=lambda x: x and 'date' in str(x).lower())
            if date_elem:
                published = date_elem.get('datetime', '') or date_elem.get_text(strip=True)
            else:
                published = ''
            
            # Find URL
            link_elem = article.find('a', href=True)
            url = link_elem['href'] if link_elem else ''
            
            return {
                'title': title,
                'content': content,
                'published': published,
                'url': url
            }
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None
    
    def clean_html(self, html_content: str) -> str:
        """Clean HTML content for better readability"""
        # Unescape HTML entities
        content = html.unescape(html_content)
        
        # Remove script and style tags
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
        
        return content
    
    def save_to_html(self, output_file: str = "blog_ebook.html"):
        """Save all posts to a single HTML file"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog Collection</title>
    <style>
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f9f9f9;
        }
        .container {
            background-color: white;
            padding: 40px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            text-align: center;
        }
        .post {
            margin-bottom: 50px;
            page-break-after: always;
        }
        .post-title {
            color: #2980b9;
            font-size: 2em;
            margin-bottom: 10px;
            margin-top: 30px;
        }
        .post-meta {
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 20px;
            font-size: 0.9em;
        }
        .post-content {
            text-align: justify;
        }
        .post-content img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
        }
        .post-content p {
            margin-bottom: 15px;
        }
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 40px 0;
        }
        @media print {
            body {
                background-color: white;
            }
            .container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>My Blog Collection</h1>
"""
        
        # Sort posts by published date
        def get_sort_key(post):
            published = post.get('published', '')
            if not published:
                return ''
            try:
                # Try ISO format first
                return datetime.fromisoformat(published.replace('Z', '+00:00')).isoformat()
            except:
                return published
        
        sorted_posts = sorted(self.posts, key=get_sort_key)
        
        for i, post in enumerate(sorted_posts, 1):
            title = post.get('title', 'Untitled')
            content = self.clean_html(post.get('content', ''))
            published = post.get('published', '')
            
            # Format date
            if published:
                try:
                    date_obj = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%B %d, %Y')
                except:
                    formatted_date = published
            else:
                formatted_date = 'Unknown date'
            
            html_content += f"""
        <div class="post">
            <h2 class="post-title">{i}. {title}</h2>
            <div class="post-meta">Published on {formatted_date}</div>
            <div class="post-content">
                {content}
            </div>
        </div>
"""
            if i < len(sorted_posts):
                html_content += "        <hr>\n"
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML file saved to: {output_file}")
        return output_file
    
    def save_to_markdown(self, output_file: str = "blog_ebook.md"):
        """Save all posts to a single Markdown file"""
        md_content = "# My Blog Collection\n\n"
        
        # Sort posts by published date
        def get_sort_key(post):
            published = post.get('published', '')
            if not published:
                return ''
            try:
                return datetime.fromisoformat(published.replace('Z', '+00:00')).isoformat()
            except:
                return published
        
        sorted_posts = sorted(self.posts, key=get_sort_key)
        
        for i, post in enumerate(sorted_posts, 1):
            title = post.get('title', 'Untitled')
            content = post.get('content', '')
            published = post.get('published', '')
            
            # Format date
            if published:
                try:
                    date_obj = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    formatted_date = date_obj.strftime('%B %d, %Y')
                except:
                    formatted_date = published
            else:
                formatted_date = 'Unknown date'
            
            # Convert HTML to plain text (basic conversion)
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text(separator='\n\n')
            text_content = html.unescape(text_content)
            
            md_content += f"""
## {i}. {title}

*Published on {formatted_date}*

{text_content}

---

"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"✓ Markdown file saved to: {output_file}")
        return output_file


def main():
    print("=" * 60)
    print("Blogger to eBook Converter (Web Scraping)")
    print("=" * 60)
    print()
    
    # Get blog URL from user
    blog_url = input("Enter your Blogger blog URL (e.g., https://myblog.blogspot.com): ").strip()
    
    # Initialize converter
    converter = BloggerToEbook(blog_url)
    
    # Fetch posts
    print("\nFetching posts...")
    converter.fetch_posts_via_feed()
    
    if not converter.posts:
        print("\n⚠ No posts found!")
        print("This could mean:")
        print("  - Your blog URL is incorrect")
        print("  - Your blog is private")
        print("  - Your blog has no published posts")
        return
    
    print(f"\n✓ Successfully fetched {len(converter.posts)} posts!")
    
    # Choose output format
    print("\nChoose output format:")
    print("1. HTML (recommended - best for PDF conversion)")
    print("2. Markdown")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if not choice:
        choice = '1'
    
    print()
    if choice in ['1', '3']:
        converter.save_to_html()
    
    if choice in ['2', '3']:
        converter.save_to_markdown()
    
    print("\n" + "=" * 60)
    print("✓ Conversion complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("📄 For PDF:")
    print("   1. Open 'blog_ebook.html' in your browser")
    print("   2. Press Ctrl+P (or Cmd+P on Mac)")
    print("   3. Select 'Save as PDF'")
    print("   4. Adjust margins if needed")
    print("   5. Click 'Save'")
    print("\n📚 For EPUB:")
    print("   1. Download Calibre (free): https://calibre-ebook.com/")
    print("   2. Add 'blog_ebook.html' to Calibre")
    print("   3. Convert to EPUB format")
    print()


if __name__ == "__main__":
    main()