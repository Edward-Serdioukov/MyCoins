import csv

# Предположим, что у нас есть два списка:
urls = ['http://example.com/product1', 'http://example.com/product2', 'http://example.com/product3']
prices = ['10.99', '15.49', '8.99']

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