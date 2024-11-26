from confluent_kafka import Consumer
import json
import pandas as pd

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
print('Kafka Consumer has been initiated...')

print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['sealing-planning'])

def main():
    count_m = 1
    lista = []
    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        
        data_dict = json.loads(data)
        
        
        lista.append(data_dict)
        
        count_m += 1
        
        print(lista)        
        
        if count_m == 50:
            df_orders = pd.DataFrame(lista) 
             
        
            print(df_orders)
    c.close()
        
if __name__ == '__main__':
    main()