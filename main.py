import time
import sched
import requests
import pandas as pd
from notification import Notify

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
        self.__run()

    def __run(self):
        self.__scrap_page()
        self.__get_accident()
        Notify(self.result)

    def __scrap_page(self):
        try:
            url = "https://poweroff.loe.lviv.ua/search_off?csrfmiddlewaretoken=" \
                  "QRUjXkiT8HWXOxqCn5y8mezrCJQuWaLzJMwKaykvgNYALnaUClTiBB3usHb0O" \
                  "rlF&city={}&street={}&otg={}&q=%D0%9F%D0%BE%D1%88%D1%83%D0%BA".format(*self.address, {})
            page = requests.get(url)
            self.tables = pd.read_html(page.text)
        except requests.exceptions.ConnectTimeout:
            self.result = "Відсутній інтернет"

    def __get_accident(self):
        try:
            table = self.tables[2]
            self.result = "В {2}.\n{5}, {6}.\nЗ {7} \nПо {8}.".format(*table.values[0])
        except AttributeError:
            self.result = f"В {self.address[0].capitalize()} аварійних відключень непередбачено!"


def start(sc):
    city = ""
    street = ''
    otg = ''
    PowerOffLoe(city, street, otg)
    sc.enter(600, 1, start, (sc,))


if __name__ == '__main__':
    s.enter(0, 1, start, (s,))
    s.run()
