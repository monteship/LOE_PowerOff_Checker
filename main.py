import time
import sched

import lxml
import requests
import pandas as pd
from notifypy import Notify
from bs4 import BeautifulSoup

s = sched.scheduler(time.time, time.sleep)


class PowerOffLoe:
    """
    Scrap tables from https://poweroff.loe.lviv.ua.
    using parametric: city, street, otg
    """

    def __init__(self, city='', street='', otg=''):
        self.address = city, street, otg
        self.result = []
        self.tables = None
        self.__get_accident()
        self.__get_schedule()
        self.__send_notify()

    def __get_accident(self):
        try:
            url = "https://poweroff.loe.lviv.ua/search_off?csrfmiddlewaretoken=" \
                  "QRUjXkiT8HWXOxqCn5y8mezrCJQuWaLzJMwKaykvgNYALnaUClTiBB3usHb0O" \
                  "rlF&city={}&street={}&otg={}&q=%D0%9F%D0%BE%D1%88%D1%83%D0%BA".format(*self.address, {})
            page = requests.get(url)
            tables = pd.read_html(page.text)
            table = tables[2]
            self.result = "В {2}.\n{5}, {6}.\nЗ {7} \nПо {8}.".format(*table.values[0])
        except IndexError:
            self.result = f"В {self.address[0].capitalize()} аварійних відключень непередбачено!"
        except requests.exceptions.ConnectTimeout:
            self.result = "Відсутній інтернет"

    def __get_schedule(self):  # ToDo
        url = 'https://poweroff.loe.lviv.ua/gav_city3'
        page = requests.get(url)
        send_post = requests.post(url, cookies=page.cookies)

    def __send_notify(self):
        notification = Notify()
        notification.title = "PowerOffLoe"
        notification.message = self.result
        notification.send()


def start(sc):
    city = 'Сіде'
    street = ''
    otg = ''
    PowerOffLoe(city, street, otg)
    sc.enter(600, 1, start, (sc,))


if __name__ == '__main__':
    s.enter(0, 1, start, (s,))
    s.run()
