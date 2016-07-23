#!/usr/bin/python

import logging
from getpass import getpass

from config import Config
from lib.network import Network
from lib.vk import VK


def main():
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)
    ########################################################

    n = Network()
    vk = VK(n)

    print('Token is: ' + vk.auth_direct(Config.USER_LOGIN, Config.USER_PASSWORD, Config.APP_ID, Config.APP_SECRET))

    ########################################################
    logging.info("--- APP END ---")
    return

if __name__ == "__main__":
    main()
