# Pull base image
FROM python:3.12

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV http_proxy 'http://tahirin:Nn2200011****@pxy-mcafee:8080'
ENV https_proxy 'http://tahirin:Nn2200011****@pxy-mcafee:8080'
WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

CMD [ "python3", "/code/manage.py", "runserver", "0.0.0.0:8000"]