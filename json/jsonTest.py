import json

if __name__ == '__main__':
    file = open('../data/tmp_order_order.json', mode='r', encoding='utf-8')
    json_data = json.load(file)
    strRead = json_data["job"]["content"][0]
    reader = json.load(json.dumps(str(strRead)))
    # writer = json.load(strRead)["writer"]
    print(strRead)
    # print(reader)
    # print(writer)
    # if strJson.__contains__("defaultFS")
