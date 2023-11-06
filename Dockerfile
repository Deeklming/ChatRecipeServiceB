FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 80

CMD ["python3", "main.py"]
