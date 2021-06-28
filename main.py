#!/usr/bin/env python
__author__ = "Fedor Teleshov <fdrt29@gmail.com>"
__copyright__ = "Copyright 2021"

import sys

import requests
import vk_api


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция."""

    # Код двухфакторной аутентификации
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def auth(login, password):
    """ Пример обработки двухфакторной аутентификации """

    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    return vk_session.get_api()


def get_tag_id(tag_name: str, vk) -> int:
    response = vk.fave.getTags()
    for item in response['items']:
        if item["name"] == tag_name:
            return int(item["id"])
    raise ValueError('Could not find a tag with the same name')


def process_item(item):
    urls = list()
    for attachment in item['post']['attachments']:
        if not attachment['photo']:
            return
        urls.append(get_maximum_image(attachment['photo'])['url'])
    download_images(urls)
    # pprint(item)


def get_maximum_image(photo):
    return max(photo['sizes'], key=lambda p: p['height'])


def download_images(urls: list):
    counter = 0
    for url in urls:
        img_data = requests.get(url).content
        with open('{0}.jpg'.format(str(counter)), 'wb') as handler:
            handler.write(img_data)
        counter += 1


def main():
    login, password = sys.argv[1:3]
    vk = auth(login, password)

    try:
        my_tag_id = get_tag_id("References", vk)
    except Exception as e:
        print(e)
        return

    response = vk.fave.get(tag_id=my_tag_id, count=1)
    # pprint(response)
    for item in response['items']:
        process_item(item)


if __name__ == '__main__':
    main()
