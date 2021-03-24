FROM python:3.8

ARG PORT=8080

# Local Docker 8080
#              8000
ENV PORT=${PORT}

COPY requirements.txt /
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
  apt-get -y update && \
  apt-get install -y google-chrome-stable && \
  pip install -r requirements.txt

COPY worship_ppt/ /worship_ppt

CMD gunicorn --bind :$PORT --workers 1 --threads 8 "worship_ppt.app:create_app()";
