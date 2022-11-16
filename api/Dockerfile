FROM python:3.9

WORKDIR /code

COPY ./requirements.prod.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

CMD ["python", "main.py"]
