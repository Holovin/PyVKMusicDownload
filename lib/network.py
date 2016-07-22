import logging

import requests
from config import Config


class Network:
    session = None
    last_answer = ""

    def __init__(self):
        self.clean()
        return

    # core
    def get_data(self):
        return self.last_answer.text

    def get_data_json(self):
        return self.last_answer.json()

    def clean(self):
        self.last_answer = None
        self.session = requests.Session()
        logging.info("Downloader init... ok")

        return

    def _get_cookie_value(self, name):
        return self.session.cookies.get(name)

    def do_get(self, url):
        logging.debug("Get url: " + url)

        try:
            self.last_answer = self.session.get(url, headers=Config.HEADERS)
            logging.debug("Result url (" + str(self.last_answer.status_code) + " : " + self.last_answer.url + ")")

            if self.last_answer.url.lower() != url.lower():
                logging.warning("Redirect to: " + self.last_answer.url)

        except requests.exceptions.RequestException as e:
            logging.fatal("Fatal error [get url]: " + str(e))
            exit()

        logging.debug("Getting url... ok")
        return True

    def do_post(self, url, data):
        logging.debug("Post url: " + url)

        try:
            self.last_answer = self.session.post(url, headers=Config.HEADERS, data=data)
            logging.debug("Result url (" + str(self.last_answer.status_code) + " : " + self.last_answer.url + ")")

        except requests.exceptions.RequestException as e:
            logging.fatal("Fatal error [post url]: " + str(e))
            exit()

        logging.debug("Posting url... ok")
        return True
