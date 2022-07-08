# !/usr/bin/python
# -*- coding: UTF-8 -*-

from connect.mongodb.get_Conn import getConn

if __name__ == '__main__':

    # 获取连接
    conn = getConn()
    # 数据库名admin
    db = conn.local
    for x in db.posts.find():
        print(x)
    # posts = db.posts.find_one({"author": "Maxsu"})
    # posts = db.posts.find_one()
    # 关闭连接
    conn.close()
