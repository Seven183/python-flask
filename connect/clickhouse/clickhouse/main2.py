#encoding:utf-8
from clickhouse_driver import connect

if __name__ == '__main__':

    conn = connect('clickhouse://default:123456@' + '172.19.0.183' + ':9000/test_order_db')
    cursor = conn.cursor()

    # 自定义过滤列
    orderFilterColumns = ''
    # orderFilterColumns = 't_order_order.ID,t_order_order.TENANT_CODE'
    orderSplitColumns = orderFilterColumns.split(",")

    productFilterColumns = ''
    # productFilterColumns = 't_order_product.ID,t_order_product.TENANT_CODE'
    productSplitColumns = productFilterColumns.split(",")

    receiveFilterColumns = ''
    # receiveFilterColumns = 't_order_receive.ID,t_order_receive.TENANT_CODE'
    receiveSplitColumns = receiveFilterColumns.split(",")


    orderCode = set()
    orderOrderCodeSql = "select ORDER_CODE from test_order_db.t_order_order where UPDATE_TIME > subtractMinutes(now(),15)"
    cursor.execute(orderOrderCodeSql)
    orderOrderCodeValues = cursor.fetchall()
    for orderOrderCodeValue in orderOrderCodeValues:
        orderCode.add(orderOrderCodeValue[0])

    productOrderCodeSql = "select ORDER_CODE from test_order_db.t_order_product where UPDATE_TIME > subtractMinutes(now(),15)"
    cursor.execute(productOrderCodeSql)
    productOrderCodeValues = cursor.fetchall()
    for productOrderCodeValues in productOrderCodeValues:
        orderCode.add(productOrderCodeValues[0])

    receiveOrderCodeSql = "select ORDER_CODE from test_order_db.t_order_receive where UPDATE_TIME > subtractMinutes(now(),15)"
    cursor.execute(receiveOrderCodeSql)
    receiveOrderCodeValues = cursor.fetchall()
    for receiveOrderCodeValues in receiveOrderCodeValues:
        orderCode.add(receiveOrderCodeValues[0])

    # 遍历orderCode
    for orderCod in orderCode:
        orderSql = "select * from test_order_db.t_order_order where ORDER_CODE = '{}'".format(orderCod)
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
            receiveSql = "select * from test_order_db.t_order_receive where ORDER_CODE = '{}'".format(orderValue[orderCodeIndex])
            cursor.execute(receiveSql)
            receiveValues = cursor.fetchall()
            # 拿出所有receive表拼接列
            receiveColumns = ''
            receivColumnsWithTypes = cursor.columns_with_types
            for receivColumnsWithType in receivColumnsWithTypes:
                receiveColumns = receiveColumns + 'RECEIVE_' + receivColumnsWithType[0] + ','

            productSql = "select * from test_order_db.t_order_product where ORDER_CODE = '{}'".format(orderValue[orderCodeIndex])
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
                            wideTableOrderValues = ''
                            wideTableProductValues = ''
                            wideTableReceiveValues = ''

                            # 宽表值
                            for orderIndex in range(0, len(orderColumnsWithTypes)):
                                wideTableOrderValues = wideTableOrderValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                            for productIndex in range(0, len(productColumnsWithTypes)):
                                wideTableProductValues = wideTableProductValues + "'" + str(productValue[productIndex]).replace("'", "\\'") + "',"

                            for receiveIndex in range(0, len(receivColumnsWithTypes)):
                                wideTableReceiveValues = wideTableReceiveValues + "'" + str(receiveValue[receiveIndex]).replace("'", "\\'") + "',"


                            # 去除宽表不想要的列和值,如果没有要去除的列则忽略
                            orderIndex = 0
                            for orderColumnsWithType in orderColumnsWithTypes:
                                if len(orderSplitColumns) > 0 and str(orderSplitColumns).__contains__("t_order_order"):
                                    for orderSplitColumn in orderSplitColumns:
                                        if orderSplitColumn.split(".")[1].__eq__(orderColumnsWithType[0]):
                                            orderColumns = orderColumns.replace('ORDER_' + orderSplitColumn.split(".")[1] + "," , "")
                                            wideTableOrderValues = wideTableOrderValues.replace("'" + str(orderValue[orderIndex]) + "',", "")
                                    orderIndex = orderIndex + 1

                            productIndex = 0
                            for productColumnsWithType in productColumnsWithTypes:
                                if len(productSplitColumns) > 0 and str(productSplitColumns).__contains__("t_order_product"):
                                    for productSplitColumn in productSplitColumns:
                                        if productSplitColumn.split(".")[1].__eq__(productColumnsWithType[0]):
                                            productColumns = productColumns.replace('PRODUCT_' + productSplitColumn.split(".")[1] + "," , "")
                                            wideTableProductValues = wideTableProductValues.replace("'" + str(productValue[productIndex]) + "',", "")
                                    productIndex = productIndex + 1

                            receiveIndex = 0
                            for receivColumnsWithType in receivColumnsWithTypes:
                                if len(receiveSplitColumns) > 0 and str(receiveSplitColumns).__contains__("t_order_receive"):
                                    for receiveSplitColumn in receiveSplitColumns:
                                        if receiveSplitColumn.split(".")[1].__eq__(receivColumnsWithType[0]):
                                            orderColumns = orderColumns.replace('RECEIVE_' + receiveSplitColumn.split(".")[1] + ",", "")
                                            wideTableReceiveValues = wideTableReceiveValues.replace("'" + str(receiveValue[receiveIndex]) + "',", "")
                                    receiveIndex = receiveIndex + 1

                            wideTableColumns = orderColumns + productColumns + receiveColumns
                            wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                            wideTableValues = wideTableOrderValues + wideTableProductValues + wideTableReceiveValues
                            wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                            wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                            print(wideTableSql)
                            cursor.execute(wideTableSql)
                    else:
                        # 宽表值
                        wideTableOrderValues = ''
                        wideTableReceiveValues = ''

                        # 宽表值
                        for orderIndex in range(0, len(orderColumnsWithTypes)):
                            wideTableOrderValues = wideTableOrderValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                        for receiveIndex in range(0, len(receivColumnsWithTypes)):
                            wideTableReceiveValues = wideTableReceiveValues + "'" + str(receiveValue[receiveIndex]).replace("'", "\\'") + "',"

                        # 去除宽表不想要的列和值,如果没有要去除的列则忽略
                        orderIndex = 0
                        for orderColumnsWithType in orderColumnsWithTypes:
                            if len(orderSplitColumns) > 0 and str(orderSplitColumns).__contains__("t_order_order"):
                                for orderSplitColumn in orderSplitColumns:
                                    if orderSplitColumn.split(".")[1].__eq__(orderColumnsWithType[0]):
                                        orderColumns = orderColumns.replace('ORDER_' + orderSplitColumn.split(".")[1] + ",", "")
                                        wideTableOrderValues = wideTableOrderValues.replace("'" + str(orderValue[orderIndex]) + "',", "")
                                orderIndex = orderIndex + 1

                        receiveIndex = 0
                        for receivColumnsWithType in receivColumnsWithTypes:
                            if len(receiveSplitColumns) > 0 and str(receiveSplitColumns).__contains__("t_order_receive"):
                                for receiveSplitColumn in receiveSplitColumns:
                                    if receiveSplitColumn.split(".")[1].__eq__(receivColumnsWithType[0]):
                                        orderColumns = orderColumns.replace('RECEIVE_' + receiveSplitColumn.split(".")[1] + ",", "")
                                        wideTableReceiveValues = wideTableReceiveValues.replace("'" + str(receiveValue[receiveIndex]) + "',", "")
                                receiveIndex = receiveIndex + 1


                        wideTableColumns = orderColumns + receiveColumns
                        wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                        wideTableValues = wideTableOrderValues + wideTableReceiveValues
                        wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                        wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                        print(wideTableSql)
                        cursor.execute(wideTableSql)
            else:
                if len(productValues) > 0:
                    for productValue in productValues:
                        # 宽表值
                        wideTableOrderValues = ''
                        wideTableProductValues = ''

                        for orderIndex in range(0, len(orderColumnsWithTypes)):
                            wideTableOrderValues = wideTableOrderValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                        for productIndex in range(0, len(productColumnsWithTypes)):
                            wideTableProductValues = wideTableProductValues + "'" + str(productValue[productIndex]).replace("'", "\\'") + "',"

                        # 去除宽表不想要的列和值,如果没有要去除的列则忽略
                        orderIndex = 0
                        for orderColumnsWithType in orderColumnsWithTypes:
                            if len(orderSplitColumns) > 0 and str(orderSplitColumns).__contains__("t_order_order"):
                                for orderSplitColumn in orderSplitColumns:
                                    if orderSplitColumn.split(".")[1].__eq__(orderColumnsWithType[0]):
                                        orderColumns = orderColumns.replace('ORDER_' + orderSplitColumn.split(".")[1] + ",","")
                                        wideTableOrderValues = wideTableOrderValues.replace("'" + str(orderValue[orderIndex]) + "',", "")
                                orderIndex = orderIndex + 1

                        productIndex = 0
                        for productColumnsWithType in productColumnsWithTypes:
                            if len(productSplitColumns) > 0 and str(productSplitColumns).__contains__("t_order_product"):
                                for productSplitColumn in productSplitColumns:
                                    if productSplitColumn.split(".")[1].__eq__(productColumnsWithType[0]):
                                        productColumns = productColumns.replace('PRODUCT_' + productSplitColumn.split(".")[1] + ",", "")
                                        wideTableProductValues = wideTableProductValues.replace("'" + str(productValue[productIndex]) + "',", "")
                                productIndex = productIndex + 1

                        wideTableColumns = orderColumns + productColumns
                        wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                        wideTableValues = wideTableOrderValues + wideTableProductValues
                        wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                        wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                        print(wideTableSql)
                        cursor.execute(wideTableSql)
                else:
                    # 宽表值
                    wideTableOrderValues = ''

                    # 宽表值
                    for orderIndex in range(0, len(orderColumnsWithTypes)):
                        wideTableOrderValues = wideTableOrderValues + "'" + str(orderValue[orderIndex]).replace("'", "\\'") + "',"

                        # 去除宽表不想要的列和值,如果没有要去除的列则忽略
                    orderIndex = 0
                    for orderColumnsWithType in orderColumnsWithTypes:
                        if len(orderSplitColumns) > 0 and str(orderSplitColumns).__contains__("t_order_order"):
                            for orderSplitColumn in orderSplitColumns:
                                if orderSplitColumn.split(".")[1].__eq__(orderColumnsWithType[0]):
                                    orderColumns = orderColumns.replace('ORDER_' + orderSplitColumn.split(".")[1] + ",", "")
                                    wideTableOrderValues = wideTableOrderValues.replace("'" + str(orderValue[orderIndex]) + "',","")
                            orderIndex = orderIndex + 1

                    wideTableColumns = orderColumns
                    wideTableColumns = wideTableColumns[0:len(wideTableColumns) - 1]

                    wideTableValues = wideTableOrderValues
                    wideTableValues = wideTableValues[0:len(wideTableValues) - 1]
                    wideTableSql = "insert into test_order_db.t_order_product_receive (" + wideTableColumns + ")values(" + wideTableValues + ")"
                    print(wideTableSql)
                    cursor.execute(wideTableSql)
