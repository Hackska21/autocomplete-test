FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . /src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

