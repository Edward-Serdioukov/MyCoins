from PIL import Image

filename = 'c:\\work\\MY\\doc\\MyCoins\\beijing-olympic-logo2.jpg'  # Путь к исходному изображению
icon_size = (64, 64)  # Размер иконки

image = Image.open(filename)
#image = image.resize(icon_size, Image.ANTIALIAS)  # Изменение размера изображения
image.save('output_icon.ico', format='ICO')  # Сохранение иконки