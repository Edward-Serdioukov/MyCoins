import json
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Загрузка данных из JSON-файлов
with open('coins.json', 'r') as f:
    coins_data = json.load(f)

with open('countries.json', 'r') as f:
    countries_data = json.load(f)

# Подсчет количества монет по странам
coin_counts = Counter(coin['country'] for coin in coins_data)

# Преобразование данных в DataFrame для удобства
coin_counts_df = pd.DataFrame(coin_counts.items(), columns=['country', 'count'])

# Преобразование данных о странах в DataFrame
countries_df = pd.DataFrame(countries_data)

# Приведение названий стран к единому формату (заглавные буквы)
coin_counts_df['country'] = coin_counts_df['country'].str.title()
countries_df['country'] = countries_df['country'].str.title()

# Объединение данных по странам
merged_df = pd.merge(coin_counts_df, countries_df, on='country', how='left')

# Сортировка данных по убыванию количества монет
sorted_df = merged_df.sort_values(by='count', ascending=False)

# Функция для добавления изображения флага
def get_flag_image(path, zoom=0.05):
    if pd.notna(path):  # Проверяем, что путь к изображению не является NaN
        try:
            image = plt.imread("assets"+path)
            return OffsetImage(image, zoom=zoom)
        except FileNotFoundError:
            print(f"Файл не найден: {path}")
        except Exception as e:
            print(f"Ошибка при загрузке флага: {e}")
    return None

# Создание горизонтальной столбчатой диаграммы
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(sorted_df['country'], sorted_df['count'], color='skyblue')

# Настройка диаграммы
ax.set_xlabel('Количество монет')
ax.set_ylabel('Страны')
ax.set_title('Количество монет по странам')
ax.invert_yaxis()  # Обратный порядок, чтобы максимальные значения были сверху

# Добавление названий стран и флагов
for i, (bar, (_, row)) in enumerate(zip(bars, sorted_df.iterrows())):
    country_label = row['country']
    flag_path = row['src']
    bar_y_center = bar.get_y() + bar.get_height() / 2

    # Добавление названия страны
    ###ax.text(bar.get_width(), bar_y_center, f' {country_label}', va='center')

    # Добавление флага после названия страны
    """
    flag_image = get_flag_image(flag_path)
    if flag_image:
        ab = AnnotationBbox(flag_image, (0, bar_y_center), frameon=False, xycoords="data", boxcoords="offset points", pad=0)
        ax.add_artist(ab)
    """
plt.show()

# Вывод данных в консоль
for _, row in sorted_df.iterrows():
    print(f"{row['country']}: {row['count']}")
