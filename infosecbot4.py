# Код считывает ссылки на Telegram-каналы из файла channels.txt.
# №од записывает в HTML файл строки с обогащенными данными о каналах.
# Код записывает в Excel файл telegram_infosecurity.xlsx строки с данными о каналах.
# Код использует библиотеку telethon для работы с Telegram API. 
# И Телеграм блокируют наш доступ к API на 12 часов за слишком частое использование функции GetFullChannelRequest
# Для обхода блокировки используем ограничение скорости запросов.
# Для этого добавляем константы REQUESTS_LIMIT и REQUEST_INTERVAL.
# Для ограничения скорости запросов используем time.sleep(REQUEST_INTERVAL) после каждого запроса.
# Но такой способ не является оптимальным, так как блокировка может быть наложена на IP-адрес.
# Для обхода блокировки по IP-адресу можно использовать прокси-серверы.
# Для этого в TelegramClient добавляем параметр proxy.
# Прокси-серверы можно найти в интернете, например, на сайте https://hidemy.name/ru/proxy-list/
# Пример использования прокси-сервера:
# proxy = ('socks5', 'proxy_host', proxy_port)
# async with TelegramClient('session_name', api_id, api_hash, proxy=proxy) as client:
#    ...
# После этого код будет использовать прокси-сервер для обхода блокировки по IP-адресу.
# После добавления прокси-сервера код будет выглядеть следующим образом:
#   async with TelegramClient('session_name', api_id, api_hash, proxy=proxy) as client:
#       for idx, channel in enumerate(channels, start=1):
#           try:
#               ... # Получение информации о канале
#               time.sleep(REQUEST_INTERVAL)  # Пауза для ограничения скорости запросов
#           except Exception as e:
#               print(f"Не удалось обработать {channel}: {e}")
#       ... # Запись в Excel
#       print("Данные успешно сохранены в файл telegram_infosecurity.xlsx")

import asyncio
import time
import os
import pandas as pd
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest

# Получаем API ID и HASH из переменных окружения
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')

# Проверяем, что значения были загружены
if not api_id or not api_hash:
    print(f"API ID или API HASH не найдены в переменных окружения. Убедитесь, что они заданы., {api_id}, {api_hash}")
    	

# Список Telegram-каналов
input_file = 'channels.txt'  # Файл с ссылками на каналы (по одной ссылке на строку)

# Считываем ссылки на каналы из файла
with open(input_file, 'r', encoding='utf-8') as file:
    channels = [line.strip() for line in file if line.strip()]

# Создаем пустой список для хранения данных
data = []

# Константы для ограничения запросов
REQUESTS_LIMIT = 10  # Лимит запросов в секунду
REQUEST_INTERVAL = 1 / REQUESTS_LIMIT  # Интервал между запросами

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        for idx, channel in enumerate(channels, start=1):
            try:
                # Получаем информацию об объекте
                entity = await client.get_entity(channel)

                # Определяем тип объекта
                type_ = "Канал" if getattr(entity, 'broadcast', False) else "Чат"

                # Получаем дополнительную информацию
                full_channel = await client(GetFullChannelRequest(entity))
                title = entity.title
                participants = full_channel.full_chat.participants_count
                about = full_channel.full_chat.about if full_channel.full_chat.about else "Описание отсутствует"

                # Сохраняем данные
                data.append({
                    "№": idx,  # Добавляем номер строки
                    "Название": title,
                    "Тип": type_,
                    "Подписчики": participants,
                    "URL": channel,
                    "Описание": about
                })
                print(f"№: {idx}, Название: {title}, Тип: {type_}, Подписчики: {participants}, URL: {channel}")
            except Exception as e:
                print(f"Не удалось обработать {channel}: {e}")

            # Пауза для ограничения скорости запросов
            time.sleep(REQUEST_INTERVAL)

    # Запись в Excel
    df = pd.DataFrame(data)
    df.to_excel("telegram_infosecurity.xlsx", index=False)
    print("Данные успешно сохранены в файл telegram_infosecurity.xlsx")

# Запуск программы
asyncio.run(main())
