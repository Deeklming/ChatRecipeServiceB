FROM python:3.11

WORKDIR /app

COPY . /app
# COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]
