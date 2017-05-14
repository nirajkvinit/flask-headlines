import pymysql
import dbconfig

class DBHelper:
    def connect(self, database="crimemap"):
        return pymysql.connect(
            host = dbconfig.db_host,
            user = dbconfig.db_user,
            passwd = dbconfig.db_password,
            db = database
        )

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "select description from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "insert into crimes (description) value (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "delete from crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()
    def add_crime(self, category, date, latitude, longtitude, description):
        connection = self.connect()
        try:
            query = "insert into crimes (category, date, latitude, longtitude, description) values(%s, %s, %s, %s, %s )"
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, latitude, longtitude, description))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
