from mysql.connector import MySQLConnection, Error
from config import Config

DB = Config('config.ini', 'mysql').parse()


def get_data_checkin(CCCD: int):
    # Query student infomation with CCCD from database
    query = """SELECT CCCD, concat(first_name, ' ', last_name) as fullname, birthday, name
                FROM CheckIn.Checkin_student
                INNER JOIN Checkin_classsh ON Checkin_student.classSH_id=Checkin_classsh.id
                WHERE CCCD=%s;
            """
    args = (CCCD,)

    try:
        conn = MySQLConnection(**DB)
        cursor = conn.cursor()
        cursor.execute(query, args)
        row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

    return row