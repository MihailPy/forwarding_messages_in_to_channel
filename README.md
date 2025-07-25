# README

## Описание проекта

Этот проект представляет собой Telegram-бота, который пересылает сообщения из указанных источников (чатов или каналов) в целевые каналы, используя две разные учетные записи Telegram. Проект основан на библиотеке Telethon и поддерживает параллельную работу нескольких аккаунтов.

## Основные возможности

- Пересылка сообщений из нескольких источников в целевые каналы
- Поддержка работы с двумя аккаунтами одновременно
- Фильтрация сообщений по типу (текст, медиа)
- Логирование операций
- Гибкая настройка через конфигурационный файл

## Структура проекта

```
forwarding_messages_in_to_channel/
├── .env.example          # Пример файла конфигурации
├── config.py             # Конфигурация фильтров и обработчиков
├── filters.py            # Фильтры для сообщений
├── handlers.py           # Обработчики сообщений
├── login.py              # Генератор сессионных строк
├── main.py               # Основной скрипт
├── requirements.txt      # Зависимости
└── utils/                # Вспомогательные модули
    ├── __init__.py
    ├── logger.py         # Логирование
    └── tools.py          # Вспомогательные функции
```

## Требования

- Python 3.7+
- Учетные записи Telegram с API-ключами
- Права на чтение в исходных чатах/каналах
- Права на запись в целевые каналы

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/MihailPy/forwarding_messages_in_to_channel.git
   cd forwarding_messages_in_to_channel
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Настройте конфигурацию:
   - Переименуйте `.env.example` в `.env`
   - Заполните все необходимые параметры

## Настройка

1. Получите сессионные строки:
   ```bash
   python login.py
   ```
   Скопируйте вывод в соответствующие переменные в `.env`.

2. Настройте параметры в `.env`:
   ```ini
   # API данные первого аккаунта
   api_id1=ВАШ_API_ID_1
   api_hash1=ВАШ_API_HASH_1
   string_session1=ВАША_СЕССИЯ_1

   # API данные второго аккаунта
   api_id2=ВАШ_API_ID_2
   api_hash2=ВАШ_API_HASH_2
   string_session2=ВАША_СЕССИЯ_2

   # ID целевых каналов
   my_channel1=ID_ЦЕЛЕВОГО_КАНАЛА_1
   my_channel2=ID_ЦЕЛЕВОГО_КАНАЛА_2

   # ID исходных чатов (через запятую)
   sources_of_messages1=ID_ИСТОЧНИКА_1,ID_ИСТОЧНИКА_2
   sources_of_messages2=ID_ИСТОЧНИКА_3,ID_ИСТОЧНИКА_4
   ```

3. Настройте фильтры и обработчики в `config.py`:
   ```python
   FILTERS = {
       'text': True,      # Пересылать текстовые сообщения
       'media': True,     # Пересылать медиа-сообщения
       'max_length': 500, # Максимальная длина текста
   }
   ```

## Запуск

```bash
python main.py
```

## Дополнительные возможности

1. **Фильтрация сообщений**:
   - По типу (текст/медиа)
   - По длине текста
   - По ключевым словам (можно настроить в `filters.py`)

2. **Логирование**:
   - Все операции логируются в консоль
   - Можно настроить запись логов в файл через `utils/logger.py`

3. **Расширение функционала**:
   - Добавление новых обработчиков в `handlers.py`
   - Создание дополнительных фильтров в `filters.py`

## Лицензия

MIT License
