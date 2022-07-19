import requests
from pprint import pprint
from vktoken import vktoken
#

url = 'https://api.vk.com/method/photos.get'
params = {'owner_id': '3660349',
          'extended': '1',
          'album_id': 'profile',
          'access_token': vktoken,
          'v': '5.131'}
res = requests.get(url, params=params)
inf_photo = res.json()
# pprint(inf_photo['response']['items']['sizes'])
# pprint(inf_photo)

for select_photo in inf_photo['response']['items']:
    # pprint(select_photo)
    max_size = 0
    for next_photo in select_photo['sizes']:
        # print(next_photo['height'])
        # print(next_photo['url'])
        if next_photo['height'] >= max_size:
            max_size = next_photo['height']
            name_photo =



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
