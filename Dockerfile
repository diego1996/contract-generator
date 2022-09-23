FROM python:3.10
ENV PYTHONUNBUFFERED 1
ENV XDG_RUNTIME_DIR=/tmp
RUN apt update -y # && apt install -y wkhtmltopdf
RUN apt install xvfb xfonts-75dpi xfonts-base -y
RUN apt install -yqq --no-install-recommends \
        fontconfig libfreetype6 libxml2 libxslt1.1 libjpeg62-turbo zlib1g \
        libfreetype6 liblcms2-2 libtiff5 tk tcl libpq5 \
        libldap-2.4-2 libsasl2-2 libx11-6 libxext6 libxrender1 \
        locales-all \
        bzip2 ca-certificates curl gettext-base git gnupg2 nano \
        openssh-client telnet unzip xz-utils
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
RUN apt-get -f install && dpkg -i wkhtmltox_0.12.6.1-2.bullseye_amd64.deb
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app
COPY ./app-entrypoint.sh /app-entrypoint.sh
RUN sed -i 's/\r//' /app-entrypoint.sh
RUN chmod +x /app-entrypoint.sh
WORKDIR /app
