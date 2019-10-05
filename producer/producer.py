from kafka import KafkaProducer
import datetime
import time


producer = KafkaProducer(bootstrap_servers=['172.17.0.1:9092'])
steps=100
topic='my-topic2'
for i in range(steps):
    now = str(datetime.datetime.now())
    if i == 0:
        print("started: %s" % str(now))
        producer.send(topic, key=b'foo', value=b'===========Producer started============'+bytes(now, encoding='utf8'))
    print(i)
    producer.send(topic, key=b'foo', value=bytes(now, encoding='utf8'))
    if i == steps-1:
        print("stopped: %s" % str(now))
        producer.send(topic, key=b'foo', value=b'===========Producer stopped============'+bytes(now, encoding='utf8'))
    time.sleep(1)




