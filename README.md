# forwarding_messages_in_to_channel

## Что делает проект

Проект пересылает новые сообщения из заданных Telegram-источников в целевые каналы.
Поддерживается несколько аккаунтов Telegram одновременно: для каждого аккаунта задаются
свои источники и свой целевой канал.

Технологии:

- Python
- Telethon
- Typer CLI
- Pytest

## Как установить

1. Клонировать репозиторий:

```bash
git clone https://github.com/MihailPy/forwarding_messages_in_to_channel.git
cd forwarding_messages_in_to_channel
```

1. Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
source .venv/bin/activate
```

1. Установить зависимости:

```bash
pip install -r requirements.txt
```

1. Подготовить `.env`:

```bash
cp .env.example .env
```

1. Подготовить `accounts.json`:

```bash
cp accounts.example.json accounts.json
```

## Как настроить

Конфиг хранится в двух местах:

- `.env` для секретов (`API_ID`, `API_HASH`, `STRING_SESSION`)
- `accounts.json` для структуры аккаунтов, источников и целевых каналов

Базовый поток настройки:

1. Добавить аккаунт через CLI (`add-account`)
2. Получить `string session` для аккаунта (`login --save`)
3. Добавить источники (`add-source`)
4. Проверить конфиг (`check`)

## Как получить session

Через CLI для конкретного аккаунта:

```bash
python cli.py login <account_name> --save
```

Команда авторизует аккаунт и сохранит строку сессии в `.env` в переменную
`<ACCOUNT_NAME>_STRING_SESSION`.

## Как добавить аккаунт

Запустить интерактивную команду:

```bash
python cli.py add-account
```

Она:

- запросит имя аккаунта, `API ID`, `API Hash`, целевой канал
- создаст запись в `accounts.json`
- сохранит `API_ID` и `API_HASH` в `.env`

После этого нужно получить сессию:

```bash
python cli.py login <account_name> --save
```

## Как проверить конфиг

Проверка доступности источников/цели и авторизации каждого аккаунта:

```bash
python cli.py check
```

Команда валидирует:

- наличие обязательных env-переменных
- корректность `string session`
- доступ к источникам
- возможность писать в целевой канал

## Как запустить

Запуск форвардинга:

```bash
python main.py
```

Процесс поднимет клиента(ов) и будет слушать новые сообщения до остановки.

## Quality checks

```bash
uv run ruff check .
uv run pyright
uv run pytest
```

## Makefile

Для удобства те же проверки вынесены в `Makefile`:

```bash
make lint
make typecheck
make test
make check
```

## Тесты

Тесты лежат в `tests/` и запускаются через `pytest`.

Покрыты:

- поиск аккаунтов в конфиге через `services/config_storage.py`
- нормализация ввода каналов и чатов
- базовая валидация `accounts.json` и `STRING_SESSION` в `config.py`

## Архитектура

Текущая структура:

```text
.
├── main.py                  # Точка входа: запуск всех клиентов
├── cli.py                   # CLI для управления аккаунтами и валидации
├── config.py                # Загрузка/проверка accounts.json и .env
├── accounts.example.json    # Пример структуры accounts.json
├── models/
│   └── account.py           # Модель AccountConfig
├── services/
│   ├── config_storage.py    # Чтение/запись accounts.json для CLI
│   ├── forwarder.py         # Логика пересылки сообщений
│   └── validation.py        # Проверка прав, источников, целей
├── tests/
│   ├── test_config.py          # Тесты загрузки и валидации конфига
│   └── test_config_storage.py  # Тесты CLI-хранилища accounts.json
└── utils/
    └── logger.py            # Логирование
```

Поток выполнения:

1. `services/config_storage.py` читает и обновляет `accounts.json` для CLI-команд.
2. `config.py` загружает аккаунты и секреты для запуска приложения.
3. `main.py` создаёт Telethon-клиенты для всех аккаунтов.
4. `services/forwarder.py` подписывается на `NewMessage` из `sources`.
5. Новые сообщения пересылаются в `target_channel`.

## Безопасность секретов

- Не коммитить `.env` и `accounts.json` в публичный репозиторий.
- Использовать отдельные Telegram-аккаунты для форвардинга, не личные.
- Минимизировать права аккаунтов: только нужные чаты/каналы.
- Регулярно ротировать `API_HASH`/сессии при подозрении на утечку.
- Никогда не публиковать `STRING_SESSION` в логах, чатах и issue.
- Для продакшн-деплоя хранить секреты
в менеджере секретов или переменных окружения CI/CD.
