import shutil
import requests
from mysql.connector import MySQLConnection, Error
from config import Config

DB = Config('config.ini', 'mysql').parse()


def get_image_to_train():
    url_prefix = 'https://nckh-2022.s3.ap-southeast-1.amazonaws.com/'
    query = """
    SELECT CCCD, image
    FROM Checkin_student
    WHERE trained=0
    """
    data_loaded = []
    try:
        conn = MySQLConnection(**DB)
        cursor = conn.cursor(buffered=True)
        cursor.execute(query)

        row = cursor.fetchone()

        while row is not None:
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
            data_loaded.append(str(row[0]))
            row = cursor.fetchone()

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
