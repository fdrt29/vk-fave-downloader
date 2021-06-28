#!/usr/bin/env python
__author__ = "Fedor Teleshov <fdrt29@gmail.com>"
__copyright__ = "Copyright 2021"

import os
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
    if tag_name == '':
        return 0
    response = vk.fave.getTags()
    for item in response['items']:
        if item["name"] == tag_name:
            return int(item["id"])
    raise ValueError('Could not find a tag with the same name')


def process_item(item) -> list:
    urls = list()
    if 'attachments' not in item['post']:
        return []
    for attachment in item['post']['attachments']:
        if attachment['type'] != 'photo':
            continue
        urls.append(get_maximum_image(attachment['photo'])['url'])
    return urls


def get_maximum_image(photo):
    return max(photo['sizes'], key=lambda p: p['height'])


def download_images(urls: list, path):
    counter = 0
    for url in urls:
        print('download %i '.format(counter) + url)
        img_data = requests.get(url).content
        with open(path + '\\{0}.jpg'.format(str(counter)), 'wb') as handler:
            handler.write(img_data)
        counter += 1


def create_download_directory():
    path = '.\\vk-downloaded'
    path_counter = 0
    while os.path.exists(path + str(path_counter)):
        path_counter += 1
    path += str(path_counter)
    os.makedirs(path)
    return path


def main():
    login, password = sys.argv[1:3]
    starting_with_post = int(sys.argv[3]) - 1
    posts_quantity = int(sys.argv[4])
    tag_name = sys.argv[5] if len(sys.argv) == 6 else ''

    vk = auth(login, password)

    try:
        my_tag_id = get_tag_id(tag_name, vk)
    except Exception as e:
        print(e)
        return

    urls = list()
    still_to_load_posts = posts_quantity
    while still_to_load_posts > 0:
        load_on_iteration = max(0, min(100, still_to_load_posts))
        offset = starting_with_post + (posts_quantity - still_to_load_posts)
        try:
            response = vk.fave.get(tag_id=my_tag_id, count=load_on_iteration, offset=offset)
        except Exception as e:
            print(e)
            return
        still_to_load_posts -= load_on_iteration
        for item in response['items']:
            urls += process_item(item)

    path = create_download_directory()
    download_images(urls, path)


if __name__ == '__main__':
    main()
