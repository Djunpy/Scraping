import requests
from bs4 import BeautifulSoup
import time
from random import randrange
import json

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}


def get_articles_url(url):
    s = requests.Session()  # Отправляем запрос на главную стр
    response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('span', class_='navigations').find_all('a')[-1].text)  # Определяем количество страниц

    articles_urls_list = []
    for page in range(1, pagination_count + 1):  # Проходим циклом по каждой странице
        response = s.get(url=f'https://hi-tech.news/page/{page}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        articles_urls = soup.find_all('a', class_='post-title-a') # Получаем все post-title-a

        for au in articles_urls:  # Проходимся цилом по post-title-a и собираем ссылки на статьи
            art_url = au.get('href')
            articles_urls_list.append(art_url)
            # time.sleep(randrange(2, 5))
            print(f'Обработал => {page}/{pagination_count}')

    with open('articles_urls.txt', 'w') as file:
        for url in articles_urls_list:
            file.write(f'{url}\n')

    return 'Работа по сбору ссылок выполнена!'


def get_data(file_path):
    with open(file_path) as file:
        urls_list = [line.strip() for line in file.readlines()]

    urls_count = len(urls_list)
    s = requests.Session()

    result_data = []
    for url in enumerate(urls_list[:50]):
        response = s.get(url=url[1], headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        article_title = soup.find('div', class_='post-content').find('h1', class_='title').text.strip()
        article_date = soup.find('div', class_='post').find('div', class_='tile-views').text.strip()
        article_img = f"'https://hi-tech.news/ {soup.find('div', class_='post-media-full').find('img').get('src')}'"
        article_content = soup.find('div', class_='the-excerpt').text.strip().replace('\n', '')

        result_data.append(
            {
                'original_url': url[1],
                'article_title': article_title,
                'article_date': article_date,
                'article_img': article_img,
                'article_content': article_content,
            }
        )
        #print(f'{article_title}\n{article_date}\n{article_img}\n {10*"#"}')
        print(f'Обработал {url[0] + 1}/{urls_count}')

    with open('result.json', 'w', encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    #print(get_articles_url(url='https://hi-tech.news/'))
    get_data('articles_urls.txt')


if __name__ == '__main__':
    main()