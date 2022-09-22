FROM python:3.10
ENV PYTHONUNBUFFERED 1
# RUN apt update -y && apt install -y wkhtmltopdf
RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y wget
RUN apt-get install -y openssl build-essential
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvJf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN cp wkhtmltox/bin/wkhtmlto* /usr/bin/
#
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app
COPY ./app-entrypoint.sh /app-entrypoint.sh
RUN sed -i 's/\r//' /app-entrypoint.sh
RUN chmod +x /app-entrypoint.sh
WORKDIR /app
