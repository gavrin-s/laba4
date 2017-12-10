import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from threading import Thread, Lock
from datetime import datetime
import time

headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}


def get_posts(url, queue, headers=None):
    while True:
        titles = set()
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        post_list = soup.find('div', {'class': 'feed__container'})
        items = post_list.find_all('div', {'class': 'feed__item'})

        for item in items[::-1]:
            date = item.find('time', {'class': 'time'}).get('title')
            date = datetime.strptime(date[:-16], "%d.%m.%Y %H:%M:%S")
            author = item.find('span', {'class': 'entry_header__author__name'}).text
            title = item.find('div', {'class': 'entry_content--short'}).find('span').text
            try:
                content = item.find('div', {'class': 'entry_content--short'}).find('p').text
            except AttributeError:
                content = ''

            if title not in titles:
                titles.add(title)

                queue.put({'date': date,
                           'author': author,
                           'title': title,
                           'content': content})
                """print({'date': date,
                       'author': author,
                       'title': title,
                       'content': content})"""
        time.sleep(600)  # every 10 minutes update news


if __name__ == "__main__":
    url = 'https://tjournal.ru/recent'
    queue = Queue()

    thread = Thread(target=get_posts, args=(url, queue), kwargs={'headers':headers,})
    thread.daemon = True
    thread.start()

    safeprint = Lock()

    while True:
        try:
            data = queue.get(block=False)
        except Empty:
            pass
            #print('queue is empty')
        else:
            with safeprint:
                print(data)
        time.sleep(20) # print one new every 20 secods from queue
