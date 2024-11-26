import json
import logging
import random
import time
import pandas as pd

from confluent_kafka import Producer
from faker import Faker

fake=Faker()

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

p=Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer has been initiated...')


def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)
        
def create_data():
    df_orders = pd.read_csv('./orders.csv').reset_index(drop=True)
    for index, row in df_orders.iterrows():
        row_dict = row.to_dict()
        
def main():
    df_orders = pd.read_csv('./orders.csv').reset_index(drop=True)
    for index, row in df_orders.iterrows():
        row_dict = row.to_dict()
        m = json.dumps(row_dict)
        p.poll(1)
        p.produce('sealing-planning', m.encode('utf-8'),callback=receipt)
        p.flush()
        time.sleep(1)


if __name__ == '__main__':
    main()