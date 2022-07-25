import os
import dload
import requests
from pprint import pprint
from vktoken import vktoken

class VkLoading():
    def __init__(self, token, owner_id, folder):
        self.token = token
        self.owner_id = owner_id
        self.folder = folder

    def req_photo_info(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.owner_id,
                  'extended': '1',
                  'album_id': 'profile',
                  'access_token': self.token,
                  'v': '5.131'}
        res = requests.get(url, params=params)
        return res.json()

    def loading_photo(self):
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
                photo_name = f"{select_photo['likes']['count']}{select_photo['date']}.jpg"
            else:
                photo_name = f"{select_photo['likes']['count']}.jpg"

            photo_copy[photo_name] = url_photo
            photo_json['file_name'] = photo_name
            photo_json['size'] = size
            all_photo_json.append(photo_json)

        os.mkdir(self.folder)
        for filename, url in photo_copy.items():
            path_file = self.folder + '/' + filename
            dload.save(url, path_file)
            print(f'Файл {filename} загружен на компьютер')
        print(f'Всего загружено {len(photo_copy)} файлов')

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.token)}

    def creat_folder(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'false'}
        response = requests.put(upload_url, headers=headers, params=params)

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': f'{disk_file_path}/{file}', 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path):
        response_href = self._get_upload_link(disk_file_path=disk_file_path)
        href = response_href.get('href', '')
        response = requests.put(href, data=open(f'{os.getcwd()}/{disk_file_path}/{file}', 'rb'))


def API_VK():
    owner_id = input('Введите ID аккаунта Вконтакте: ')
    folder = input('Введите имя папки куда будут загружены фотографии: ')
    vk = VkLoading(token=vktoken, owner_id=owner_id, folder=folder)
    vk.loading_photo()

    token = input('Введите токен для доступа к Яндекс Диску: ')
    ya = YandexDisk(token=token)
    ya.creat_folder(disk_file_path=folder)

    file_list = os.listdir(folder)
    hundred_percent = len(file_list)
    file_percent = 100 // hundred_percent
    symbol_percent = '#'
    percent = symbol_percent * file_percent
    step = 0
    for file in file_list:
        ya.upload_file_to_disk(disk_file_path=folder)
        step += 1
        print('\n' * 100)
        print('Ход загрузки:')
        print(f'{percent * step} Загружено {file_percent * step} %')

if __name__ == '__main__':
    API_VK()