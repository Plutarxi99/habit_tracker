FROM python:3.10-slim
LABEL name="Отслеживание привычек"
LABEL creator="Егор <plutarx> Шеванов"
LABEL version="1.0"
LABEL description="Это приложение создано \
для отслеживания и установки атомарных привычек."

WORKDIR /code
RUN pip install --upgrade pip
COPY ./requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . .

