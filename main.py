import time
import sched
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

import exceptions
from notification import Notify

s = sched.scheduler(time.time, time.sleep)


def format_response(columns, method='accident'):
    matches = re.finditer(r">((?:\\.|.).*?)<", columns)
    out = []
    for match in matches:
        request = match.group()
        out.append(request[1:-1])
    if method == 'accident':
        return f"В {out[2]}.\n{out[8]}, {out[10]}.\nЗ {out[12]} по {out[14]}."
    else:
        print(out)
        return f'Not implemented'


class PowerOffLoe:
    """
    Scrap tables from https://poweroff.loe.lviv.ua.
    using parametric: city, street, otg
    """

    def __init__(self, city='', street='', otg='', group: int = 0):
        self.address = city, street, otg
        if group not in range(3):
            raise exceptions.InvalidGroupNumber('В Львівській області заявлено 3 групи')
        self.group = group
        self.result = []
        self.page = self.__scrap_page()
        self.__communication()

    def __communication(self):
        self.__get_accident()
        if self.group:
            self.__get_group_schedule()
        else:
            self.result.append('Група споживачів не обрана.')
        Notify(self.result)

    def __scrap_page(self):
        try:
            url = "https://poweroff.loe.lviv.ua/search_off?csrfmiddlewaretoken=" \
                  "QRUjXkiT8HWXOxqCn5y8mezrCJQuWaLzJMwKaykvgNYALnaUClTiBB3usHb0O" \
                  "rlF&city={}&street={}&otg={}&q=%D0%9F%D0%BE%D1%88%D1%83%D0%BA".format(*self.address, {})
            page = requests.get(url)
            return page
        except requests.exceptions.ConnectTimeout:
            self.result = "Відсутній інтернет"

    def __get_group_schedule(self):
        try:
            self.result.append('Not implemented')
        except AttributeError:
            self.result.append(f"Тимчасові незручності спричинені змінами на сайті!")

    def __get_accident(self):
        try:
            soup = BeautifulSoup(self.page.text, "html.parser")
            table = soup.select('table')[2]
            columns = str(table.find('tbody').find_all('td'))
            self.result.append(format_response(columns))
        except AttributeError:
            self.result.append(f"В {self.address[0].capitalize()} аварійних відключень непередбачено!")


def start(sc):
    city = "Сіде"
    street = ''
    otg = ''
    group = 0
    PowerOffLoe(city, street, otg, group)
    sc.enter(600, 1, start, (sc,))


if __name__ == '__main__':
    s.enter(0, 1, start, (s,))
    s.run()
