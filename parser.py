# threads_scraper/parser.py
import json
import re
from parsel import Selector
from nested_lookup import nested_lookup
import jmespath
from typing import List, Dict
from utils.lang_detect import detect_language


def parse_threads_page(page_content: str, keyword: str) -> List[Dict]:
    """Universal Threads parser.Retrieves posts and replies, detects language and adds a keyword field."""
    selector = Selector(page_content)
    posts_data = []

    scripts = selector.css('script[type="application/json"][data-sjs]::text').getall()

    for script in scripts:
        if '"thread_items"' not in script:
            continue

        try:
            data = json.loads(script)
        except json.JSONDecodeError:
            continue

        threads = nested_lookup("thread_items", data)
        if not threads:
            continue

        for thread_list in threads:
            for thread in thread_list:
                parsed = extract_post_data(thread, keyword)
                if parsed:
                    posts_data.append(parsed)

    return posts_data


def extract_post_data(post: dict, keyword: str) -> dict:
    """
    Extracts fields from a Threads post with support for different data structures.
    """
    try:
        data = jmespath.search(
            """
            {
                nickname: post.user.username,
                text: post.caption.text,
                likes: post.like_count || post.likeCount || post.likecount,
                reposts: post.repost_count || post.text_post_app_info.repost_count || post.text_post_app_info.repostCount,
                comments: post.comment_count || post.text_post_app_info.direct_reply_count || post.text_post_app_info.reply_count
            }
            """, post)

        if not data or not data.get("text"):
            return None

        data["lang"] = detect_language(data["text"])
        data["keyword"] = keyword
        data["text"] = clean_text(data["text"])

        for key in ("likes", "reposts", "comments"):
            data[key] = data.get(key, 0) or 0

        return data

    except Exception as e:
        print(f"[⚠️] Post's parsing error: {e}")
        return None



def clean_text(text: str) -> str:
    """Delete HTML tags and unwanted characters from text."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\s.,!?@#\$%\-\(\)\":;]", "", text)
    return text.strip()
