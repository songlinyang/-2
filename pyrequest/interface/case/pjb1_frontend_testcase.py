import os,sys
BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
sys.path.append(BASE_PATH)
DATA_PATH = os.path.join(BASE_PATH,"data/pjb1")
import unittest
import requests
from common import common
from ddt import ddt,data, file_data, unpack
from selenium import  webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.FireFoxDriverNOBrowser import FirefoxDriverNOBrowser
import time

@ddt
class CheckFrontedTest(unittest.TestCase):
    def setUp(self):
        self.baseUrl = "http://192.168.1.195:8087"
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        pass

    def getToken(self,username,password):
        url = self.baseUrl+"/pj-common/login"
        payload = {
            "username": username,
            "password": password,
            "imageCode": "111111",
            "clientType": "WEB"}
        response = requests.post(url=url, json=payload).json()
        rsp_data = common.get_value_byKey(response, "data")
        rsp_token = common.get_value_byKey(rsp_data,"token")
        if rsp_token:
            return rsp_token
        else:
            return ""

    @file_data(os.path.join(DATA_PATH,"ddt_test_login_testcase.json"))
    def test_001_login_testcase(self,username,password):
       url = self.baseUrl+"/pj-common/login"
       payload = {
           "username":username,
           "password":password,
           "imageCode":"111111",
           "clientType":"WEB"}
       response = requests.post(url=url, json=payload).json()
       rsp_data = common.get_value_byKey(response, "data")
       rsp_user = common.get_value_byKey(rsp_data,"user")
       rsp_username = common.get_value_byKey(rsp_user,"username")
       self.assertEquals(rsp_username,username)

    @file_data(os.path.join(DATA_PATH,"ddt_test_charge_testcase.json"))
    def test_002_charge_testcase(self,username,password,chargeAmount):
        print(username,password)
        # driver = webdriver.Firefox() #取消注释后用来进行调试
        driver = FirefoxDriverNOBrowser()
        driver.get(self.baseUrl+"/login")
        driver.maximize_window()
        driver.implicitly_wait(3)
        # 登陆
        userName = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/div/div[2]/div/div[1]/input")
        userName.send_keys(username)
        passWord = driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/div/div[2]/div/div[3]/input")
        passWord.send_keys(password)
        driver.find_element_by_xpath("//*[@id='app']/div/div[1]/div[2]/div/div[2]/div/div[6]").click()
        time.sleep(2)
        #我的账户
        my_account = driver.find_elements_by_class_name("menu-item")[-1]
        my_account.click()
        # 点击充值
        CZAN = driver.find_element_by_class_name('btn-charge')
        CZAN.click()  # 点击充值按钮
        time.sleep(1)

        writeMoney = driver.find_element_by_name("chargemoney")
        writeMoney.send_keys(chargeAmount)  # 输入充值金额
        time.sleep(0.5)
        payMoney2 = driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[2]/div/div[2]/div[6]/div[2]/div')
        payMoney2.click()  # 充值 按钮
        time.sleep(3)
        sureBtn = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[2]/div/div[3]/div/div[2]/div/a')
        sureBtn.click()  # 确认按钮
        knowBtn = WebDriverWait(driver, 65, 0.5).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/b/div[4]/div[2]/a')))
        # knowBtn = driver.find_element_by_xpath('/html/body/b/div[4]/div[2]/a')
        knowBtn.click()
        time.sleep(2)
        checkCode = driver.find_element_by_xpath('//*[@id="smsCode"]')
        checkCode.send_keys("111111")
        time.sleep(1)
        passWd2 = driver.find_element_by_id("password")
        passWd2.send_keys("123456")  # 交易密码
        time.sleep(0.5)
        subminBtn = driver.find_element_by_id("nextButton")
        subminBtn.click()  # 确定 按钮
        time.sleep(6)

        al1 = EC.alert_is_present()(driver)  # 判断 最后的警告alert弹窗
        while al1 is False:
            al1 = EC.alert_is_present()(driver)  # 判断 最后的警告alert弹窗
        if al1:
            al1.accept()  #已获取 最后的警告alert弹窗，并进行关闭

        time.sleep(3)
        #交易明细
        detail = driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/div/div[1]/a[4]')
        detail.click()
        #获取充值金额
        charge_amount_js = """return document.querySelector('div.trade-detail>div.table>table>tbody>tr').getElementsByTagName('td')[2].textContent"""
        charge_amount = str(driver.execute_script(charge_amount_js))
        print("当前用户充值金额为:%s" % charge_amount)
        #退出浏览器
        driver.quit()
        #断言结果
        self.assertEquals(str(charge_amount),chargeAmount)

    @file_data(os.path.join(DATA_PATH,"ddt_test_invest_testcase.json"))
    def test_003_invest_testcase(self,username,password,investAmount,investProduct):
        url = self.baseUrl + "/pj-p2p-core/pcFront/planInvest/v3.0/submitInvestOrder"
        token = self.getToken(username,password)

        self.headers.update({"Authorization": "Bearer %s" % token})

        payload = {"investAmt": investAmount, "couponId": "", "planId": investProduct}
        if token:
            response = requests.post(url,headers=self.headers,json=payload).json()
            rsp_retMsg = common.get_value_byKey(response,"retMsg")
            if rsp_retMsg:
                self.assertEquals(rsp_retMsg,"OK","出借成功")
            else:
                rsp_retMsg=""
                self.assertTrue(rsp_retMsg,msg="服务器异常")
        else:
            self.assertTrue(token,msg="用户登陆失败，无法获取token")