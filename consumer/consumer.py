from kafka import KafkaConsumer
import datetime
import time
import logging
import os

logging.basicConfig(filename='/tmp/consumer.log',level=logging.INFO)

now=datetime.datetime.now()
print ("Consumer started: %s" % str(now))
logging.info('KAFKA_SRVS='+os.environ.get('KAFKA_SRVS'))
logging.info("Consumer started: %s" % str(now))
brocker_started=bool(False)

while brocker_started != True:
    try:
        consumer = KafkaConsumer('my-topic',
                                 group_id='my-group'+str(now),
                                 bootstrap_servers=[os.environ.get('KAFKA_SRVS')],
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False)
    except Exception as e:
        print("Brocker NOT started!")
        logging.info("Brocker NOT started!" )
        print(str(e))
        time.sleep(5)
    else:
        brocker_started=bool(True)


for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
    logging.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                message.offset, message.key,
                                                message.value))

