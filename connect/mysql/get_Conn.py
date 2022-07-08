import pymysql
import yaml


def getConn():
    global conn
    with open("../../property.yaml", "r") as f:
        load = yaml.safe_load(f)["MYSQL"]
    conn = pymysql.connect(host=load["HOST"], user=load["USERNAME"], password=load["PASSWORD"], database=load["DB"], charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    return conn


class get_Conn:
    def __init__(self):
        self.data = []
    pass
