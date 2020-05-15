import os,sys
BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
sys.path.append(BASE_PATH)
DATA_PATH = os.path.join(BASE_PATH,"data/pjb3")
import unittest
import requests
from common import common
from ddt import ddt, file_data
from db_fixture.db_frontend_api_testcase import Operate
import time

@ddt
class CheckFrontendApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.op = Operate("pj_test3_core")

    def setUp(self):
        self.baseUrl = "http://192.168.1.175:8085"

    def tearDown(self):
        pass

    @file_data(os.path.join(DATA_PATH,"ddt_test_matchAssignTask.json"))
    def test_001_matchAssignTask(self,username,resultAssert):
        has_invest = self.op.get_invest_order(username)
        if has_invest:
            # 设置当天可债转金额为0
            print("设置当天可债转金额为0")
            self.op.set_debit_limit_zero()

            # 跑1号：投资匹配任务
            print("跑1号：投资匹配任务")
            rsp1 = requests.post(url=self.baseUrl+'/pj-p2p-job/p2gRun/01matchPlanInvest').json()
            print(common.get_value_byKey(rsp1,"retMsg"))
            result = common.get_value_byKey(rsp1,"retMsg") == 'OK'
            if result is not True:
                self.assertIs(result,True,msg="投资匹配任务执行失败，测试失败")

            # 跑3号：普通资产满标申请银行放款
            print("跑3号：普通资产满标申请银行放款")
            rsp2 = requests.post(url=self.baseUrl+'/pj-p2p-job/p2gRun/03allInvestMakeLoan').json()
            result = common.get_value_byKey(rsp2,"retMsg") == 'OK'
            if result is not True:
                self.assertIs(result,True,msg="普通资产满标申请银行放款任务执行失败，测试失败")

            # 跑4号：普通资产满标起息确认
            print("等待60s")
            time.sleep(60)
            print("跑4号：普通资产满标申请银行放款")
            rsp3 = requests.post(url=self.baseUrl+'/pj-p2p-job/p2gRun/04allProductMakeLoan').json()
            if rsp3:
                print(rsp3)
                result = common.get_value_byKey(rsp3, "retMsg") == 'OK'
                if result is not True:
                    self.assertIs(result, True, msg="普通资产满标起息确认任务执行失败，测试失败")


                order_status_result = self.op.get_invest_order_status(username)
                order_status = common.get_value_byKey(order_status_result, "status")

                allow_time = 0
                while order_status == 200 and allow_time < 5:
                    print("第%d次等待10s"%allow_time)
                    time.sleep(10)
                    order_status_result = self.op.get_invest_order_status(username)
                    order_status = common.get_value_byKey(order_status_result, "status")
                    allow_time+=1

                self.op.close_invest_order_check()
                # 断言是否匹配资产成功
                self.assertIn(order_status, resultAssert,"投资订单当前匹配状态为%s" % order_status)

        else:
            self.assertTrue(has_invest,msg="用户下单失败，网络或网关异常，测试失败")