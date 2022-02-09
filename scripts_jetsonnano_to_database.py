import boto3
from botocore.exceptions import NoCredentialsError
from mysql.connector import MySQLConnection, Error
from config import Config
from uuid import uuid4

# Get configuration data from config.ini file
DB = Config('config.ini', 'mysql').parse()
AWS = Config('config.ini', 'aws').parse()


def upload_image_to_aws(local_file_name: str, remote_file_name: str, bucket: str = AWS['bucket']) -> bool:
    '''
    upload_image_to_aws function uploads image to AWS S3 bucket
    param local_file_name: File in local want to upload to S3
    param remote_file_name: Name of file on S3
    param bucket: S3 bucket name
    '''
    s3 = boto3.client(
        's3', aws_access_key_id=AWS['access_key'], aws_secret_access_key=AWS['secret_access_key'])

    try:
        s3.upload_file(local_file_name, bucket,
                       'logs/{}'.format(remote_file_name))
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
    Insert a check-in person into database
    NOTE: Date format: "yyyy-mm-dd"
          Time format: "hh:mm:ss"

    Example: insert_log_database(105180001, 4, 0, '2020-1-1','12:23:42', '107210025.jpg')
    """
    query = """
    INSERT INTO Checkin_log(student_id, camera_id, mask, date, time, image)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    img_ext = image.split('.')[-1]
    img_name = '{}.{}'.format(uuid4().hex, img_ext)
    args = (student_id, camera_id, mask, date,
            time, 'logs/{}'.format(img_name))
    try:
        conn = MySQLConnection(**DB)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

        upload_image_to_aws(image, img_name)
        print(img_name)

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
