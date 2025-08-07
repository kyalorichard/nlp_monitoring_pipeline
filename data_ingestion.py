from snscrape.modules.twitter import TwitterSearchScraper
from GoogleNews import GoogleNews
from googleapiclient.discovery import build
from facebook_scraper import get_posts
import pandas as pd
import datetime
import json
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create data directory
if not os.path.exists('data'):
    os.makedirs('data')


# ===================== TWITTER =====================
def scrape_twitter(query="digital ID", limit=100):
    logging.info("Scraping Twitter...")
    tweets = []
    try:
        for i, tweet in enumerate(TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            tweets.append({
                "platform": "Twitter",
                "date": tweet.date.strftime("%Y-%m-%d %H:%M:%S"),
                "content": tweet.content
            })
    except Exception as e:
        logging.error(f"Twitter scraping failed: {e}")
    return tweets


# ===================== GOOGLE NEWS =====================
def scrape_google_news(query="digital ID", period="7d"):
    logging.info("Scraping Google News...")
    googlenews = GoogleNews(period=period)
    googlenews.search(query)
    results = googlenews.results()
    news_items = [{
        "platform": "GoogleNews",
        "date": item["date"],
        "content": f"{item['title']} - {item['desc']}"
    } for item in results]
    return news_items


# ===================== YOUTUBE =====================
def scrape_youtube_comments(query="digital ID", api_key="", max_results=5):
    logging.info("Scraping YouTube...")
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(q=query, part="id", type="video", maxResults=max_results)
    response = request.execute()

    comments = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        try:
            comment_req = youtube.commentThreads().list(
                part="snippet", videoId=video_id, maxResults=10
            ).execute()
            for c in comment_req["items"]:
                comments.append({
                    "platform": "YouTube",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "content": c["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                })
        except Exception as e:
            logging.warning(f"Error getting comments for video {video_id}: {e}")
            continue
    return comments


# ===================== FACEBOOK =====================
def scrape_facebook(page="UNDP", max_posts=5):
    logging.info(f"Scraping Facebook page: {page}")
    posts = []
    try:
        for post in get_posts(page, pages=1):
            posts.append({
                "platform": "Facebook",
                "date": post["time"].strftime("%Y-%m-%d %H:%M:%S"),
                "content": post["text"][:500] if post["text"] else ""
            })
            if len(posts) >= max_posts:
                break
    except Exception as e:
        logging.error(f"Facebook scraping failed: {e}")
    return posts


# ===================== COLLECT AND SAVE =====================
def collect_data():
    twitter_data = scrape_twitter()
    news_data = scrape_google_news()
    youtube_data = scrape_youtube_comments(api_key=os.getenv("YOUTUBE_API_KEY", ""))
    facebook_data = scrape_facebook()

    combined = twitter_data + news_data + youtube_data + facebook_data

    output_path = "data/latest_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    logging.info(f"Data collection complete. Saved to {output_path}")


if __name__ == "__main__":
    collect_data()
