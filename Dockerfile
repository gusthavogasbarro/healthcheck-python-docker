FROM python:3
COPY . /app
RUN pip3 install flask && pip3 install mysql-connector-python && pip3 install redis && pip3 install flask-redis && pip3 install flask-mysql && pip3 install boto3
WORKDIR /app
CMD python3 app.py
EXPOSE 5000