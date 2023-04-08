#!/bin/sh
# A script to start postgres development database

docker build -t my-postgres-db ./
docker run -d --name my-postgresdb-container -p 5432:5432 my-postgres-db