import time
import sched
import requests
import re
from bs4 import BeautifulSoup
from win10toast import ToastNotifier

s = sched.scheduler(time.time, time.sleep)


class PowerOffLoe:
    """
    Scrap tables from https://poweroff.loe.lviv.ua.
    using parametric: city, street, otg
    """

    def __init__(self, city='', street='', otg=''):
        self.address = city, street, otg
        self.table = ''
        self.columns = ''
        self.result = ''
        self.__scrap_power_off()
        self.__send_win_notification()

    def __scrap_power_off(self):
        try:
            url = "https://poweroff.loe.lviv.ua/search_off?csrfmiddlewaretoken=" \
                  "QRUjXkiT8HWXOxqCn5y8mezrCJQuWaLzJMwKaykvgNYALnaUClTiBB3usHb0O" \
                  "rlF&city={}&street={}&otg={}&q=%D0%9F%D0%BE%D1%88%D1%83%D0%BA".format(*self.address, {})
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            self.table = soup.select('table')[0]
            self.columns = str(self.table.find('tbody').find_all('td'))
            self.__format_text()
        except AttributeError:
            self.result = f"В {self.address[0].capitalize()} запланованих аварійних відключень немає!"
        except requests.exceptions.ConnectTimeout:
            self.result = "Відсутній інтернет"

    def __format_text(self):
        matches = re.finditer(r">((?:\\.|.).*?)<", self.columns)
        out = []
        for match in matches:
            request = match.group()
            out.append(request[1:-1])
        self.result = f"В {out[2]}.\n{out[8]}, {out[10]}.\nЗ {out[12]} по {out[14]}."

    def __send_win_notification(self):
        try:
            toaster = ToastNotifier()
            toaster.show_toast(title="Прошу уваги!!", msg=self.result, duration=5, threaded=True)
            while toaster.notification_active():
                time.sleep(0.1)
        except TypeError:
            # Lag for Python 3.11
            pass


def start(sc):
    city = "Сіде"
    street = ''
    otg = ''
    PowerOffLoe(city, street, otg)
    sc.enter(600, 1, start, (sc,))


if __name__ == '__main__':
    s.enter(0, 1, start, (s,))
    s.run()