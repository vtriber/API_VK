import requests
from pprint import pprint
from vktoken import vktoken
#
class VkLoading():

    def __init__(self, token):
        self.token = token

    def req_photo_info(self, owner_id):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.owner_id,
                  'extended': '1',
                  'album_id': 'profile',
                  'access_token': self.token,
                  'v': '5.131'}
        res = requests.get(url, params=params)
        return res.json()

    def loading_photo(self, owner_id):
        photo_copy = {}
        all_photo_json = []
        inf_photo = self.req_photo_info()
        for select_photo in inf_photo['response']['items']:
            max_size = 0
            photo_json = {}
            for size_photo in select_photo['sizes']:
                if size_photo['height'] >= max_size:
                    max_size = size_photo['height']
                    url_photo = size_photo['url']
                    size = size_photo['type']
            if select_photo['likes']['count'] in photo_copy:
                photo_name = f"{select_photo['likes']['count'] + select_photo['date']}.jpg"
            else:
                photo_name = f"{select_photo['likes']['count']}.jpg"

            photo_copy[photo_name] = url_photo
            photo_json['file_name'] = photo_name
            photo_json['size'] = size
            all_photo_json.append(photo_json)


        pprint(all_photo_json)
        pprint(photo_copy)
owner_id = '3660349'
vk = VkLoading(token=vktoken)
vk.loading_photo(owner_id=owner_id)
#pprint(
#
#
#
# r = requests.get(url)
#
# # urllib.urlretrieve(url, "photo.jpg")
# #
# with open('photo.png', 'wb') as code:
#     code.write(r.content)
# #
