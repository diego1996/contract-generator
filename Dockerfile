FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN apt update -y && apt install -y wkhtmltopdf
#
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app
COPY ./app-entrypoint.sh /app-entrypoint.sh
RUN sed -i 's/\r//' /app-entrypoint.sh
RUN chmod +x /app-entrypoint.sh
WORKDIR /app
