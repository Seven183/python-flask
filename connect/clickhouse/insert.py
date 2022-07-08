from datetime import datetime
import psutil as psutil

from connect.clickhouse.get_Conn import getConn

if __name__ == '__main__':

    client = getConn()
    now = datetime.now()
    time_stamp = now.strftime('%a %b %d %H:%M:%S CST %Y')  # Tue Apr 06 15:32:55 CST 2021  <class 'str'>
    create_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()

    try:
        sql = "insert into clickhouse_host_metrics777(time_stamp,host_name, chart_name, metric_name,metric_value,create_at) " \
              "values('%s','%s','%s','%s','%s','%s')" % (time_stamp, client.connection, "磁盘IO", net_io.bytes_sent, disk_io.write_time , create_at)
        res = client.execute(sql)
        print("成功写入数据")
    except Exception as e:
        print(str(e))