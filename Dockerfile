##
## Dockerfile to generate a Docker image from a GeoDjango project
##

## Start from an existing image with Miniconda installed
FROM continuumio/miniconda3

MAINTAINER Mark Foley

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=awm2023_tutorial.settings

## Ensure that everything is up-to-date
RUN apt-get -y update && apt-get -y upgrade
RUN conda update -n base conda && conda update -n base --all

## Make a working directory in the image and set it as working dir.
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

## UPDATE: these are not necessary as conda gets whatever it needs anyway.
## Get the following libraries. We can install them "globally" on the image as it will contain only our project

#RUN apt-get -y install build-essential python-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

## You should have already exported your conda environment to an "ENV.yml" file.
## Now copy this to the image and install everything in it. Make sure to install a WSGI server - it may not be in the source
## environment.
COPY ENV.yml /usr/src/app
RUN conda env create -n awm2023_tutorial --file ENV.yml

## Make RUN commands use the new environment
## See https://pythonspeed.com/articles/activate-conda-dockerfile/ for explanation
RUN echo "conda activate awm2023_tutorial" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

## Set up conda to match our test environment
RUN conda config --add channels conda-forge && conda config --set channel_priority strict
RUN cat ~/.condarc

## Install the appropriate WSGI server. If ccoming from Linux or Macc, this will probably be already there. If coming
## from MS Windows, you'll need to install it here.

#RUN conda install uwsgi
RUN conda install gunicorn

## Copy everything in your Django project to the image and display a directory listing.
COPY . /usr/src/app
RUN ls -la

## Make sure that static files are up to date and available.
RUN python manage.py collectstatic --no-input

## Expose port on the image. We'll map a localhost port to this later. You can change this if desired.
EXPOSE 8002

## Run a WSGI server - "uwsgi" or "gunicorn". uWSGI is a Web Server Gateway Interface (WSGI) server implementation
## that is typically used to run Python web applications. Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.
## It is an alternative to uWSGI.

#CMD uwsgi --ini uwsgi.ini
CMD gunicorn awm2023_tutorial.wsgi --config gunicorn.conf.py