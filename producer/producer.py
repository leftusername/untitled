from kafka import KafkaProducer
import datetime
import time
import os
import logging


logging.basicConfig(filename='/tmp/producer.log',level=logging.INFO)
brocker_started=bool(False)
print(os.environ.get('KAFKA_SRVS'))
logging.info('KAFKA_SRVS='+os.environ.get('KAFKA_SRVS'))

while brocker_started != True:
    try:
        producer = KafkaProducer(bootstrap_servers=[os.environ.get('KAFKA_SRVS')],
                                 max_block_ms=600000)
#        producer = KafkaProducer(bootstrap_servers=[os.environ['kafka1']+'9092',os.environ['kafka2']+'9093',os.environ['kafka3']+'9094'])
    except:
        print("Brocker NOT available!" )
	
        logging.info('Brocker NOT available!')
#        logging.exception(str(e))
#        producer =''
        time.sleep(10)
    else:
        brocker_started=bool(True)



steps=100
topic='my-topic'
for i in range(steps):
    now = str(datetime.datetime.now())
    if i == 0:
        print("started: %s" % str(now))
        producer.send(topic, key=b'foo', value=b'===========Producer started============'+bytes(now, encoding='utf8'))
        logging.info(now+' ===========Producer started============')
    print(i)
    producer.send(topic, key=b'foo', value=bytes(now, encoding='utf8'))
    logging.info(now+' '+str(i))
    if i == steps-1:
        print("stopped: %s" % str(now))
        producer.send(topic, key=b'foo', value=b'===========Producer stopped============'+bytes(now, encoding='utf8'))
        logging.info(now + ' ===========Producer stopped============')
    time.sleep(1)





