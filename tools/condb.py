import pymysql
import re
from warnings import filterwarnings
import psycopg2


filterwarnings("error",category=pymysql.Warning)

class db():
    instance = None
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, host, dbname, port, user='root', passwd='123456'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname

    def ReadFromMysql(self, sql):
        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.dbname)
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            conn.close()
            return (res)
        except pymysql.Error as e:
            return (repr(e))


    def WriteToMysql(self, sql):
        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.dbname)
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        except pymysql.Error as e:
            return (repr(e))


    def RWMsql(self, sqls):
        r_res = []
        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.dbname)
            cursor = conn.cursor()
            for sql in sqls:
                cursor.execute(sql)
                if re.search(r'^select', sql, re.IGNORECASE):
                    r_res.append(cursor.fetchall())
            conn.commit()
            cursor.close()
            conn.close()
            return r_res
        except pymysql.Error as e:
            return (repr(e))


    def ReadFromPgsql(self, sql):
        # try:
        conn = psycopg2.connect(
            host=self.host, port=self.port, user=self.user, password=self.passwd, database=self.dbname)
        cursor = conn.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        conn.close()
        return res
        # except:
        #     return 2222


    def WriteToPgsql(self, sql):
        pass


    def RWPgsql(self, sqls):
        pass
