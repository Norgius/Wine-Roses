# Новое русское вино

Сайт магазина авторского вина "Новое русское вино".

## Запуск

- Скачайте код
- Для запуска установите виртуальное окружение и библиотеки из файла `requirements.txt`.
```
$ python3.10 -m venv env

$ . ./env/bin/activate

$ pip install -r requirements.txt
```
- Запускать сайт из командной строки, находясь в корневой директории сайта.
```
$ python main.py
```
- Перейдите на сайт по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Работа с сайтом
Для изменения данных о винах в директорию `wine_data/` необходимо поместить файл с обновленными данными в формате Excel-таблицы.

Файл должен иметь имя вида `wine.xlsx`. Допускается хранить несколько файлов `wine2.xlsx`, `wine3.xlsx`. Будет выбираться всегда файл с большим порядковым номером в названии.

Файл должен содержать заголовки `Категория, Название, Сорт, Цена, Картинка, Акция`.

В качестве примера в `wine_data/` лежит файл `wine.xlsx`.

Картинки загружать в директорию `images/`.