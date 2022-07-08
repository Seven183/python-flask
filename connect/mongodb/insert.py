# !/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from connect.mongodb.get_Conn import getConn

if __name__ == '__main__':

    # 获取连接
    conn = getConn()
    # 数据库名admin
    db = conn.local
    post = {"author": "Maxsu",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print("post id is ", post_id)

    # 关闭连接
    conn.close()
