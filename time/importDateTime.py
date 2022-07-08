import datetime

'''
    datetime.date：表示日期的类。常用的属性有year, month, day；
    datetime.time：表示时间的类。常用的属性有hour, minute, second, microsecond；
    datetime.datetime：表示日期时间。
    datetime.timedelta：表示时间间隔，即两个时间点之间的长度。
    datetime.tzinfo：与时区有关的相关信息。

'''

if __name__ == '__main__':
    print(datetime.date.today())
    print(datetime.date(2021, 12, 22))
    print(datetime.time(10, 22, 22))
    print('today():', datetime.datetime.today())
    print('now():', datetime.datetime.now())
    print('utcnow():', datetime.datetime.utcnow())
    print('timedelta():', datetime.datetime.now() + datetime.timedelta(days=-1))
    print('timedelta2():', (datetime.datetime.now() + datetime.timedelta(days=1)) - (datetime.datetime.now() - datetime.timedelta(days=1)))
