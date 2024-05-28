import csv
import flet as ft
from bs4 import BeautifulSoup
import requests
import json
import time

def get_price_from_html(html):
    # Использование BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Поиск элемента по классу и извлечение текста из тега <span>
    try:
        price_span = soup.find('a', class_='right price-container').find('span')
    except Exception as e:
        print(e)
        return "Нет цены"
    return price_span.text


def fetch_prices(page: ft.Page, content: ft.Column, urls):
    prices = []
    proxy = {
        'http': 'http://38.54.16.97:80',
        'https': 'http://38.54.16.97:80'
    }
    for url in urls:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        """
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
            print(response.text)
        except requests.exceptions.ProxyError:
            print("Проблема с прокси")
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения")
        """
        # Отправка HTTP запроса и получение ответа
        #response = requests.get(url)
        if response.status_code == 200:
            price = get_price_from_html(response.text)
            time.sleep(31)
        else:
            price = "Ошибка загрузки страницы"
        prices.append(price)
        content.controls.append( ft.Row([ft.Text("Цена на странице"),
                    ft.Text(spans=[ ft.TextSpan(f"{url}", ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE), url=url, ),]), 
                    ft.Text(f": {price}")]))

        page.update()   
    return prices

def main(page: ft.Page):
    page.title = "Извлечение цен"
    page.vertical_alignment = "start"

    # Поле ввода для URL
    #urls_textbox = ft.TextField(label="Введите URL, разделяя их запятыми", text_align="start", width=300, multiline=True)
    #page.add(urls_textbox)

    # Кнопка для запуска процесса извлечения
    #fetch_button = ft.ElevatedButton(text="Извлечь цены", on_click=lambda _: fetch_button_click(page, urls_textbox))
    # Создание контейнера с возможностью прокрутки
    content = ft.Column(scroll=True, auto_scroll=True, width=page.width, height=page.height)

    data = []   
    fetch_button = ft.ElevatedButton(text="Извлечь цены", on_click=lambda _: fetch_button_click(page, content, data))
    content.controls.append(fetch_button)
    page.add(content)
    

#def fetch_button_click(page: ft.Page, urls_textbox: ft.TextField):
def fetch_button_click(page: ft.Page, content: ft.Column, data):
    # Получение списка URL из текстового поля
    #urls = [url.strip() for url in urls_textbox.value.split(",") if url.strip()]
    
    # Путь к вашему JSON файлу
    filename = 'coins.json'

    # Чтение данных из файла и их загрузка в список словарей
    with open(filename, 'r') as f:
        data = json.load(f)

    urls = []
    for coin in data:
        url = coin["url"]
        urls.append(url)

    prices = fetch_prices(page, content, urls)

    # Путь к файлу CSV, который вы хотите создать
    filename = 'urls_and_prices.csv'

    # Открытие файла для записи
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Запись заголовков столбцов
        writer.writerow(['URL', 'Price'])
        
        # Проходим по спискам urls и prices параллельно с помощью функции zip
        for url, price in zip(urls, prices):
            writer.writerow([url, price])

    print(f'Данные успешно записаны в файл {filename}')

    # Отображение результатов
    """
    for i, price in enumerate(prices, start=1):
        content.controls.append(    
                        ft.Text(spans=[ ft.TextSpan(f"Цена на странице {urls[i-1]}: {price}", 
                    ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    url=urls[i-1], ),]))

    # Обновляем страницу, чтобы отобразить новые результаты
    page.update()
    """
if __name__ == "__main__":
    ft.app(target=main)