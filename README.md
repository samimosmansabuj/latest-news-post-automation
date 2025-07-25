<div align="center">
<h1>News Post Automation</h1>
Scrapping Latest News from any Popular Website & create a news post with scrapping data in your website!!!
<br>
</div>

<br>

## How to Run This Project Step by step --------


### Clone from GitHub

-   Clone the repository

```bash
git clone https://github.com/samimosmansabuj/latest-news-post-automation.git
```

-   Go to the project directory

```bash
cd latest-news-post-automation
```

-   Create a virtual environment

```bash
python -m venv venv
```

-   Activate the virtual environment

```bash
source venv/Scripts/activate
```

-   Install the dependencies or Lib

```bash
pip install -r requirements.txt
```

-   Run the server

```bash
python latest_news_post_automation.py
```

-   Create a file named `.env` in the `latest-news-post-automation` directory and add the following lines

```bash
NEWS_SITE_URL = website_url (ex: https://jamuna.tv/)

# CLIENT_SITE---------------
CLIENT_SITE_CREATE_POST_API_ENDPOINT = post_create_api_endpoint (ex: https://base_url/wp-json/wp/v2/posts)
CLIENT_SITE_CATEGORY_GET_API_ENDPOINT = category_list_api_endpoint (ex: https://base_url/wp-json/wp/v2/categories/)
CLIENT_SITE_MEDIA_UPLOAD_API_ENDPOINT = media_file_upload_endpoint (ex: https://base_url/wp-json/wp/v2/media/)
CLIENT_USERNAME = website_url
CLIENT_APP_PASSWORD = user_app_password
```


