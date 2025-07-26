from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv
import os
load_dotenv()
from utils import get_category, uploadMediaFile
from datetime import datetime, timedelta
import pytz
import time

bd_tz = pytz.timezone('Asia/Dhaka')


def main():
    while True:
        try:
            # >>> PLACE ALL YOUR SCRAPING AND POSTING CODE HERE <<<

            


            def verify_latest_news(news_url):
                news_view_request = requests.get(url=news_url, headers={"User-Agent": "Mozilla/5.0"})
                news_view = BeautifulSoup(news_view_request.content, "html.parser")
                news_time = news_view.find("time").get_text(strip=True)
                time_cleanning = news_time.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
                news_time_formating = bd_tz.localize(datetime.strptime(time_cleanning, "%d %B, %Y %I:%M %p"))
                current_time = datetime.now(bd_tz)
                
                diff = int((current_time - news_time_formating).total_seconds() // 60)
                if 0 <= diff <= 5:
                    print(f"Found Latest News (within 5 minutes): {news_url}!")
                    print("Starting news scraping...")
                    return news_view

            def select_latest_news_url(articles):
                for article in articles:
                    # news_url = article.find("a", class_="story-link")['href']
                    news_url = article.find("a")['href']
                    verifyNews = verify_latest_news(news_url)
                    if verifyNews:
                        return verifyNews
                return None


            # Scrapping Main Website Page & Select Latest News====================================
            # def run_news_checker():
            #     print(f"\n🕒 Checking news at {datetime.now(bd_tz).strftime('%Y-%m-%d %I:%M:%S %p')}")
            #     site_view_request = requests.get(
            #         url=os.getenv('NEWS_SITE_URL'),
            #         headers={"User-Agent": "Mozilla/5.0"}
            #     )
            #     site_view = BeautifulSoup(site_view_request.content, "html.parser")
            #     #Jamuna Home Page Second 4 Card News
            #     articles2 = site_view.find_all("section", class_="row")[1].select("article.article")
                
            #     print("🔍 Verifying latest news...")
            #     latest_new = select_latest_news_url(articles2[:4])
            #     if latest_new is None:
            #         print("❌ Not found a latest news")
            #         exit()
            #     print("News Scrapping Successfully!")



            print("Starting latest news searching...")
            site_view_request = requests.get(url=os.getenv('NEWS_SITE_URL'), headers={"User-Agent": "Mozilla/5.0"})
            site_view = BeautifulSoup(site_view_request.content, "html.parser")

            #Jamuna Home Page Second 4 Card News
            articles2 = site_view.find_all("section", class_="row")[1].select("article.article")
            #Jamuna Home Page Feature News
            # articles = site_view.select("article.article")

            print("Verify latest news searching...")
            latest_new = select_latest_news_url(articles2[:4])
            if latest_new is None:
                print("❌ Not found a latest news")
                # exit()
            else:
                print("News Scrapping Successfully!")


                # Single News Scrapping=============================================================
                print("Extract & Data Collection from Scrapping...")
                print("News Title: ", latest_new.find("h1", class_="story-title").get_text(strip=True))
                title = latest_new.find("h1", class_="story-title").get_text(strip=True)
                category_id = get_category(latest_new.find("a", class_="story-tag-link").text)
                news_image = latest_new.find("img", class_="wp-post-image")['src']
                article_text_content = []
                for p in latest_new.find("div", class_="article-content").find_all("p"):
                    if not p.find('img') and len(p.text) > 10:
                        article_text_content.append(p.text)
                article_text_content.append("সোর্স যমুনা নিউজ।")

                print("Data Collecting & Store Successfully!")

                # create_post_url = os.getenv('CLIENT_SITE_CREATE_POST_API_ENDPOINT')

                # def create_post_your_website(url, *args, **kwargs):
                #     username = os.getenv('CLIENT_USERNAME')
                #     app_password = os.getenv('CLIENT_APP_PASSWORD')
                    
                #     print("Uploading featured image...")
                #     feature_image = uploadMediaFile(args[2], title)
                #     print("Image uploaded!")
                    
                #     post_data = {
                #         "title": f"{title}",
                #         "content": "<p>" + "<br><br>".join(article_text_content) + "<p>",
                #         # "content": f"{article_text_content}",
                #         "status": "publish",
                #         "featured_media": feature_image
                #     }
                #     print("Creating post on your site...")
                #     response = requests.post(
                #         url=url,
                #         auth=HTTPBasicAuth(username, app_password),
                #         json=post_data
                #     )
                #     return response

                # response = create_post_your_website(create_post_url, title, category_id, news_image, article_text_content)

                # if response.status_code == 201:
                #     print("Post created successfully!")
                #     print("Post URL:", response.json().get("link"))
                # else:
                #     print("Failed to create post")
                #     print("Status Code:", response.status_code)
                #     print("Response:", response.text)

            print("✅ Script execution completed. Waiting 5 minutes...\n")
            time.sleep(30)  # 5 minutes = 300 seconds

        except Exception as e:
            print("⚠️ Error occurred:", e)
            print("Retrying in 5 minutes...\n")
            time.sleep(30)


if __name__ == "__main__":
    main()

