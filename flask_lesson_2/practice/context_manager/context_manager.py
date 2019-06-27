import psycopg2


class ContextForDatabase:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = psycopg2.connect(user='cursor',
                              password='password',
                              host='localhost',
                              port='5432',
                              database=self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


if __name__=='__main__':

    with ContextForDatabase('flask_db') as db:
        cursor = db.cursor()
        command = """SELECT * FROM products.fruits;"""
        cursor.execute(command)
        result = cursor.fetchall()
        print(result)

