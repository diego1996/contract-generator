FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV XDG_RUNTIME_DIR=/tmp
RUN apt update -y # && apt install -y wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN dpkg -i apt-get -f install && wkhtmltox_0.12.6-1.buster_amd64.deb
#
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app
COPY ./app-entrypoint.sh /app-entrypoint.sh
RUN sed -i 's/\r//' /app-entrypoint.sh
RUN chmod +x /app-entrypoint.sh
WORKDIR /app
