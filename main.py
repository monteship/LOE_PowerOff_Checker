import time
import sched
import requests
import pandas as pd
from notifypy import Notify

s = sched.scheduler(time.time, time.sleep)


def get_loe_accident(*address):
    try:
        url = "https://poweroff.loe.lviv.ua/search_off?csrfmiddlewaretoken=" \
              "QRUjXkiT8HWXOxqCn5y8mezrCJQuWaLzJMwKaykvgNYALnaUClTiBB3usHb0O" \
              "rlF&city={}&street={}&otg={}&q=%D0%9F%D0%BE%D1%88%D1%83%D0%BA".format(*address, {})
        page = requests.get(url)
        tables = pd.read_html(page.text)
        table = tables[2]
        return "В {2}.\n{5}, {6}.\nЗ {7} \nПо {8}.".format(*table.values[0])
    except IndexError:
        return f"В {address[0].capitalize()} аварійних відключень непередбачено!"
    except requests.exceptions.ConnectTimeout:
        return "Відсутній інтернет"


def get_schedule(self):  # ToDo
    url = 'https://poweroff.loe.lviv.ua/gav_city3'
    page = requests.get(url)
    send_post = requests.post(url, cookies=page.cookies)


def send_notify(message):
    notification = Notify()
    notification.title = "PowerOffLoe"
    notification.message = message
    notification.send()


def start(sc):
    city = 'Сіде'
    street = ''
    otg = ''
    response = get_loe_accident(city, street, otg)
    send_notify(response)
    sc.enter(600, 1, start, (sc,))


if __name__ == '__main__':
    s.enter(0, 1, start, (s,))
    s.run()
