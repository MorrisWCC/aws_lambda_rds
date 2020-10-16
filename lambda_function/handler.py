import json
from datetime import datetime
import pymysql
import requests
import rds_config
from urllib.parse import unquote
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

rds_host = rds_config.db_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password,
                           db=db_name, connect_timeout=5,
                           cursorclass=pymysql.cursors.DictCursor)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    exit()

def search(event, context):
    logger.info(event['body'])
    post_body = json.loads(event['body'])
    country = post_body['country']

    sql = f"""
            SELECT * FROM `showInfo`.`showDetails`
            WHERE location like '%{country}%'
            OR  title like '%{country}%'
           """
    with conn.cursor() as cur:
        cur.execute(sql)
        records = cur.fetchall()

    rtn_data = []

    for record in records:
        tmp = {}
        tmp['title'] = record['title']
        tmp['startTime'] = datetime.strftime(record['startTime'], '%Y-%m-%d %H:%M:%S')
        tmp['endTime'] = datetime.strftime(record['endTime'], '%Y-%m-%d %H:%M:%S')
        tmp['location'] = record['location']
        tmp['locationName'] = record['locationName']
        tmp['price'] = record['price']

        rtn_data.append(tmp)

    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(rtn_data),
    }

    return response

