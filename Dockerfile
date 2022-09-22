FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app/contracts
RUN apt update -y && apt install -y wkhtmltopdf
COPY requirements.txt /app/contracts/
RUN pip install -r requirements.txt
COPY . /app/contracts/
COPY ./app-entrypoint.sh /app-entrypoint.sh
RUN sed -i 's/\r//' /app-entrypoint.sh
RUN chmod +x /app-entrypoint.sh
CMD /app-entrypoint.sh

