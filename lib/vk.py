import json
import logging

import re
import webbrowser

from lib.network import Network


class VK:
    VK_APP_ID = 5559086
    API_VERSION = '5.53'
    URI_API = 'https://api.vk.com/method/'
    URI_OAUTH = 'https://oauth.vk.com/'

    RESPONSE = 'response'
    ATTACHMENTS = 'attachments'
    WALL_MAX_COUNT = 100
    ACCESS_TOKEN = 'access_token'

    network = None
    token = ''
    token_url = ''

    def __init__(self, network: Network, token=''):
        self.network = network
        self.token = token
        self.token_url = '&' + self.ACCESS_TOKEN + '=' + token
        return

    @staticmethod
    def _dict_to_params(params):
        out = ''

        for key, value in params.items():
            out += key + '=' + value + '&'

        return out[:-1]

    def _check_error(self):
        temp = self.network.get_data_json()

        if 'error' in temp:
            logging.error('VK api error(' + str(temp['error']['error_code']) + '): ' + temp['error']['error_msg'])
            return True

        return False

    @staticmethod
    def auth_window():
        webbrowser.open(
            'https://oauth.vk.com/authorize?client_id=' + str(VK.VK_APP_ID) +
            '&display=page&scope=audio,wall&redirect_uri=https://oauth.vk.com/blank.html&response_type=token' +
            '&v=' + VK.API_VERSION)
        return

    def auth_direct(self, login, password, client_id, clinet_secret):
        params = self._dict_to_params({
            'grant_type': 'password',
            'client_id': str(client_id),
            'client_secret': str(clinet_secret),
            'username': login,
            'password': password,
            'v': self.API_VERSION,
        })

        self.network.do_get(self.URI_OAUTH + 'token?' + params)
        resp = self.network.get_data_json()

        if not self._check_error():
            return resp[self.ACCESS_TOKEN]

        return False

    @staticmethod
    def _link_to_login(link):
        # convert raw link to user_name if needed
        r = re.search('(https?://vk.com/)?(.+)', link)

        if r.group(2):
            return r.group(2)

        return False

    def api_get_user_id(self, user_link):
        user_link = self._link_to_login(user_link)

        self.do_api_get('users.get', {'user_ids': user_link})
        if not self._check_error():
            users = self.network.get_data_json()[self.RESPONSE]

            if len(users) > 0:
                return users[0]['id']

        return False

    def api_get_user_wall(self, domain, offset, count):
        if 0 > count or count > self.WALL_MAX_COUNT:
            logging.warning('Count param is incorrect')
            return False

        domain = self._link_to_login(domain)

        self.do_api_get('wall.get',
                        {'domain': domain,
                         'filter': 'owner',
                         'count': str(count),
                         'offset': str(offset)
                         })

        if not self._check_error():
            return self.network.get_data_json()

        return False

    def api_get_user_wall_raw(self, domain, offset, count, user_hash):
        if 0 > count or count > self.WALL_MAX_COUNT:
            logging.warning('Count param is incorrect')
            return False

        domain = self._link_to_login(domain)

        data = {'act': 'a_run_method',
                'al': '1',
                'hash': user_hash,
                'method': 'wall.get',
                'param_count': str(count),
                'param_domain': domain,
                'param_extended': '0',
                'param_offset': str(offset),
                'param_v': self.API_VERSION
                }

        self.network.do_post('https://new.vk.com/dev/', data)

        data = self.network.get_data()
        data = re.search('<!>({.+)', data)

        if data.group(1):
            return json.loads(data.group(1))
        else:
            logging.fatal('RawParse error')
            return False


    @staticmethod
    def json_wall_get_total(json):
        return json[VK.RESPONSE]['count']

    def do_api_get(self, method_name, params):
        self.network.do_get(self.URI_API + method_name + '?' + self._dict_to_params(params) + '&v=' + self.API_VERSION +
                            self.token_url)
        return True

    def do_api_post(self, method_name, params):
        params[VK.ACCESS_TOKEN] = self.token
        self.network.do_post(self.URI_API + method_name + '&v=' + self.API_VERSION, params)
        return True
