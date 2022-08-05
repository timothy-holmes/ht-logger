FROM python:latest

# construct working directory in container
WORKDIR /srv/ht-tracker

# copy git repo to workdir
COPY . ./

# backup database
# COPY ./data/database.db ./data/backup/database-$(date +%Y%m%d%H%M%S).db

# (maybe) display contents of workdir for debugging purposes
RUN ls -R

# get list of dependencies
# RUN pip3 install pipreqs
# RUN pipreqs --force

# install dependencies
RUN pip3 install -r requirements.txt

# TODO: install test dependecies and run tests
