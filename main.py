from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from utils import get_category, uploadMediaFile
from difflib import get_close_matches
import requests
import os
import pytz
import re

bd_tz = pytz.timezone("Asia/Dhaka")
load_dotenv()

headers = {"User-Agent": "Mozilla/5.0"}


#Function for scrapping single news=======================================================
def single_news_scrapping(news_url):
    news_view_request = requests.get(news_url, headers=headers)
    news_view = BeautifulSoup(news_view_request.content, "html.parser")
    return news_view

#Function for parse news time==============================================================
def parse_news_time(news_time_str):
    # Remove ordinal suffix like '1st', '2nd', '3rd', '4th'
    time = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', news_time_str)
    try:
        news_time = datetime.strptime(time, "%d %B, %Y %I:%M %p")
        return bd_tz.localize(news_time)
    except Exception as e:
        print("Time parsing failed:", e)
        return None

#Function for Check with title this news created or not=====================================
def check_with_title(post_title):
    post_list = []
    params = {
        'after': datetime.now().strftime("%Y-%m-%dT00:00:00"),
        '_fields': 'title,date',
        'per_page': 100,
    }
    response = requests.get("https://www.banglatrend.online/wp-json/wp/v2/posts", params=params)
    if response.status_code == 200:
        posts = response.json()
        for post in posts[:15]:
            post_list.append(post['title']['rendered'])
    else:
        print("❌ Failed to fetch posts:", response.status_code)
    
    if post_title in post_list:
        return False
    return True


#Funcation for verify latest news=============================================================
def verify_latest_news(latest_news_list):
    list = []
    for news_url in latest_news_list:
        news_view = single_news_scrapping(news_url)
        news_time = parse_news_time(news_view.find("time").get_text(strip=True))
        news_title = check_with_title(news_view.find("h1", class_="story-title").get_text(strip=True))
        if news_time and (datetime.now(bd_tz) - news_time) <= timedelta(minutes=120) and news_title:
            # print(f"✅ This news ({news_url}) was posted within the last 120 minutes...")
            list.append(news_url)
        else:
            print(f"⏩ This news ({news_url}) is older than 120 minutes or already created. Skipping...")
    return list

#function for Get list of Latest news===========================================================
def scrapping_home_page():
    #Define a list for latest news-------------------------
    latest_news_list = []
    
    print("Start Scrapping Home Page!!!")
    
    #Scrapping Start Home/Site
    site_view_request = requests.get(os.getenv("NEWS_SITE_URL"), headers=headers)
    site_view = BeautifulSoup(site_view_request.content, "html.parser")
    
    #Add Feature latest News in Latest news List-----------
    latest_news_list.append(site_view.find_all("section", id="post")[0].select("article.article")[0].find("a", class_="story-link")["href"])
    
    #Add latest News in Latest news List-------------------
    latest_articles_section = site_view.find_all("section", id="post")[1].select("article.article")
    for article in latest_articles_section:
        latest_news_list.append(article.find("a")["href"])
    
    #cleaning news for post within 5 munites
    print("Verify latest news searching...")
    latest_news_list = verify_latest_news(latest_news_list)
    if latest_news_list:
        print(f"{len(latest_news_list)} Latest news found!")
        return latest_news_list
    else:
        print("❌ Not found latest news that was posted within the last 120 minutes...")



def unmatch_category_selection(category_name):
    category_keyword = {
        'অপরাধ': [],
        'আন্তর্জাতিক': [],
        'খেলাধুলা': ["ক্রিকেট", "ফুটবল", "অলিম্পিক", "খেলোয়ার"],
        'গাইড এবং টিপস': [],
        'চাকরি': [],
        'জাতীয়': [],
        'জীবনযাপন': [],
        'বাণিজ্য': [],
        'বিনোদন': ["শিল্প ও সাহিত্য"],
        'মতামত': [],
        'রাজনীতি': [],
        'সারাদেশ': [],
    }
    for key, values in category_keyword.items():
        if category_name in values:
            return key
    return None

#function for Get news Category===========================================================
def get_matching_category(category_name):
    category_name = category_name.strip()
    try:
        response = requests.get(os.getenv('CLIENT_SITE_CATEGORY_GET_API_ENDPOINT'))
        if response.status_code == 200:
            categories = {cat['name'].strip(): cat['id'] for cat in response.json()}
            category = categories[category_name] if category_name in categories.keys() else None
            if category is not None:
                return category
            else:
                matching_category = unmatch_category_selection(category_name)
                category = categories[matching_category] if matching_category in categories.keys() else None
                if category:
                    return category

                #use difflib---------------
                # best_match = get_close_matches(category_name, categories.keys(), n=1, cutoff=0.5)
                # if best_match:
                #     match_name = best_match[0]
                
                
                print(f"❌ Category '{category_name}' not found in API.")
                print("Scrapping news Category: ", category_name)
                # print("Site news Category: ", categories)
                return None
        else:
            print("❌ Failed to get categories:", response.status_code)
            return None
    except Exception as e:
        print("❌ Error:", e)
        return None


#function for Scrapping news and Create post===========================================================
def create_post(news_url, count):
    print(f"🚀 {count} News Scrapping Start...")
    news_view = single_news_scrapping(news_url)
    print(f"🟢 {count} News Scrapping Successfully!!!")
    
    print("⏳ Extract & Data Collection from Scrapping...")
    title = news_view.find("h1", class_="story-title").get_text(strip=True)
    print("News Title: ", title)
    category = get_matching_category(news_view.find("a", class_="story-tag-link").get_text(strip=True))
    feature_image_url = news_view.find("img", class_="wp-post-image")['src']
    article_text_content = []
    for p in news_view.find("div", class_="article-content").find_all("p"):
        if not p.find("img") and len(p.text) > 10:
            article_text_content.append(p.get_text(strip=True))
    article_text_content.append("সোর্স যমুনা নিউজ।")
    print("🟢 Data Collecting & Store Successfully!")
    
    #Create Post=============================================================================
    print(f"⏳ Creating {count} post on your site...")
    create_post_api_url = os.getenv("CLIENT_SITE_CREATE_POST_API_ENDPOINT")
    username = os.getenv("CLIENT_USERNAME")
    password = os.getenv("CLIENT_APP_PASSWORD")
    
    print("Uploading featured image...")
    feature_image = uploadMediaFile(feature_image_url, title)
    print("Image uploaded!")
    
    post_data = {
        "title": f"{title}",
        "content": "<p>" + "<br><br>".join(article_text_content) + "<p>",
        # "content": f"{article_text_content}",
        "status": "publish",
        "featured_media": feature_image,
        "categories": category
    }
    response = requests.post(
        url=create_post_api_url,
        auth=HTTPBasicAuth(username, password),
        json=post_data
    )
    if response.status_code == 201:
        print("Post created successfully!")
        print("Post URL:", response.json().get("link"))
    else:
        print("Failed to create post")
        print("Status Code:", response.status_code)
        print("Response:", response.text)





if __name__ == "__main__":
    count = 0
    news_list = scrapping_home_page()
    for news_url in news_list:
        print('-------------Starting...------------------------')
        count += 1
        create_post(news_url, count)
        print('-------------End!!!------------------------')
        
    print(f"{count} Post created successfully!")
    

