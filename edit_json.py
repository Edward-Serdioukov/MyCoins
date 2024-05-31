import json

# Открытие и чтение исходного JSON-файла
with open('coins.json', 'r') as file:
    data = json.load(file)

# Добавление нового атрибута 'description' к каждому элементу
for item in data:
    item['description'] = ''

# Запись обновленных данных обратно в JSON-файл
with open('coins.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Updated JSON with 'description' attribute.")
