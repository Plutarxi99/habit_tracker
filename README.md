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
|     **DATABASE_LOGIN**| <pre><code>'{"ENGINE": "django.db.backends.postgresql","NAME": "django_proj_educ","USER": "postgres",}'</code></pre> |     словарь для подключения к базе данных. P.S. не забудь создать ее|
|     **SECRET_KEY**| django-insecure-hu213gr51uh234gbrtf34oqufg35835g3q5g       |     код генерируется автоматически при создании приложения|
|     **SUPERUSER_EMAIL**| email_superuser       |     установить почту суперюзера|
|     **SUPERUSER_PASSWORD**| password_superuser       |     установить пароль суперюзера|
|     **USER_PASSWORD**| password_user       |     установить пароль юзера|
|     **TELEGRAM_TOKEN**| 1234567899:QWERTYUIOPSSDFGHJKLZXCVBNM<>QWERTYU         |     телеграмм токен полученный от Bot_Father|
|     **CELERY_BROKER_URL**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для работы celery|
|     **CELERY_RESULT_BACKEND**| <pre><code>redis://127.0.0.1:6379</code></pre>    |     база данных для работы celery|
|     **CHAT_ID_TG_TEST**| 123456789   |     получение chat id пользователя для работы кастомной команды проверки бота|
</details>

<details>

<summary>Как использовать?</summary>

* После установки нужных настроук в файле **<.env>**. Надо выполнить команду для установки пакетов:
  <pre><code>pip install -r requirements.txt </code></pre>

* Создать суперюзера:
  <pre><code>python3 manage.py ccsu</code></pre>

* Для запуска работы celery worker:
  <pre><code>python3 manage.py celery_worker</code></pre>

* Для запуска работы celery beat:
  <pre><code>celery -A config beat -l INFO</code></pre>


</details>
