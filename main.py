import time
import sched
import requests
import pandas as pd
from notifypy import Notify

s = sched.scheduler(time.time, time.sleep)


def get_loe_accident(address) -> str:
    try:
        client = requests.session()
        url = 'https://poweroff.loe.lviv.ua/'
        client.get(url)
        csrftoken = client.cookies['csrftoken']
        payload = {'csrfmiddlewaretoken': csrftoken}
        response = requests.get(url, data={**payload, **address})
        table = pd.read_html(response.text)[2]
        return "В {2}.\n{5}, {6}.\nЗ {7} \nПо {8}.".format(*table.values[0])
    except IndexError:
        return f"В {address['city'].capitalize()} аварійних відключень непередбачено!"
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
    address = {
        'city': 'Сіде',
        'street': '',
        'otg': ''}
    response = get_loe_accident(address)
    send_notify(response)
    sc.enter(600, 1, start, (sc,))


if __name__ == '__main__':
    s.enter(0, 1, start, (s,))
    s.run()
