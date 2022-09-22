FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app/contracts
RUN apt update -y && apt install -y wkhtmltopdf
COPY requirements.txt /app/contracts/
RUN pip install -r requirements.txt
COPY . /app/contracts/
CMD sh app-entrypoint.sh

