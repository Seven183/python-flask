#encoding:utf-8
from clickhouse_driver import connect

if __name__ == '__main__':

    conn = connect('clickhouse://default:123456@' + '172.19.0.183' + ':9000/test_order_db')
    cursor = conn.cursor()

    # 近15分钟之内的order数据
    orderSql = "select * from test_order_db.t_order_order where UPDATE_TIME > subtractMinutes(now(),15)"
    # orderSql = "select * from test_order_db.t_order_order"
    cursor.execute(orderSql)

    index = 0
    orderCodeIndex = 0
    orderColumns = ''
    orderColumnsWithTypes = cursor.columns_with_types

    # 拿出所有order表拼接列 以及order_code对应的下标
    for orderColumnsWithType in orderColumnsWithTypes:
        if str(orderColumnsWithType[0]).__eq__("ORDER_CODE"):
            orderCodeIndex = index
        orderColumns = orderColumns + 'ORDER_' + orderColumnsWithType[0] + ','
        index = index + 1

    # 拿出所有order的值
    orderValues = cursor.fetchall()

    for orderValue in orderValues:
        receiveSql = "select * from test_order_db.t_order_receive where ORDER_CODE = '{}' and UPDATE_TIME > subtractMinutes(now(),15)".format(orderValue[orderCodeIndex])
        # receiveSql = "select * from test_order_db.t_order_receive where ORDER_CODE = '{}'".format(orderValue[orderCodeIndex])
        cursor.execute(receiveSql)
        receiveValues = cursor.fetchall()
        # 拿出所有receive表拼接列
        receiveColumns = ''
        receivColumnsWithTypes = cursor.columns_with_types
        for receivColumnsWithType in receivColumnsWithTypes:
            receiveColumns = receiveColumns + 'RECEIVE_' + receivColumnsWithType[0] + ','

        productSql = "select * from test_order_db.t_order_product where ORDER_CODE = '{}' and UPDATE_TIME > subtractMinutes(now(),15)".format(orderValue[orderCodeIndex])
        # productSql = "select * from test_order_db.t_order_product where ORDER_CODE = '{}'".format(orderValue[orderCodeIndex])
        cursor.execute(productSql)
        productValues = cursor.fetchall()
        # 拿出所有product表拼接列
        productColumns = ''
        productColumnsWithTypes = cursor.columns_with_types
        for productColumnsWithType in productColumnsWithTypes:
            productColumns = productColumns + 'PRODUCT_' + productColumnsWithType[0] + ','

        if len(receiveValues) > 0:
            for receiveValue in receiveValues:
                if len(productValues) > 0:
                    for productValue in productValues:
                        # 宽表值
                        wideTableValues = ''
                        # 宽表列
                        wideTableColumns = orderColumns + productColumns + receiveColumns
                        wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                        # 宽表值
                        for orderIndex in range(0, len(orderColumnsWithTypes)):
                            wideTableValues = wideTableValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                        for productIndex in range(0, len(productColumnsWithTypes)):
                            wideTableValues = wideTableValues + "'" + str(productValue[productIndex]).replace("'", "\\'") + "',"

                        for receiveIndex in range(0, len(receivColumnsWithTypes)):
                            wideTableValues = wideTableValues + "'" + str(receiveValue[receiveIndex]).replace("'", "\\'") + "',"

                        wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                        wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                        print(wideTableSql)
                        cursor.execute(wideTableSql)
                else:
                    # 宽表值
                    wideTableValues = ''
                    # 宽表列
                    wideTableColumns = orderColumns + receiveColumns
                    wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                    # 宽表值
                    for orderIndex in range(0, len(orderColumnsWithTypes)):
                        wideTableValues = wideTableValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                    for receiveIndex in range(0, len(receivColumnsWithTypes)):
                        wideTableValues = wideTableValues + "'" + str(receiveValue[receiveIndex]).replace("'", "\\'") + "',"

                    wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                    wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                    print(wideTableSql)
                    cursor.execute(wideTableSql)
        else:
            if len(productValues) > 0:
                for productValue in productValues:
                    # 宽表值
                    wideTableValues = ''
                    # 宽表列
                    wideTableColumns = orderColumns + productColumns
                    wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                    for orderIndex in range(0, len(orderColumnsWithTypes)):
                        wideTableValues = wideTableValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                    for productIndex in range(0, len(productColumnsWithTypes)):
                        wideTableValues = wideTableValues + "'" + str(productValue[productIndex]).replace("'", "\\'") + "',"

                    wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                    wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                    print(wideTableSql)
                    cursor.execute(wideTableSql)
            else:
                # 宽表值
                wideTableValues = ''
                # 宽表列
                wideTableColumns = orderColumns
                wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                # 宽表值
                for orderIndex in range(0, len(orderColumnsWithTypes)):
                    wideTableValues = wideTableValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                print(wideTableSql)
                cursor.execute(wideTableSql)
