from kafka import KafkaConsumer
import datetime

now=datetime.datetime.now()
print ("Consumer started: %s" % str(now))

# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('my-topic2',
                         group_id='my-group'+str(now),
                         bootstrap_servers=['172.17.0.1:9092'],
                         auto_offset_reset='earliest',
                         enable_auto_commit=False)
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
