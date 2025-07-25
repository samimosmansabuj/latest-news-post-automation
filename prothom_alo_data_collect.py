from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

import re
site_url = "https://www.prothomalo.com/search"
params = {"sort": "latest-published"}
headers = {"User-Agent": "Mozilla/5.0"}


def scrapping_selected_news(news_view_page):
    try:
        
        title = news_view_page.find("h1", class_="IiRps").text.strip()
        category = news_view_page.find("a", class_="vXi2j").text.strip()
        
        feature_image = ""
        
        all_images = news_view_page.find_all("img")
        print("Found", len(all_images), "images")

        for img in all_images:
            print("IMG:", img)
            print("SRC:", img.get("src"))
            print("DATA-SRC:", img.get("data-src"))
        
    except:
        pass
    
    


def is_withing_5_munites(news_time):
    bangla_to_english_digit = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")
    news_time = news_time.translate(bangla_to_english_digit)
    minute_match = re.search(r"(\d+)\s*মিনিট", news_time)
    hour_match = re.search(r"(\d+)\s*ঘন্টা", news_time)
    
    if hour_match:
        return False
    
    if minute_match:
        minutes = int(minute_match.group(1))
        return minutes <= 30
    
    return False


def select_news_from_webpage(article):
    news_time = article.find("time", class_="published-time").text.strip()
    if is_withing_5_munites(news_time):        
        news_view_url = article.find("a", class_="title-link")['href']
        # news_view_request = Request(news_view_url, headers=headers)
        news_view_request = requests.get(news_view_url, headers=headers)
        
        news_view_page = BeautifulSoup(news_view_request.content, "html.parser")
        # news_view_page = BeautifulSoup(urlopen(news_view_request).read().decode("utf-8"), "html.parser")
        
        scrapping_selected_news(news_view_page)
    else:
        print("গত ৫ মিনিটে নতুন কোনো পোস্ট করা হয়নি।")



print("Starting latest news searching...")
# site_view_request = Request(site_url, headers=headers)
site_view_request = requests.get(url=site_url, headers=headers, params=params)
try:
    # page = urlopen(site_view_request)
    # html = page.read().decode("utf-8")
    soup = BeautifulSoup(site_view_request.content, "html.parser")
    articles = soup.select("div.K-MQV")
    for article in articles[:2]:
        select_news_from_webpage(article)
except Exception as e:
    print("❌ Error occurred:", e)








# print(news_heading.text.strip())

# print(article.a["href"])

# headline_tag = article.find("a", class_="story-link")
# title = headline_tag.text.strip() if headline_tag else "No title"
# link = "https://www.prothomalo.com" + headline_tag["href"] if headline_tag else "No link"

# # Category (if exists)
# category_tag = article.select_one("p.category-title a")
# category = category_tag.text.strip() if category_tag else "No category"

# # Image (if exists)
# img_tag = article.find("img")
# image_url = img_tag["src"] if img_tag else "No image"

# print("\n📰 Title:", title)
# print("🔗 Link:", link)
# print("📂 Category:", category)
# print("🖼️ Image:", image_url)



