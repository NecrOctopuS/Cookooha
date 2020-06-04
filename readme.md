# Cookooha

Сайт на Flask.
Пример можно посмотреть на [Heroku](https://demo-tutors-finder-with-db.herokuapp.com/).

## Запуск

Для запуска сайта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите команды для базы данных
```
flask db upgrade
python3 add_data.py
```
- Запустите сервер командой `flask run`

После этого переходите по ссылке [127.0.0.1:5000](http://127.0.0.1:5000), вы увидите главную страницу.

Либо задеплойте его на [Heroku](https://heroku.com/).

В файле `.env` или в настройках окружения создайте следующие переменные:
```
SECRET_KEY='my-super-secret-phrase-I-dont-tell-this-to-nobody' #Секретный ключ проекта
RECIPES_PER_MAIN_PAGE=6 #Количество карточек на главной странице
```


## Особенности

Изначальные данные находятся в файлах
```
recipes.json
ingredients.json
ingredient_groups.json
```
Их можно записать в базу данных запустив скрипт командой `python3 add_data.py`.

## Цели проекта

Код написан в учебных целях — это проектное задание четвертой недели в курсе по Flask на сайте [Stepik](https://stepik.org/).