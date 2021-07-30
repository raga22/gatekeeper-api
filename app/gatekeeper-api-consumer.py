from kafka import KafkaConsumer
import psycopg2
import json
import consts


consumer = KafkaConsumer(
    'gatekeeper-event',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    group_id='gatekeeper',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Connect to an existing database
conn = psycopg2.connect("host=127.0.0.1 port=5432 dbname=blankspacedb user=admin password=admin123")
conn.autocommit = True
# Open a cursor to perform database operations
cur = conn.cursor()

def create_table(msg):
    collumn = ""
    for col in msg['collumns']:
        collumn += f'{col["name"]} {col["type"]},'

    create_tbl_query = f'CREATE TABLE {msg["table"]} ( { collumn[:-1] } )'

    cur.execute(create_tbl_query)
    print('create table success')
    insert_value(msg)


def alter_table(msg):
    print('alter table')


def insert_value(msg):
    col_name = ""
    col_val = ""
    for col in msg['collumns']:
        col_name += f'{col["name"]},'
        col_val += f'\'{col["value"]}\','
        
    insert_query = f" INSERT INTO {msg['table']} ({col_name[:-1]}) VALUES ({col_val[:-1]})"

    cur.execute(insert_query)
    print('insert success')


def delete_value(msg):
    where_str = ""
    for col in msg['collumns']:
        where_str += f' AND {col["name"]} = \'{col["value"]}\''
    delete_query = f"DELETE FROM {msg['table']} where 1=1 {where_str}"
    cur.execute(delete_query)
    print('delete success')


for message in consumer:
    #SELECT 1 FROM information_schema.tables WHERE
    cur.execute("select * from information_schema.tables where table_name=%s", (message.value['table'],))
    
    if message.value['operation'] == consts.INSERT:
        if bool(cur.rowcount):
            insert_value(message.value)
        else:
            create_table(message.value)
    elif message.value['operation'] == consts.DELETE:
        if bool(cur.rowcount):
            delete_value(message.value)

conn.commit()
conn.close()

#pep 8
# transaksi 
#verbose naming

# infrastruktur
# enginering mindset
# validasi, api, logging
# benchmarking