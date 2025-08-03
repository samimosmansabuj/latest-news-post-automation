# page = urlopen(jamuna_tv_site)
# html = page.read().decode("utf-8")


# def start___ ():
#     print("কোন ওয়েবসাইট থেকে নিউজ কালেকশন করবেন? Jamuna/Prothom Alo")
#     print("01. Jamuna")
#     print("02. Prothom Alo")
#     which_site = input('Enter 01 or 02: ')
#     if int(which_site) == 1:
#         print("Start New Scrapping from Jamuna! Are you sure?")
#         agree = input('Yes or No: ')
#         if agree.lower() == 'yes':
#             print('Thank you Jamuna')
#         else:
#             print("Wrong Input!")
#             return start___()
#     elif int(which_site) == 2:
#         print("Start New Scrapping from Prothom Alo! Are you sure?")
#         agree = input('Yes or No: ')
#         if agree.lower() == 'yes':
#             print('Thank you Prothom Alo')
#         else:
#             print("Wrong Input!")
#             return start___()
#     elif which_site.lower() == 'exit':
#         return exit
#     else:
#         print("Wrong Input!")
#         return start___()

# start___()


# # news = urlopen(news_details_url)
# print(f"Found Latest News: {news_details_url}!")
# print("Starting news scraping...")
# news = urlopen(news_details_url)
# news_html = news.read().decode("utf-8")
# news_page_content = BeautifulSoup(news_html, 'html.parser')
# print("News Scrapping Successfully!")


















# def verify_latest_news(news_url):
#     news_view_request = requests.get(url=news_url, headers={"User-Agent": "Mozilla/5.0"})
#     news_view = BeautifulSoup(news_view_request.content, "html.parser")
#     news_time = news_view.find("time").get_text(strip=True)
#     time_cleanning = news_time.replace("st", "").replace("nd", "").replace("rd", "").replace("th", "")
#     news_time_formating = bd_tz.localize(datetime.strptime(time_cleanning, "%d %B, %Y %I:%M %p"))
#     current_time = datetime.now(bd_tz)
    
#     diff = int((current_time - news_time_formating).total_seconds() // 60)
#     if 0 <= diff <= 150:
#         print(f"Found Latest News (within 5 minutes): {news_url}!")
#         print("Starting news scraping...")
#         return news_view



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



