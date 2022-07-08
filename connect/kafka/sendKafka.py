import json
from kafka import KafkaProducer
import yaml

if __name__ == '__main__':
    with open("../../property.yaml") as f:
        load = yaml.safe_load(f)["KAFKA"]

    producer = KafkaProducer(bootstrap_servers=load["BOOTSTRAP_SERVERS"])
    msg_dict = {
        "interval": 10,
        "producer": {
            "name": "producer 1",
            "host": "10.10.10.1",
            "user": "root",
            "password": "root"
        },
        "cpu": "33.5%",
        "mem": "77%",
        "msg": "Hello kafka"
    }
    msg = json.dumps(msg_dict)
    producer.send('mykafka', bytes(msg, encoding='utf-8'), partition=0)
    producer.close()
    print("success")
