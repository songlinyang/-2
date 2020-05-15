# -*- coding:utf-8 -*-
from db_fixture.mysql_db import DB
from os.path import dirname,abspath,join
BASE_DIR = dirname(dirname(abspath(__file__)))
import configparser as cparser
cf = cparser.ConfigParser()
cf.read(BASE_DIR+"/config.ini")
username = cf.get("investconf","username")

class Operate():

    def __init__(self,db_name):
        self.connection = DB(db_name).connection

    """
    获取订单信息
    :param username:
    :return result:
    """
    def get_invest_order(self,username):
        sql = """SELECT * FROM `pj_test3_user`.`t_user` a LEFT JOIN `pj_test3_core`.`t_plan_invest` b ON a.`id`=b.`investor_id` WHERE a.`cellphone`='%s' AND b.`status`=%d;""" % (username,200)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result

    """
        设置当天债转进池金额为0
    """
    def set_debit_limit_zero(self):
        self.connection.ping(reconnect=True)
        sql = """UPDATE `pj_test3_other`.`t_debt_limit` a SET a.debt_limit=0 WHERE a.`effect_date`=DATE(NOW());"""
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
        self.connection.commit()

    """
    获取订单状态
    :param username:
    :return result:
    """
    def get_invest_order_status(self,username):
        sql = """SELECT b.`status` FROM `pj_test3_user`.`t_user` a LEFT JOIN `pj_test3_core`.`t_plan_invest` b ON a.`id`=b.`investor_id` WHERE a.`cellphone`='%s' ORDER BY b.`id` DESC LIMIT 1;""" % (username)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()[0]
        return result

    def close_invest_order_check(self):
        self.connection.close()