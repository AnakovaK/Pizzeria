# Pizzeria Silver


### Описание проекта

Сайт ресторана-пиццерии с возможностью заказать доставку на дом.
Покупатель добавляет товары из большого ассортимента в корзину из меню.
Меню сайта улучшено фильтрами, для быстрого поиска по начинке. 
Также при покупке и оформлении заказа начисляются баллы ресторана.

### Технологический стек:
- Python 3.8
- Django 4

### Функционал:
- Регистрация (при желании пользователя)
- Авторизация
- Полноценное меню с выбором пиццы, которую можно добавить в корзину покупок
- Фильтры для вышеупомянутого меню
- Подсчет общей суммы покупки и бонусных баллов за нее
- Выбор метода оплаты при подтверждении заказа

### Инструкция по настройке проекта:
Самый удобный для запуска проекта - PyCharm. Можно запустить на ОС Windows или Linux.

1. Склонировать проект
2. Открыть проект в PyCharm с наcтройками по умолчанию
3. Создать виртуальное окружение (через settings -> project "Pizzeria" -> project interpreter)
4. Открыть терминал в PyCharm, проверить, что виртуальное окружение активировано.
5. Обновить pip:
   ```bash
   pip install --upgrade pip
   ```
6. Установить в виртуальное окружение необходимые пакеты: 
   ```bash
   pip install -r requirements.txt
   ```

7. Синхронизировать структуру базы данных с моделями: 
   ```bash
   python manage.py migrate
   ```

8. Создать суперпользователя
   ```bash
   python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('vasya', 'abc@123.net', 'pizzaproga')"
   ```

9. Создать конфигурацию запуска в PyCharm (файл `manage.py`, опция `runserver`)
