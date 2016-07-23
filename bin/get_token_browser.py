#!/usr/bin/python

import logging
from lib.vk import VK


def main():
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)
    ########################################################
    VK.open_auth_window()
    ########################################################
    logging.info("--- APP END ---")
    return

if __name__ == "__main__":
    main()
