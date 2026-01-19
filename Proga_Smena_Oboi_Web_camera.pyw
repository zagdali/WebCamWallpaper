import requests
import ctypes
import time
import os
import threading
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem, Icon
import tkinter as tk
from tkinter import simpledialog

# Глобальная переменная для времени ожидания
sleep_time = 10

def download_image(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f'Изображение успешно скачано и сохранено как: {file_path}')
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при скачивании изображения: {e}')

def set_wallpaper(image_path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        print(f'Обои установлены: {image_path}')
    except Exception as e:
        print(f'Ошибка при установке обоев: {e}')

def main(url, file_path):
    file_path = os.path.join(os.getcwd(), file_path)
    download_image(url, file_path)
    set_wallpaper(file_path)

def update_wallpapers():
    urls = [
        ('https://kamery.humlnet.cz/images/webcams/trutnov/2048x1536.jpg', 'trutnov_image.jpg'),
        # ('https://kamery.humlnet.cz/images/webcams/zacler/2048x1536.jpg', 'zacler.jpg'),
        # ('https://kamery.humlnet.cz/images/webcams/janskelazne/2048x1536.jpg', 'janskelazne.jpg')
    ]
    
    while True:
        for url, file_path in urls:
            main(url, file_path)
            time.sleep(sleep_time)

def create_image(width, height):
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2 - 10, height // 2 - 10, width // 2 + 10, height // 2 + 10),
        fill=(0, 0, 0))
    return image

def on_quit(icon, item):
    icon.stop()

def change_sleep_time(icon, item):
    global sleep_time
    
    # Инициализация Tkinter для использования диалогового окна
    root = tk.Tk()
    root.withdraw()  # Скрываем основное окно

    # Создаем диалоговое окно для ввода нового времени ожидания
    new_time = simpledialog.askinteger("Изменить время ожидания", "Введите время ожидания в секундах:", minvalue=1)
    
    if new_time is not None:
        sleep_time = new_time
        print(f'Время ожидания изменено на: {sleep_time} секунд')

# Создаем иконку в трее с дополнительным пунктом меню для изменения времени ожидания
icon = Icon("Wallpaper Changer", create_image(64, 64), "Wallpaper Changer", menu=pystray.Menu(
    MenuItem("Change Sleep Time", change_sleep_time),
    MenuItem("Quit", on_quit)
))

# Запускаем поток для обновления обоев
threading.Thread(target=update_wallpapers, daemon=True).start()

# Запускаем иконку в трее
icon.run()