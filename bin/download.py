#!/usr/bin/python

import logging
import time
from datetime import datetime
from config import Config
from lib.fm import FM
from lib.network import Network
from lib.vk import VK


def main():
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)
    ########################################################
    FM.do_directory(Config.OUTPUT_DIRECTORY)

    n = Network()
    vk = VK(n, Config.USER_TOKEN)

    current = 0
    total = 1

    while current < total:
        data = vk.api_get_user_wall(Config.USER_LINK, current, VK.WALL_MAX_COUNT)
        total = vk.json_wall_get_total(data)

        for record in data[VK.RESPONSE]['items']:
            logging.info('Progress: ' + str(current) + ' / ' + str(total))
            current += 1

            date = datetime.fromtimestamp(record['date']).strftime('%Y_%m_%d')
            FM.do_directory(Config.OUTPUT_DIRECTORY + date)

            if VK.ATTACHMENTS not in record:
                logging.debug('Skip date: ' + date + ' because post without audio')
                continue

            for attach in record['attachments']:
                if attach['type'] == 'audio':
                    file_name = FM.safe_file_name(attach['audio']['artist'] + ' - ' + attach['audio']['title'] + '.mp3')
                    file_path = Config.OUTPUT_DIRECTORY + date + '/' + file_name
                    file_size = FM.file_size(file_path)

                    if not Config.OVERRIDE_EXISTS or file_size > 0:
                        logging.debug('Skip file [' + file_name + '] because it exist')
                        continue

                    logging.info('Getting file [' + file_name + ']...')
                    url = attach['audio']['url']

                    if url == '':
                        if file_size == -1:
                            logging.info('DCMA file. Create empty and skip...')
                            open(file_path, 'w').close()
                        else:
                            logging.info('DCMA file. Skip...')

                        continue

                    time.sleep(1)
                    n.do_get(url, True)

                    if n.last_answer.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in n.last_answer:
                                f.write(chunk)
                    else:
                        logging.warning('Wrong HTTP answer...')
                        continue

                    logging.info('Downloaded ok...')

    ########################################################
    logging.info("--- APP END ---")
    return

if __name__ == "__main__":
    main()
