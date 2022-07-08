
from connect.clickhouse.get_Conn import getConn

if __name__ == '__main__':

    client = getConn()
    try:
        # sql = "DROP TABLE clickhouse_host_metrics777 "
        sql = "ALTER TABLE clickhouse_host_metrics777 DELETE WHERE chart_name = '磁盘IO' "
        res = client.execute(sql)
        print("删除数据")
    except Exception as e:
        print(str(e))