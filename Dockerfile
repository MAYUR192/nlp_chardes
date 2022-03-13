FROM python:3.6

RUN pip install --upgrade pip==19.3
RUN pip --version

RUN apt-get update
RUN apt-get install -y gettext-base

ENV DEBIAN_FRONTEND noninteractive


ARG PORT
ENV PORT $PORT
RUN echo "Selected port: $PORT"

RUN apt-get update
RUN apt-get install -y nginx gunicorn supervisor ffmpeg

RUN mkdir -p /deploy
COPY . /deploy
COPY docker-entrypoint.sh /
RUN pip install -r /deploy/requirements.txt
RUN mkdir -p /etc/nginx/sites-enabled
RUN rm -rf /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-enabled/flask_test.conf
COPY flask.conf /etc/nginx/sites-enabled/
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf


# Setup supervisord
RUN mkdir -p /var/log/supervisor && touch /var/log/supervisor/error.log && touch /var/log/supervisor/access.log
RUN chmod 755 /var/log/supervisor 

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# Start processes
CMD ["/usr/bin/supervisord"] 

