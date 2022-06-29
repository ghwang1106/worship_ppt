FROM python:3.8 as base

ARG PORT=8080

ENV PORT=${PORT}
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /worship
RUN cd worship && python3 -m pytest

FROM base as image-dev

CMD FLASK_ENV=development FLASK_APP="worship.app:create_app()" FLASK_RUN_PORT=$PORT flask run --host=0.0.0.0

FROM base as image-prod

CMD gunicorn --bind :$PORT --reload --capture-output --enable-stdio-inheritance --workers 1 --threads 8 "worship.app:create_app()";
