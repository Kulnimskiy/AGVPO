import os
import time
from datetime import datetime, timezone


class Monkey(object):
    def __init__(self, filepath):
        self._cached_stamp = 0
        self.filename = filepath

    def ook(self):
        stamp = datetime.fromtimestamp(os.stat(self.filename).st_mtime, tz=timezone.utc)
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            print(self.filename[-20 : ] + " has changed" + " " + str(stamp))


def main():
    while True:
        file = Monkey(input("Введи путь к файлу: "))
        file.ook()
        time.sleep(1)


if __name__ == '__main__':
    main()
