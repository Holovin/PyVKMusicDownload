import logging
import os


class FM:
    @staticmethod
    def do_directory(path, exist_ignore=True):
        os.makedirs(path, exist_ok=exist_ignore)
        logging.debug("Create directory: " + path)
        return

    @staticmethod
    def check_file(path):
        if os.path.isfile(path):
            return True

        return False

    @staticmethod
    def file_size(path):
        if FM.check_file(path):
            return os.stat(path).st_size

        return -1

    @staticmethod
    def safe_file_name(file_name):
        out = ''

        for char in file_name:
            if char.isalnum() or char in '()_-[].&\'",|#':
                out += char
            else:
                out += '_'

        return out