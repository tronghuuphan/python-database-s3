import shutil
import requests
import os
from mysql.connector import MySQLConnection, Error
from config import Config

# Get configuration data from config.ini file
DB = Config('config.ini', 'mysql').parse()

def check_new_register():
    # Query student's data which wasn't trained
    query = """
    SELECT CCCD, image
    FROM Checkin_student
    WHERE trained=0
    """
    new_data = 0

    try:
        conn = MySQLConnection(**DB)
        cursor = conn.cursor(buffered=True)
        cursor.execute(query)
        row = cursor.fetchone()
        new_data = row
        cursor.close()
        conn.close()

    except Error as e:
        print(e)
        return -1

    finally:
        if not new_data:
            print('No New Registration')
            return 0  # No new register
        return 1 # New register

