import requests
import random
from bs4 import BeautifulSoup

__all__ = ['get_image']

"""NSFW functions"""

# Function for getting the site parameters
async def get_site_params(site: str):
    site_url = {
        'danbooru': 'https://danbooru.donmai.us',
        'gelbooru': 'https://gelbooru.com/index.php?',
        'rule34': 'https://rule34.xxx/index.php?'
    }[site]
    tag_param = {
        'danbooru': '/post/index.xml?limit=100&tags=',
        'gelbooru': 'page=dapi&s=post&q=index&tags=',
        'rule34': 'page=dapi&s=post&q=index&tags='
    }[site]
    id_param = {
        'danbooru': '/posts/',
        'gelbooru': 'page=post&s=view&id=',
        'rule34': 'page=post&s=view&id='
    }[site]
    return site_url, tag_param, id_param

# Function for getting image
async def get_image(site: str, tags: str):
    site_url, tag_param, id_param = await get_site_params(site)
    try:
        r = requests.get(site_url + tag_param + tags.lower())
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            post_count = soup.find('posts').find_all('post')
            if (site != 'danbooru' and int(soup.find('posts')['count']) == 0) or len(post_count) == 0:
                return None, None, 'The specified tag returned no results.'
            else:
                post = post_count[random.randint(0, len(post_count)-1)]
                file_url = post['file_url']
                post_link = site_url + id_param + post['id']
                return file_url, post_link, None
        else:
            if site == 'danbooru' and r.status_code == 422:
                error_message = 'Danbooru searches are limited to two tags.'
            else:
                error_message = f'Couldn\'t process the request. Status code: {r.status_code} {r.reason}.'
            return None, None, error_message
    except requests.exceptions.RequestException as e:
        return None, None, f'**ERROR:** {type(e).__name__} - {e}'