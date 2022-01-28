import boto3
from botocore.exceptions import NoCredentialsError
from decouple import config
import os

from mysql.connector import MySQLConnection, Error


def upload_image_to_aws(local_file_name, remote_file_name, bucket=config('S3_BUCKET_NAME')):
    s3 = boto3.client('s3',
                      aws_access_key_id='AKIAQ57B5NVX2FCVMCZW', aws_secret_access_key='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')

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

upload_image_to_aws('fake_data.sql','fake01.sql')


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
