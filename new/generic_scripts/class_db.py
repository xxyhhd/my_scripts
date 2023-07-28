import pymysql
import psycopg2


class Db:

    def fetchone(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._cur.close()
        self._conn.close()



class Mysql_Db(Db):
    def __init__(self, dbname, user, password, host, port):
        self._conn = pymysql.connect(database=dbname, user=user, password=password, host=host, port=port)
        self._cur = self._conn.cursor()

    def execute(self, query, params=None):
        try:
            self._cur.execute(query, params)
        except pymysql.Error as e:
            print(e)
            self.rollback()
            self.close()
            return False


class Pgsql_Db(Db):
    def __init__(self, dbname, user, password, host, port):
        self._conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
        self._cur = self._conn.cursor()

    def execute(self, query, params=None):
        try:
            self._cur.execute(query, params)
        except psycopg2.Error as e:
            self.rollback()
            self.close()
            print(e)
            return False
