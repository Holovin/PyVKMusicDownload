import logging


class Config:
    USER_LOGIN = ''             # for: get_token_direct
    USER_PASSWORD = ''          # for: get_token_direct | if 2fa enabled insert here special app password
    USER_HASH = ''              # need for *_raw methods
    USER_TOKEN = ''             # insert result from get_token_*.py or leave empty

    USER_LINK = ''              # user name to download (can be https://vk.com/durov or just durov)
    OUTPUT_DIRECTORY = ''       # inner directory name for download
    SKIP_EXISTS = True          # if True files with size > 0 will be skipped

    # vk official keys for get_token_direct method
    APP_ID = 2274003
    APP_SECRET = 'hHbZxrka2uZ6jB1inYsH'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
        #'Cookie': ''           # need for *_raw methods
    }