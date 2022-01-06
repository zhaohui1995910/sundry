# -*- coding: utf-8 -*-
# @Time    : 2022/1/6 9:28
# @Author  : 10867
# @FileName: 数据库.py
# @Software: PyCharm
import pymssql


class DBConnection(object):
    def __init__(self, ip, user, passwd, db):
        self.server = ip
        self.user = user
        self.password = passwd
        self.database = db

        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = pymssql.connect(
            server=self.server,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='GB2312'
        )
        self.cur = self.conn.cursor(as_dict=True)
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    with DBConnection('192.168.121.xxx', user="xxx", passwd="123456", db="xxx") as cur:
        cur.execute("select * from studnet;")
        result = cur.fetchall()
        print(result)
