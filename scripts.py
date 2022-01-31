import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config
import os

from mysql.connector import MySQLConnection, Error
from config import Config

DB = Config('config.ini', 'mysql').parse()
AWS = Config('config.ini', 'aws').parse()


def upload_image_to_aws(local_file_name: str, remote_file_name: str, bucket: str = AWS['storage_bucket_name']) -> bool:
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS['access_key'], aws_secret_access_key=AWS['secret_access_key'])

    try:
        s3.upload_file(local_file_name, bucket, remote_file_name)
        print('Upload Successful')
        return True
    except FileNotFoundError:
        print('The file was not found!')
        return False
    except NoCredentialsError:
        print('Credentials not available!')
        return False


def insert_log_database(student_id: int, camera_id: int, mask: int, date: str, time: str, image: str):
    """
    Insert a check-in person into databases using
    """
    query = """
    INSERT INTO Checkin_log(student_id, camera_id, mask, date, time, image)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    args = (student_id, camera_id, mask, date, time, image)
    try:
        conn = MySQLConnection(**DB)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

        upload_image_to_aws(image, image)

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
