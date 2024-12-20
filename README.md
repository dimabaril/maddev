# maddev

## Описание

Реализация разбивки сообщений на фрагменты заданной длины.

## Содержимое репозитория

- `services/`
  - `msg_split.py`: Основной модуль, содержащий функции для разбивки сообщений на фрагменты.
- `sources/`
  - `source.html`: Пример HTML-файла для тестирования.
  - `source_no_tags.html`: Пример текстового файла без тегов для тестирования.
  - `source_my.html`: Пример HTML-файла для тестирования.
- `tests/`
  - `test_msg_split.py`: Тесты для функций из `msg_split.py`.
- `split_msg.py`: Основной скрипт для разбивки сообщений на фрагменты.
- `pyproject.toml`: Конфигурационный файл для управления зависимостями с помощью Poetry.
- `poetry.lock`: Файл блокировки зависимостей, созданный Poetry.
- `README.md`: Описание проекта.

## Развертывание и запуск

### Требования

- Python 3.13
- Poetry

Если Poetry еще не установлен, вы можете установить его, следуя инструкциям на [официальном сайте Poetry](https://python-poetry.org/docs/#installation). Либо можно воспользоваться pip.

### Установка зависимостей

1. Клонируйте репозиторий:

```sh
git clone https://github.com/dimabaril/maddev.git
cd maddev
```

2. Установите зависимости:

```sh
poetry install
```

В качестве альтернативы можете использовать

```sh
pip instal -r requirements.txt
```

### Запуск основного скрипта:

1. Активируйте виртуальное окружение:

```sh
poetry shell
```

2. Пример вызова скрипта:

```sh
python split_msg.py --max_len=4296 sources/source.html
```

### Запуск тестов

Для запуска тестов используйте следующую команду:
(виртуальное окружение активировано)

```sh
pytest
```

### Контакты

Автор: Dmitrii Barilkin  
Email: dimabaril@gmail.com
