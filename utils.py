from googletrans import Translator
import asyncio
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import os
from io import BytesIO
from slugify import slugify
load_dotenv()

# username = os.getenv('USERNAME')
# app_password = os.getenv('APP_PASSWORD')



async def translate_text(text):
    async with Translator() as translator:
        result = await translator.translate(text)
        return result.text



def get_category(category_name):
    try:
        #Translate English
        category = asyncio.run(translate_text(category_name))
        #Get All Client Category List
        response = requests.get(os.getenv('CLIENT_SITE_CATEGORY_GET_API_ENDPOINT'))
        
        if response.status_code == 200:
            #Convert Json All Category List
            categories = response.json()
            category_id = None
            for ctg in categories:
                if category == ctg['name']:
                    category_id = ctg['id']
                    return category_id
            return category_id
        else:
            print("❌ Failed to get categories:", response.status_code)
    except Exception as e:
        print("❌ Error:", e)


def uploadMediaFile(image_path, title):
    username = os.getenv('CLIENT_USERNAME')
    app_password = os.getenv('CLIENT_APP_PASSWORD')

    image_response = requests.get(image_path)
    if image_response.status_code != 200:
        print("Failed to download image from URL")
        return None
    img = BytesIO(image_response.content)
    
    headers = {
        'Content-Disposition': f'attachment; filename={slugify(title)+'.jpg'}',
        'Content-Type': 'image/jpeg'
    }
    response = requests.post(
        url=os.getenv('CLIENT_SITE_MEDIA_UPLOAD_API_ENDPOINT'),
        auth=HTTPBasicAuth(username, app_password),
        headers=headers,
        data=img
    )
    
    img.close()
    
    if response.status_code == 201:
        return response.json()['id']
    else:
        print("Failed to upload image")
        print(response.status_code, response.text)


