from flask import Flask, redirect, render_template, request, url_for, jsonify 
import mysql.connector, os, redis, boto3
from mysql.connector import Error
from flaskext.mysql import MySQL

app = Flask(__name__)
@app.route('/healthcheck')
def healthcheck():
    api = versaoAPI()
    serv = services()
    return jsonify(api, serv)

def services():
    mysql = connectMSQL()
    nosql = connectNoSQL()
    fila = connectFila()
    sts = status()
    return(mysql, nosql, fila, sts)

def versaoAPI():
    versao = 'API: 1.0'
    return (versao)

def status():
    statusDeAcesso = 'Status 200'
    return(statusDeAcesso)

def connectMSQL():
    conn = None
    try:
        conn = mysql.connector.connect(host=os.getenv('MYSQL_IP'), database=os.getenv('MYSQL_DATABASE'), user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'))
        if conn.is_connected():
            return ('MySQL: OK')
    except:
        return ('MySQL: ERRO')
    

def connectNoSQL():
    conn = None
    try:
        conn = redis.StrictRedis(host=os.getenv('REDIS_IP'), port=os.getenv('REDIS_PORT'), password='')
        if conn.ping() == True:
            return ('NoSQL: Ok')
    except:
        return('NoSQL: ERRO')

def connectFila():
    try:
        conn = boto3.client('sqs', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), aws_secret_access_key=os.getenv('AWS_SECRET_KEY'), region_name=os.getenv('AWS_DEFAULT_REGION'))
        Url = conn.get_queue_url(QueueName=os.getenv('nome_fila'))
        MetaData = Url['ResponseMetadata']
        StatusCode = MetaData['HTTPStatusCode']
        Status = 'Fila: {}'.format(StatusCode)
        return('Fila: OK')
    except:
        return('Fila: Erro')

if __name__ == '__main__':
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT',5000))
    app.debug = True
    app.run(host=host, port=port)
