import requests
import bs4

response = requests.get('https://habr.com/ru/all/')
response.raise_for_status()

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}

soup = bs4.BeautifulSoup(response.text, features='html.parser')

article = soup.find('article')

articles = soup.find_all('article')

for article in articles:
    total_text = []
    title = article.find(class_='tm-article-snippet__title-link').find("span").text.lower().split()
    hubs = article.find(class_='tm-article-snippet__hubs-item-link').text.lower().split()
    post_link = article.find(class_='tm-article-snippet__title-link').attrs['href']
    post_link = 'https://habr.com' + post_link
    post = requests.get(post_link)
    post.raise_for_status()
    post_soup = bs4.BeautifulSoup(post.text, features='html.parser')
    post_text = post_soup.find('div', class_='tm-article-body').text
    post_word = [word for word in post_text.split(' ')]
    total_text = title + hubs + post_word
    for i in KEYWORDS:
        if i in total_text:
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            time = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
            link = 'https://habr.com' + href
            print(time, '-', article.find("h2").text, '-', link)
            break
