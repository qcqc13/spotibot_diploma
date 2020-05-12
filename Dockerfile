# Используем базовый образ для нашего
FROM python:stretch

# Создаём директорию бота
RUN mkdir /spotify_bot

# Копируем все файлы из текущей директории в директорию бота
COPY . /spotify_bot

# Устанавливаем рабочую директорию
WORKDIR /spotify_bot

# Устанавливаем pytelegrambotapi и apiai
RUN pip3 install --no-cache-dir pytelegrambotapi
RUN pip3 install --no-cache-dir spotipy

# Указываем команды для выполнения после запуска контейнера
CMD ["python3", "bot.py"]

