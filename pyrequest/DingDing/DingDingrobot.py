# -*- coding:utf-8 -*-
import requests
import json

"""
定义一个钉钉Robot类
"""
class DingDingRobot():

    def __init__(self):
        self.webhook = 'https://oapi.dingtalk.com/robot/send?access_token=cdf0b2717cfb723f863f5acf6ee65c2d5e7d341e55f65745f7bed6341f64b4bf'

    def set_domain(self,domain):
        self.__domain = domain

    def get_domain(self):
        return self.__domain

    def set_report_name(self,new_name):
        self.__report_name = new_name

    def get_report_name(self):
        return self.__report_name

    def set_picture_name(self,new_name):
        self.__picture_name = new_name

    def get_picture_name(self):
        return self.__picture_name

    def talk(self):
        headers = {"Content-Type":"application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
            "title":"自动测试报告",
            "text": "##### 自动化测试报告\n" +
                 # "> 自动化测试 -- 自动发标\n\n" +
                 ">  [测试结果](%s/%s)\n" % (self.__domain,self.__report_name) +
                 "> ![测试截图](%s/%s)\n" % (self.__domain,self.__picture_name) +
                 "> ##### 测试完成 [详情](http://%s/%s)\n " % (self.__domain,self.__report_name)
            },
            "at": {
            "atMobiles": [
                "QA"
                ],
                "isAtAll": "false"
                }
        }
        requests.post(self.webhook,headers=headers,json=data)
