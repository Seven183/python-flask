import json
import requests


def request_post(url, param):
    fails = 0
    while True:
        try:
            if fails >= 3:
                break

            headers = {'content-type': 'application/json'}
            ret = requests.post(url, json=param, headers=headers, timeout=10)

            if ret.status_code == 200:
                text = json.loads(ret.text)
            else:
                continue
        except:
            fails += 1
            print('网络连接出现问题, 正在尝试再次请求: ', fails)
        else:
            break
    return text

if __name__ == '__main__':
    post_url = "https://172.16.27.55:8080/mtd/predict"
    request_param = {"date": "2022-01"}
    a = request_post(post_url, request_param)
    print(a)