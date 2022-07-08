import time

if __name__ == '__main__':
    # 获取年月日 struct_time时间元组，共有九个元素组
    print(time.localtime())
    print(time.localtime(time.time()))
    print(time.localtime().tm_year)
    # 获取时间戳
    print(time.time())
    print(time.mktime(time.localtime()))
    # 时间格式化
    print(time.strftime("%Y-%m-%d %X"))
    print(time.strftime("%Y-%m-%d %X", time.localtime()))
    # format_time to struct_time
    print(time.strptime('2011-05-05 16:37:06', '%Y-%m-%d %X'))
