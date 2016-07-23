import logging


class Config:
    USER_LINK = 'user'
    USER_TOKEN = ''
    OUTPUT_DIRECTORY = 'vk_music/'
    OVERRIDE_EXISTS = True

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:2.0b7) Gecko/20100101 Firefox/4.0b7',
    }