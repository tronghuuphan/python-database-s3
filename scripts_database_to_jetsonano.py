import shutil
import requests
import os
from mysql.connector import MySQLConnection, Error
from config import Config

# Get configuration data from config.ini file
DB = Config('config.ini', 'mysql').parse()

BASE_ROOT = os.getcwd()
TRAIN_FOLDER = os.path.join(BASE_ROOT, 'images')


def get_image_to_train():
    # Create a training folder if it doesn't exist and change working directory to it
    if not os.path.exists(TRAIN_FOLDER):
        os.mkdir(TRAIN_FOLDER)
    os.chdir(TRAIN_FOLDER)

    # S3 URL
    url_prefix = 'https://nckh-2022.s3.ap-southeast-1.amazonaws.com/'

    # Query student's data which wasn't trained
    query = """
    SELECT CCCD, image
    FROM Checkin_student
    WHERE trained=0
    """

    data_loaded = []  # Array to store CCCD will be downloaded
    try:
        conn = MySQLConnection(**DB)
        cursor = conn.cursor(buffered=True)
        cursor.execute(query)
        row = cursor.fetchone()

        # Download image from S3
        while row is not None:
            STUDENT_FOLDER = os.path.join(TRAIN_FOLDER, row[0])
            if not os.path.exists(STUDENT_FOLDER):
                os.mkdir(STUDENT_FOLDER)
            os.chdir(STUDENT_FOLDER)
            img_ext = row[1].split('.')[-1]
            img_name = '{}.{}'.format(row[0], img_ext)
            url = url_prefix + str(row[1])
            r = requests.get(url, stream=True)
            if r.status_code != 200:
                print('Error when getting image from S3')
            else:
                r.raw.decode_content = True
                with open(img_name, 'wb') as file:
                    shutil.copyfileobj(r.raw, file)
                print('Image saved to {}'.format(img_name))
            os.chdir(TRAIN_FOLDER)
            data_loaded.append(str(row[0]))
            row = cursor.fetchone()
        # Update trained field status
        query_status = """
        UPDATE Checkin_student
        SET trained=1
        WHERE CCCD=%s
        """
        for data in data_loaded:
            data = (data,)
            cursor.execute(query_status, data)
            conn.commit()

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        os.chdir(BASE_ROOT)

    if data_loaded:
        return 1
    return 0
