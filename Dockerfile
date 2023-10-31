FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]
