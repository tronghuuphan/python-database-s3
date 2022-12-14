from mysql.connector import MySQLConnection, Error
from config import Config
import os
import requests
import shutil

DB = Config('config.ini', 'mysql').parse()

URL_PREFIX = 'https://do-an-tot-nghiep.s3.ap-southeast-1.amazonaws.com/'


def get_data_checkin(CCCD: str):
    # Query student infomation with CCCD from database
    query = """SELECT CCCD, concat(first_name, ' ', last_name) as fullname, birthday, name, image
                FROM db.Checkin_student
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


def get_image(CCCD: str, destination_folder):
    BASE_ROOT = os.getcwd()
    try:
        user_info = get_data_checkin(CCCD)

        image_endpoint = user_info[-1]
        image_extension = image_endpoint.split('.')[-1]
        image_name = f"{CCCD}.{image_extension}"
        DISPLAY_IMAGE_FOLDER = os.path.join(BASE_ROOT, destination_folder)

        if not os.path.exists(DISPLAY_IMAGE_FOLDER):
            os.mkdir(DISPLAY_IMAGE_FOLDER)
        os.chdir(DISPLAY_IMAGE_FOLDER)
        r = requests.get(URL_PREFIX+image_endpoint, stream=True)
        if r.status_code != 200:
            print(f'Error when getting image {CCCD}')
        else:
            r.raw.decode_cotent = True
            with open(image_name, 'wb') as file:
                shutil.copyfileobj(r.raw, file)
            print(f'Image saved: {DISPLAY_IMAGE_FOLDER}/{image_name}')
    except Error as e:
        print(e)
    finally:
        os.chdir(BASE_ROOT)
