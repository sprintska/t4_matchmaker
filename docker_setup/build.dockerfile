FROM python:3.10

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1
ENV DEV 1

ENV MATCHMAKER_TESTING 0
ENV MATCHMAKER_DEBUG 0
ENV MATCHMAKER_SECRET_KEY 0
ENV MATCHMAKER_HASURA_AUTH_KEY 0
ENV MATCHMAKER_HASURA_URL hasura.dev.advancedtransponder.net
ENV MATCHMAKER_DOMAIN matchmaker.advancedtransponder.net

# If DEV:
# this server's URL = matchmaker.advancedtransponder.net
# hasura URL = hasura.advancedtransponder.net

# If PROD:
# this server's URL = matchmaker.tabletoptournament.tools
# hasura URL = graphql-engine.tabletoptournament.tools

RUN apt-get update -y
RUN apt-get install -y nginx systemctl

COPY ./matchmaker.service /etc/systemd/system/matchmaker.service
RUN mkdir -p /var/www/matchmaker/html

WORKDIR /usr/src/matchmaker

COPY ./matchmaker /etc/nginx/sites-available
RUN ln -s /etc/nginx/sites-available/matchmaker /etc/nginx/sites-enabled/

COPY ./nginx_conf_fix.sh ./
RUN chmod +x ./nginx_conf_fix.sh
RUN ./nginx_conf_fix.sh
RUN rm ./nginx_conf_fix.sh

COPY ./matchmaker-0.1.2-py3-none-any.whl /usr/src/matchmaker
RUN pip install --upgrade pip
RUN pip install ./matchmaker-0.1.2-py3-none-any.whl
RUN rm ./matchmaker-0.1.2-py3-none-any.whl

RUN chown www-data:www-data /usr/local/lib/python3.*/site-packages/matchmaker

RUN systemctl enable matchmaker
RUN systemctl enable nginx

CMD ["systemctl", "start", "matchmaker", "nginx"]