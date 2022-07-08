
import yaml
from redis import ConnectionPool, StrictRedis

def getConn():

    global pipe
    with open("../../property.yaml") as f:
        load = yaml.safe_load(f)["REDIS"]
    pool = ConnectionPool(host=load["HOST"], port=load["PORT"], db=load["DB"], password=load["PASSWORD"], decode_responses=True)
    redis = StrictRedis(connection_pool=pool)
    return redis


class get_Conn:
    def __init__(self):
        self.data = []
    pass
