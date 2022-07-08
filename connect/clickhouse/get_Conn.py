
import yaml
from clickhouse_driver import Client


def getConn():

    global client
    with open("../../property.yaml") as f:
        load = yaml.safe_load(f)["CLICKHOUSE"]
    # client = Client(host=host_name, database='default', user='default', password='自己设的密码', send_receive_timeout=20, port=9000)
    client = Client(host=load["HOST"], database=load["DB"], send_receive_timeout=load["SEND_RECEIVE_TIMEOUT"], port=load["PORT"])
    return client


class get_Conn:
    def __init__(self):
        self.data = []
    pass
