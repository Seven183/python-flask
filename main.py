import datetime
import json

if __name__ == '__main__':

    # str = "select a,b,c from table "
    # index = str.index("select")
    # str_index = str.index("from")
    # print(str[index+6:str_index])
    # print(datetime.date.today())
    # print("sda")
    str = [{'field': 'tenant_code', 'value': 'tenant_code'}, {'field': 'new_store_count', 'value': 'count(1)'}]
    list = json.dumps(str)
    print(list)
