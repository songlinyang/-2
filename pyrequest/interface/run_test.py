import os,sys
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
UTILS_PATH = os.path.join(BASE_PATH,'utils')
sys.path.append(BASE_PATH)
from utils.HTMLTestReportCN2 import HTMLTestRunner
from utils.config import CASE_PATH,REPORT_PATH,PICTURE_PATH
import unittest
import time
import traceback
# 获取系统当前时间
now = time.strftime('%Y-%m-%d-%H_%M', time.localtime(time.time()))
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

# 启动器
class Runner():

    def __init__(self,title,description):
        print(CASE_PATH)
        self.discover =  unittest.defaultTestLoader.discover(CASE_PATH,pattern='*_testcase.py', top_level_dir=None)
        self.title = title
        self.description = description
        # 定义测试报告存放路径，支持相对路径
        self.tdResult = REPORT_PATH + "/"
        # 定义测试结果报告存放路径，支持相对路径
        self.pcResult = PICTURE_PATH + "/"


    # 运行生成报告文件
    def run(self):

        if os.path.exists(self.tdResult):
            filename = self.tdResult + "daily_result.html"
            fp = open(filename,'wb')

            #定义测试报告
            runner = HTMLTestRunner(stream=fp,title=self.title,description=self.description)

            #运行测试用例
            runner.run(self.discover)
            fp.close()
        else:
            os.mkdir(self.tdResult)
            filename = self.tdResult + "daily_result.html"
            fp = open(filename,'wb')

            #定义测试报告
            runner = HTMLTestRunner(stream=fp,title=self.title,description=self.description)

            #运行测试用例
            runner.run(self.discover)
            fp.close()

runner = Runner("测试环境每日检测报告","执行情况：")
runner.run()
