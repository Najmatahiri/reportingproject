FROM python:3.12

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV http_proxy http://tahirin:Nn2200011****@pxy-mcafee:8080
#ENV https_proxy http://tahirin:Nn2200011****@pxy-mcafee:8080


RUN apt-get update && apt-get install -y cron
RUN apt-get install -y vim
RUN apt-get install -y supervisor
# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#RUN mkdir -p $APP_HOME/python_package
#ADD ./python_package/ $APP_HOME/python_package/
#RUN pip3 install --no-index --find-links=$APP_HOME/python_package/ -r ./requirements.txt


RUN touch /var/log/cron.log

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

