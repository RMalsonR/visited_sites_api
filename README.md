# visited_sites_api
Первоначальная настройка:  
* Должен быть установлен Redis
* Миграции  
``
python migrate.py
``  
* Установка всех необходимых пакетов  
``pip install -r requirements.txt``
* Установить необходимые значения `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB_INDEX`  
 в `visited_sites_api/settings.py`    
 
 Формат даты для `GET` запроса: `YYYY-mm-dd`  
 Запуск тестов: `python manage.py test`

