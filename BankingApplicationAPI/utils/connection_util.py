from psycopg2 import connect, OperationalError
import os


def create_connection():
    try:
        conn = connect(
            host=os.environ.get('HOST'),  # boudreaudb.cxjykkle8frz.us-west-1.rds.amazonaws.com
            database=os.environ.get('DB_NAME'),  # postgres
            user=os.environ.get('DB_USERNAME'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('PORT')
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
