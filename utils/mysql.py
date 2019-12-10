import pymysql

from config.conf import *


def getDatabaseConnection():
    return pymysql.connect(host=SQL_HOST,
                           user=USERNAME,
                           passwd=PASSWORD,
                           db=DATABASE,
                           cursorclass=pymysql.cursors.DictCursor)
