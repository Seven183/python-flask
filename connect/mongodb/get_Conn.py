import pymongo
import yaml


def getConn():

    global client
    with open("../../property.yaml") as f:
        load = yaml.safe_load(f)["MONGO"]
    conn = 'mongodb://' + load["USERNAME"] + ':' + load["PASSWORD"] + '@' + load["HOST"] + ':' + load["PORT"]
    client = pymongo.MongoClient(conn)
    return client


class get_Conn:
    def __init__(self):
        self.data = []
    pass
