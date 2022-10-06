FROM python:3.10

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV DEV 1

RUN apt-get update -y
RUN apt-get install -y nginx systemctl

COPY ./matchmaker.service /etc/systemd/system/matchmaker.service
RUN mkdir -p /var/www/matchmaker/html

WORKDIR /usr/src/matchmaker

COPY ./matchmaker /etc/nginx/sites-available
RUN ln -s /etc/nginx/sites-available/matchmaker /etc/nginx/sites-enabled/

ENV MATCHMAKER_TESTING 0
ENV MATCHMAKER_DEBUG 0
ENV MATCHMAKER_SECRET_KEY 0
ENV MATCHMAKER_HASURA_ADMIN_SECRET password
ENV MATCHMAKER_HASURA_URL url.to.hasura
ENV MATCHMAKER_DOMAIN url.to.this.service

COPY ./nginx_conf_fix.sh ./
RUN chmod +x ./nginx_conf_fix.sh
RUN ./nginx_conf_fix.sh
RUN rm ./nginx_conf_fix.sh

COPY ./matchmaker-*-py3-none-any.whl /usr/src/matchmaker
RUN pip install --upgrade pip
RUN pip install ./matchmaker-*-py3-none-any.whl
RUN rm ./matchmaker-*-py3-none-any.whl

RUN chown www-data:www-data /usr/local/lib/python3.*/site-packages/matchmaker

RUN systemctl enable matchmaker
RUN systemctl enable nginx

CMD ["systemctl", "start", "matchmaker", "nginx"]