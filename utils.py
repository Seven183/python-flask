import pymysql
import pandas as pd


def getData():
    global cursor, list
    conn = pymysql.connect(host='172.19.109.55', user='gtech-dev', password='gtech-dev', database='dev_control_tower',
                           charset='utf8')
    cursor = conn.cursor()
    sql = """
        SELECT
            date_format(report_time,'%Y-%m') as month,
            sum( 
                case  when b.order_type="Actual Delivery" and b.month31>0 then b.month31 
                when b.order_type="Actual Delivery" and b.month31=0 and b.month25 > 0 then b.month25 
                when b.order_type="Actual Delivery" and b.month25=0 and b.month20 > 0 then b.month20 
                when b.order_type="Actual Delivery" and b.month20=0 and b.month15 > 0 then b.month15 
                when b.order_type="Actual Delivery" and b.month15=0 and b.month10 > 0 then b.month10 
                when b.order_type="Actual Delivery" and b.month10=0 and b.month5  > 0 then b.month5 
                ELSE 0 end
            ) as actualDelivery
        from ( 
            SELECT 
                *  
            from ( 
                SELECT 
                    *, 
                    row_number()over(partition by order_type,market,tire_type,date_format(report_time,'%Y-%m') order by report_time desc) num 
                from order_delivery 
            ) a where a.num=1
        ) b group by date_format(report_time,'%Y-%m') 
        order by date_format(report_time,'%Y-%m') 
    """

    # data = pd.read_sql(sql, conn)
    # dataset = pd.DataFrame(data, columns=data.columns)
    # return dataset
    cursor.execute(sql)
    return cursor.fetchall()


if __name__ == '__main__':
    print(getData())
