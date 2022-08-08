FROM postgres
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB balkanultra
COPY balkanultra.sql /docker-entrypoint-initdb.d/