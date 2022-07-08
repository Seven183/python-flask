
from connect.redis.get_Conn import getConn

if __name__ == '__main__':

    redis = getConn()
    pipe = redis.pipeline(transaction=True)
    # 默认transaction为True
    pipe.hset('lrx_stus:dass','xiaohong','{"age":23,"addr":"上海"}')
    # redis的操作2
    # ...
    pipe.execute()

    print(redis.get("name"))