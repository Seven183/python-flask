import json
import requests


def request_get(url, param):

    fails = 0
    while True:
        try:
            if fails >= 3:
                break
            ret = requests.get(url=url, params=param, timeout=10)
            if ret.status_code == 200:
                return json.loads(ret.text)["data"]
            else:
                continue
        except:
            fails += 1
            print('网络连接出现问题, 正在尝试再次请求: ', fails)


if __name__ == '__main__':
    post_url = "http://172.16.27.55:8080/mtd/predict"
    request_param = {"date": "2022-01"}
    a = request_get(post_url, request_param)
    print(a)
