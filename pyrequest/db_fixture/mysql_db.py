import pymysql
import configparser as cparser
import os,sys
from os.path import dirname,abspath,join
BASE_DIR = dirname(dirname(abspath(__file__)))
DB_CONFIG_DIR = join(BASE_DIR,'config.ini')

#==================读取DB配置=================#
cf = cparser.ConfigParser()
cf.read(join(BASE_DIR,"config.ini"))
host = cf.get("mysqlconf","host")
port = cf.get("mysqlconf","port")
user = cf.get("mysqlconf","user")
password = cf.get("mysqlconf","password")
charset = cf.get("mysqlconf","charset")

class DB():

    def __init__(self,db_name):
        try:
            self.connection = pymysql.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                db=str(db_name),
                charset=charset,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.err.OperationalError as e:
            print("数据库操作错误 %d: %s" % (e.args[0],e.args[1]))
