FROM python:3.8

ARG PORT=8080

ENV PORT=${PORT}
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY .pre-commit-config.yaml .
RUN git init . && pre-commit install-hooks

COPY worship_ppt/ /worship_ppt
WORKDIR /worship_ppt
RUN python3 -m pytest

CMD gunicorn --bind :$PORT --reload --capture-output --enable-stdio-inheritance --workers 1 --threads 8 "worship_ppt.app:create_app()";
