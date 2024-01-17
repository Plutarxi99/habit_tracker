# Habit tracker
Приложение создаёт привычки и отправляет уведомление об их начале в диалог с ботом в телеграмме.

> [!NOTE]
> Формат уведомлений: "Я буду [действие] в [начало действия] в течении [время действия] в [место действия]"

<details>

<summary>Данный проект содержит в себе 2 приложения:</summary>

* **habit**
   - позволяет работать с привычками
       - содержит модели Habit
* **users**
   - служит для аунтификации пользователя 
       - содержит модели User 
</details>

<details>

<summary>Что делает приложение?</summary>
Функционал:

* Регистрация пользователя, получение токена и использование в запросах
* Можно добавлять, изменять, смотреть и удалять привычки.
* Только создатель привычки может изменять и удалять привыки.
* Имеется список публичных привычек. Их могут смотреть все.
* Подключена докуменация и swagger для работы через браузер.
* Создание переодической и отложенной задачи на рассылку уведомлений.
* Гибкий график отправки уведомлений от каждоый минуты до 1 раза в неделю.
</details>

> [!IMPORTANT]
> Добавлен файл https://github.com/Plutarxi99/mailing_list/blob/main/.env.sample (для использования надо привести к ввиду **<.env>**) с помощью, которого можно настроить работу проекта. В нем лежат настройки (далее идут примеры заполнения полей):
<details>
<summary>Настройки, которые надо установить для работы приложения</summary>

| Значение | Содержание | Примечание |
|-----|-----------|-----:|
|     **SECRET_KEY**| django-insecure-hu213gr51uh234gbrtf34oqufg35835g3q5g       |     код генерируется автоматически при создании приложения|
|     **POSTGRES_DB**| NAME_BD   |     название базы данных |
|     **POSTGRES_USER**| USER_BD   |     название пользователя базы данных |
|     **POSTGRES_PASSWORD**| PASSWORD_BD   |     пароль базы данных |
|     **POSTGRES_HOST**| HOST_BD   |     название твоего сервиса используемый для контейнеризации |
|     **SUPERUSER_EMAIL**| email_superuser       |     установить почту суперюзера|
|     **SUPERUSER_PASSWORD**| password_superuser       |     установить пароль суперюзера|
|     **USER_PASSWORD**| password_user       |     установить пароль юзера|
|     **TELEGRAM_TOKEN**| 1234567899:QWERTYUIOPSSDFGHJKLZXCVBNM<>QWERTYU         |     телеграмм токен полученный от Bot_Father|
|     **CELERY_BROKER_URL_LOCAL**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для работы celery|
|     **CELERY_RESULT_BACKEND_LOCAL**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для работы celery|
|     **CELERY_BROKER_URL_DOCKER**| <pre><code>redis://redis:6379</code></pre>    |     база данных для работы celery в контейнере|
|     **CELERY_RESULT_BACKEND_DOCKER**| <pre><code>redis://redis:6379</code></pre>    |     база данных для работы celery в контейнере|
|     **CHAT_ID_TG_TEST**| 123456789   |     получение chat id пользователя для работы кастомной команды проверки бота|
|     **ENV_TYPE**| local/server   |     для использования разных настроек для запуска локально-local для запуска с сервера-server |
|     **HOST_IP**| 0.0.0.0   |     id- адрес твоего сервера базы данных |
</details>

<details>

<summary>Как использовать?</summary>

* После установки нужных настроук в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Применить миграции:
  <pre><code>python3 manage.py migrate</code></pre>

* Создать суперюзера:
  <pre><code>python3 manage.py ccsu</code></pre>

* Для запуска работы celery worker:
  <pre><code>python3 manage.py celery_worker</code></pre>

* Для запуска работы celery beat:
  <pre><code>celery -A config beat -l INFO</code></pre>


</details>

<details>

<summary>Что использовалось в приложение?</summary>
Функционал:

* Подключено rest_framework для использоваеть API приложения
* Подключено rest_framework_simplejwt для использоваеть API приложения авторизации пользователя Bearer token
* Подключено drf_yasg для создания автоматической документации и возможность работать в браузере с приложением
* Подключено django_filters для использоваеть API приложения в публичных привычках филтрации по приятным привычкам и по дате начало привычек
* Подключена django_celery_beat для использования и создание переодической задачи
* Подключена django_celery для создание и использование отложенной задачи
* Обложил тестами CRUD привычек.
</details>

<details>

<summary>Запуск приложения на удаленном сервере из docker</summary>

* Переходим в папку где будет лежать код:
  <pre><code>cd /var/www/html/</code></pre>

* Копируем код с git:
  <pre><code>git clone <URL on GIT></code></pre>
  
* Копируем .env файл свои значения переменных и поменять в файле проекта deploy/habit_tracker: server_name <HOST_IP>;


* Далее выполнить bash команда на установку нужных компанентов и копирование настроек сайта для его работы:
  <pre><code>cd /var/www/html/habit_tracker/deploy/</code></pre>
  <pre><code>sh deploy_bash.sh</code></pre>

* Создаем виртуальное окружение:
  <pre><code>python3 -m venv env</code></pre>
  <pre><code>source env/bin/activate</code></pre>

* Создаем контейнер:
  <pre><code>docker-compose build</code></pre>
  
* Поднимаем контейнер в фоновом режиме:
  <pre><code>docker-compose up -d</code></pre>


</details>
