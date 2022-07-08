from kafka import KafkaConsumer
import yaml

if __name__ == '__main__':

    with open("../../property.yaml") as f:
        load = yaml.safe_load(f)["KAFKA"]
    consumer = KafkaConsumer(load["TOPIC"], group_id=load["GROUP_ID"], bootstrap_servers=load["BOOTSTRAP_SERVERS"])
    for msg in consumer:
        result = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        print(result)
