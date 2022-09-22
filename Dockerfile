FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV XDG_RUNTIME_DIR=/tmp
RUN apt update -y && apt install -y wkhtmltopdf
#
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app
COPY ./app-entrypoint.sh /app-entrypoint.sh
RUN sed -i 's/\r//' /app-entrypoint.sh
RUN chmod +x /app-entrypoint.sh
WORKDIR /app
