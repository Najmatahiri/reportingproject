FROM python:3.12
RUN apt-get update && apt-get install -y cron
RUN apt-get install -y vim
WORKDIR /code
COPY ./requirements.txt .
RUN mkdir -p /code/python_package
COPY ./python_package/ /code/python_package/
#RUN pip3 install --no-index --find-links  /code/python_package/ -r ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN touch /var/log/cron.log

