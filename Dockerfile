# Используем базовый образ Python
FROM python:3

# Создаем директорию
RUN mkdir lms

# Устанавливаем рабочую директорию в контейнере
WORKDIR lms

# Копируем зависимости в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем код приложения в контейнер
COPY . .