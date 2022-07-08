
from connect.mysql.get_Conn import getConn

if __name__ == '__main__':

    global cursor, conn
    try:
        # 获取连接
        conn = getConn()
        cursor = conn.cursor()
        sql = "SELECT * from CTLGS "
        cursor.execute(sql)
        print(cursor.fetchone())
    except Exception:
        print("连接失败")
        cursor.close()
        conn.close()
