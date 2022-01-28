import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config
import os

from mysql.connector import MySQLConnection, Error


def upload_image_to_aws(local_file_name, remote_file_name, bucket):
    pass


def insert_log_database(student_id, camera_id, mask, date, time, image):
    """
    Insert a check-in person into databases using
    """
    query = """
    INSERT INTO Checkin_log(student_id, camera_id, mask, date, time, image)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    args = (student_id, camera_id, mask, date, time, image)
    try:
        conn = MySQLConnection(
            host=config('DB_HOST'),
            database=config('DB_NAME'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD')
        )
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
