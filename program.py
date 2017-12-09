import requests
from bs4 import BeautifulSoup

headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}


def get_posts(url, headers=None):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    post_list = soup.find('div', {'class': 'feed__container'})
    items = post_list.find_all('div', {'class': 'feed__item'})

    posts = []

    for item in items:
        datetime = item.find('time', {'class':'time'}).get('title')
        author = item.find('span', {'class': 'entry_header__author__name'}).text
        title = item.find('div', {'class':'entry_content--short'}).find('span').text
        try:
            content = item.find('div', {'class':'entry_content--short'}).find('p').text
        except AttributeError:
            content = ''

        posts.append({'datetime': datetime,
                   'author': author,
                   'title': title,
                   'content': content})

    return posts




if __name__ == "__main__":
    url = 'https://tjournal.ru/'
    posts = get_posts(url, headers)
    print(posts)