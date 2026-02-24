from itertools import product

import pymysql

DB_CONFIG = dict(
    host = 'localhost',
    user = 'root',
    password = '0000',
    database = 'cu_db',
    charset = 'utf8'
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)

    def verify_user(self, username, password):
        sql = 'select count(*) from users where username = %s AND password = %s'
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, password))
                count, = cur.fetchone()
                return count == 1

    def verify_products(self, product):
        sql = "select count(*) from members where product = %s"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, product)
                count, = cur.fetchone()
                return count == 1


    def fetch_products(self, category=None):
        with self.connect() as conn:
            with conn.cursor() as cur:
                if category == "아이스크림":
                    # %s에 들어갈 데이터를 두 번째 인자로 넘겨야 합니다.
                    sql = "select id, type, product, price, tag, stock from members where type = %s"
                    cur.execute(sql, category)
                else:
                    sql = "select id, type, product, price, tag, stock from members order by id"
                    cur.execute(sql)

                return cur.fetchall()

    def insert_product(self, type, product, price, tag, stock):
        sql = "insert into members (type, product, price, tag, stock) values (%s, %s, %s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (type, product, price, tag, stock))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    def delete_product(self, product):
        sql = "delete from members where product = %s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, product)
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

    def update_ui(self, product, price, stock):
        sql = "update members set price = %s, stock = %s where product = %s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (price, stock, product))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False

