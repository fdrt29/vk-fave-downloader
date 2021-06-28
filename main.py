#!/usr/bin/env python
__author__ = "Fedor Teleshov <fdrt29@gmail.com>"
__copyright__ = "Copyright 2021"

import sys
from pprint import pprint

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


def process_post(post):
    pprint(post)


def get_tag_id(tag_name: str, vk) -> int:
    response = vk.fave.getTags()
    for item in response['items']:
        if item["name"] == tag_name:
            return int(item["id"])
    return 0


def main():
    login, password = sys.argv[1:3]
    vk = auth(login, password)

    my_tag_id = get_tag_id("References", vk)
    if my_tag_id == 0:
        raise ValueError('Could not find a tag with the same name')
    response = vk.fave.get(tag_id=my_tag_id, count=4)
    pprint(response)
    # for post in response['items']:
    #     process_post(post)


if __name__ == '__main__':
    main()
