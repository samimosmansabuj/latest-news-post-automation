from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv
import os
load_dotenv()
from utils import get_category, uploadMediaFile




# Scrapping Main Website Page & Select Latest News====================================
print("Starting latest news searching...")
page = urlopen(os.getenv('NEWS_SITE_URL'))
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
a_tag = soup.body.article.div.a
news_details_url = a_tag['href']

# news = urlopen(news_details_url)
print(f"Found Latest News: {news_details_url}!")
print("Starting news scraping...")
news = urlopen(news_details_url)
news_html = news.read().decode("utf-8")
news_page_content = BeautifulSoup(news_html, 'html.parser')
print("News Scrapping Successfully!")

# Single News Scrapping=============================================================
print("Extract & Data Collection from Scrapping...")
main_content = news_page_content.body.section.div
article_content_details = main_content.find('div', class_="article-content")

title = main_content.h1.text
category_id = get_category(main_content.a.text)
news_time = main_content.span.time.text.strip()
article_picture = article_content_details.p.img['src']
article_text_content = []

for p in article_content_details.find_all('p'):
    if not p.find('img') and len(p.text) > 10:
        article_text_content.append(p.text)

print("Data Collecting & Store Successfully!")

my_url = os.getenv('CLIENT_SITE_CREATE_POST_API_ENDPOINT')


def create_post_your_website(url, *args, **kwargs):
    username = os.getenv('CLIENT_USERNAME')
    app_password = os.getenv('CLIENT_APP_PASSWORD')
    
    print("Uploading featured image...")
    feature_image = uploadMediaFile(args[3], title)
    print("Image uploaded!")
    
    post_data = {
        "title": f"{title}",
        "content": f"{article_text_content}",
        "status": "publish",
        "featured_media": feature_image
    }
    print("Creating post on your site...")
    response = requests.post(
        url=url,
        auth=HTTPBasicAuth(username, app_password),
        json=post_data
    )
    return response

response = create_post_your_website(my_url, title, category_id, news_time, article_picture, article_text_content)

if response.status_code == 201:
    print("Post created successfully!")
    print("Post URL:", response.json().get("link"))
else:
    print("Failed to create post")
    print("Status Code:", response.status_code)
    print("Response:", response.text)





