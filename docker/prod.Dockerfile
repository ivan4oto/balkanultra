# This docker file is used for local development via docker-compose
# Creating image based on official python3 image
FROM python:3.10.8

# Fix python printing
ENV PYTHONUNBUFFERED 1

# Installing all python dependencies
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy environment variables, export them and delete file
COPY docker/env.list /tmp/env.list
RUN export $(grep -v '^#' /tmp/env.list | xargs) && \
    echo "export $(grep -v '^#' /tmp/env.list | xargs)" > /etc/profile.d/env.sh && \
    rm /tmp/env.list

# Get the django project into the docker container
COPY docker/entrypoint.sh /entrypoint.sh
RUN mkdir /balkan-app
WORKDIR /balkan-app
ADD ./ /balkan-app/

EXPOSE 8000
CMD ["gunicorn", "balkanultra.wsgi:application", "--bind" ,"0.0.0.0:8000", "--workers", "3", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-"]


