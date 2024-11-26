from machines_available.machine_data import machine_data
from optimizer.optimization import optimize_production
import pandas as pd
from confluent_kafka import Consumer
import json

df_machines = pd.DataFrame(machine_data())
# Remove the machine with the capacity we are not going to optimize
df_machines = df_machines.dropna(subset=['capacity_per_hour'])

# df_orders = pd.read_csv('../new_orders/orders.csv')

c=Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
print('Kafka Consumer has been initiated...')

print('Available topics to consume: ', c.list_topics().topics)
c.subscribe(['sealing-planning'])

def main():

    message_count = 1

    orders_list = []
    while True:
        msg=c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue
        data=msg.value().decode('utf-8')
        
        data_dict = json.loads(data)
        
        
        orders_list.append(data_dict)
        
        message_count += 1     
        
        if message_count == 50:
            print("Handle the first 50 message to process the output.csv")
            df_orders = pd.DataFrame(orders_list)  
            df_result = optimize_production(df_machines, df_orders)
            df_result.to_csv('output.csv', index=False)
            message_count = 0
    c.close()
    


if __name__ == "__main__":
    main()
    