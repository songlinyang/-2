# -*- coding:utf-8 -*-
import os,sys
BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
sys.path.append(BASE_PATH)
DATA_PATH = os.path.join(BASE_PATH,"data/pjb2")
import unittest,time
from selenium import webdriver
from ddt import file_data,ddt
from selenium.webdriver.support.ui import WebDriverWait
from utils.FireFoxDriverNOBrowser import FirefoxDriverNOBrowser
import configparser as cparser
import platform
cf = cparser.ConfigParser()
config_path = BASE_PATH + "/config.ini"
cf.read(config_path)

#====================== 配置
cashDebit = 1000 #标的金额
times = 1 #运行次数，外部获取
###############################以下是不用修改的公共引用变量##################################
if platform.system() == "Windows":
    print("当前运行环境为：Windows")
    picture_url = BASE_PATH + "\Image\login.png"
else:
    print("当前运行环境为：Linux")
    picture_url = BASE_PATH + "/Image/login.png"
##############################以上是不用修改的公共引用变量###################################
calenderXpath = '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[3]/div/div/div/div[2]/table/tbody/tr[5]/td[7]'#出票日期
backDate ='//*[@name="endDate"]/div/div/div[2]/table/tbody/tr[2]/td[4]'#到期日期--还款的时间#还款日期7月4号
startDateElement ='//*[@name="startDate"]/div/div/div[2]/table/tbody/tr[5]/td[2]'#出票日期
#======================


@ddt
class CheckBackendTest(unittest.TestCase):
    # 实现无界面

    @classmethod
    def setUpClass(cls):
        cls.driver= FirefoxDriverNOBrowser() #无界面
        #cls.driver = webdriver.Firefox()  # 有界面

    @file_data(os.path.join(DATA_PATH,"ddt_test_checkDebit_testcase.json"))
    def test_001_checkDebit_testcase(self,debitUrl,username,password):
        self.driver.get(debitUrl)
        self.driver.maximize_window()
        self.driver.implicitly_wait(3)
        # 用户名
        userName = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[1]/input')
        userName.send_keys(username)
        # 密码
        passWord = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[3]/input')
        passWord.send_keys(password)
        # 图片验证码
        imageCode = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[5]/input')
        imageCode.send_keys("111111")
        loginBtn = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div/div[7]')
        loginBtn.click()
        try:
            driver = self.driver
            var = 1
            for var in range(1):
                # 我要借款 按钮
                borrowButton = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div[2]/div/div[2]/a[2]')
                time.sleep(0.3)
                borrowButton.click()
                time.sleep(1)
                try:
                    debitCash = driver.find_element_by_name("loanAmt")
                except:
                    # 我要借款按钮
                    debitBtn = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div[2]/div/div[2]/a[2]')
                    debitBtn.click()
                    time.sleep(0.5)
                finally:
                    # 借款金额
                    debitCash = driver.find_element_by_name("loanAmt")
                    debitCash.clear()
                    debitCash.send_keys(cashDebit)

                    # 点击还款日期
                    debitDate = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[3]/div/input')
                    debitDate.click()
                    # 日期翻页
                    # 日期翻页
                    RQfy = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[3]/div/div/div/div[1]/a[4]')
                    RQfy.click()
                    calender = driver.find_element_by_xpath(calenderXpath)
                    calender.click()

                    time.sleep(0.5)
                    calender = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[3]/div/input')
                    calender.send_keys(calenderXpath)
                    # calender.send_keys(Keys.ENTER)
                    time.sleep(1)
                    # 票号
                    piaoNum = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[10]/table/tr[1]/td[2]/input')
                    piaoNum.send_keys("E60000003")
                    # 出票人
                    debitPeople = driver.find_element_by_name('borrower')
                    debitPeople.send_keys(u"深圳市发票有限责任公司")
                    # 上传文件      #对于两个id一样的元素用一下方法定位，加上索引，用elements
                    uploadFile = driver.find_elements_by_id('uploadFile')[1]
                    uploadFile.send_keys(picture_url)
                    time.sleep(0.5)
                    # 收款人
                    receivePeople = driver.find_element_by_name('beneficiary')
                    receivePeople.send_keys(u"北京高盛信息集团股份有限公司")
                    # 出票日期
                    startDate = driver.find_element_by_name('startDate')
                    startDate.click()
                    time.sleep(0.5)
                    # 出票日期--选择 今日出票
                    todayBtn = driver.find_element_by_xpath(startDateElement)
                    todayBtn.click()
                    # 到期日期
                    endDate = driver.find_element_by_name('endDate')
                    endDate.click()
                    time.sleep(0.5)

                    # 切换到下一个月
                    qiehuan2 = driver.find_element_by_xpath(
                        '//div[@class="mx-datepicker date-select"and @name="endDate"]//a[@class="mx-calendar__next-icon"][2]')
                    qiehuan2.click()
                    time.sleep(0.5)

                    # 切换到下一个月
                    qiehuan3 = driver.find_element_by_xpath(
                        '//div[@class="mx-datepicker date-select"and @name="endDate"]//a[@class="mx-calendar__next-icon"][2]')
                    qiehuan3.click()
                    time.sleep(0.5)

                    # 30号 日期
                    selectDate = driver.find_element_by_xpath(
                        '//*[@name="endDate"]/div/div/div[2]/table/tbody/tr[2]/td[4]')
                    selectDate.click()
                    time.sleep(0.5)

                    # 背书日期
                    reviewDate = driver.find_element_by_name('endorsementDate')
                    reviewDate.click()
                    time.sleep(0.5)

                    # 切换到下一月
                    nextMoth = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[10]/table/tr[6]/td[2]/div/div/div/div[1]/a[4]')
                    nextMoth.click()
                    time.sleep(0.5)

                    # 7月 25号日期
                    selectReviewDate = driver.find_element_by_xpath(
                        '//*[@id="app"]/div/div[1]/div[2]/div[4]/div[1]/div[10]/table/tr[6]/td[2]/div/div/div/div[2]/table/tbody/tr[2]/td[4]')
                    selectReviewDate.click()
                    time.sleep(0.5)

                    # 付款行
                    payBank = driver.find_element_by_name('creator')
                    payBank.send_keys(u"招商银行")
                    # 担保金额
                    sureCash = driver.find_element_by_name('guatantyAmt')
                    sureCash.send_keys("2500000")
                    time.sleep(1)

                    # 担保名称
                    DBamount = driver.find_element_by_name('securityName')
                    DBamount.click()
                    DBamount.send_keys(u'阿里巴巴')

                    # 担保人证件号码
                    DBzj = driver.find_element_by_name("idNo")
                    DBzj.click()
                    DBzj.send_keys('230903198611112345')

                    # 担保人电话
                    DBphone = driver.find_element_by_name('mobilePhone')
                    DBzj.click()
                    DBphone.send_keys('15596325674')

                    # 担保人法人代表姓名
                    DBFName = driver.find_element_by_name('securityLegalName')
                    DBFName.click()
                    DBFName.send_keys('测试')

                    # 担保人法人代表证件类型
                    DBFCard = driver.find_element_by_name('securityLegalIdType')
                    DBFCard.click()

                    # 担保人法人代表证件号码
                    DBFNumber = driver.find_element_by_name('securityLegalIdNo')
                    DBFNumber.click()
                    DBFNumber.send_keys('230903198611112345')

                    # 点击一下查询
                    queryBtn = driver.find_element_by_class_name('searchBt')
                    queryBtn.click()
                    time.sleep(0.5)

                    # 查询按钮
                    # CX=driver.find_element_by_class_name('searchBt')
                    # CX.click()

                    # 勾选担保函协议
                    js_0 = 'document.getElementsByClassName("checkbox")[0].click();'
                    driver.execute_script(js_0)
                    time.sleep(0.5)

                    # 勾选协议  使用js语法
                    # js = "$('div>p>label').click();"#console控制台的jquery语法输入，但是不支持前端的vue框架，vue框架下需要用原版的js代码语句
                    js = 'document.getElementsByClassName("checkbox")[1].click();'
                    driver.execute_script(js)
                    time.sleep(0.5)
                    # 提交按钮
                    submitBtn = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[4]/div[2]/div')
                    submitBtn.click()
                    time.sleep(1)
                    # 确定按钮
                    enterBtn = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[5]/div/div[2]/div/span')
                    enterBtn.click()
                    time.sleep(0.7)
        except Exception as e:
            print(e)
            raise
        finally:
            result = True
            self.assertTrue(result)



    @file_data(os.path.join(DATA_PATH,"ddt_test_checkTrail_testcase.json"))
    def test_002_checkTrail_testcase(self,loginUrl,username,password):
        # 打开网页
        driver = self.driver
        driver.get(loginUrl)
        driver.maximize_window()
        self.driver.implicitly_wait(8)
        # 登录账号
        userName = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/input')
        userName.send_keys(username)
        passWord = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/input')
        passWord.send_keys(password)
        # 点击空白页
        zongheBtn = self.driver.find_element_by_xpath('//*[@id="app"]/div/h1')
        zongheBtn.click()
        loginBtn = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/button')
        loginBtn.click()
        time.sleep(3)
        try:
            driver = self.driver
            var = 1
            # element = WebDriverWait(driver, 3).until(lambda driver: driver.find_element_by_class("nprogress-busy"))
            # 借款管理
            debitOne = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/ul/li[2]/div')
            debitOne.click()
            time.sleep(0.5)
            # 借款申请审核
            debitTwo = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/ul/li[2]/ul/li[5]/div')
            debitTwo.click()
            time.sleep(0.5)
            for var in range(1):
                # 打开借款申请经办
                debitThree = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/ul/li[2]/ul/li[5]/ul/li[1]')
                debitThree.click()
                time.sleep(0.5)
                # 点击待审核
                stayAduit = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/div[2]/button/span')
                stayAduit.click()
                time.sleep(0.5)
                # 点击查看详情
                catDetail = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[3]/div[1]/div[5]/div[2]/table/tbody/tr[1]/td[24]/div/button/span')
                catDetail.click()
                time.sleep(0.5)
                # 通过按钮
                passBtn = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[3]/div/div[1]/button')
                passBtn.click()
                time.sleep(0.5)
                # 风控评级
                riskBtn = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[5]/div/div[2]/div/form/div[1]/div/div/div[1]/input')
                riskBtn.click()
                time.sleep(0.5)
                # 选择 风控评级
                selectRisk = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/ul/li[1]')
                selectRisk.click()
                # 输入审核意见
                inputInfo = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[5]/div/div[2]/div/form/div[2]/div/div[1]/textarea')
                inputInfo.send_keys(u"初审审核通过")
                time.sleep(0.5)
                # 上传文件
                # uploadFileBtn = driver.find_element_by_name("uploadFile")
                # uploadFileBtn.send_keys(u'G:\P2G-BUG\借款bug\登录2.png')
                # 提交
                submitBtn = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[5]/div/div[2]/div/form/div[4]/div/div/div[1]/button/span')
                submitBtn.click()
                time.sleep(1.5)
                # 打开复审 -- > 新流程已简化 -- > 直接进入复审阶段
                # 点击复审按钮
                passButton = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[3]/div/div[1]/button')
                passButton.click()
                time.sleep(0.5)
                # 打开风险详情
                riskPage = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[5]/div/div[2]/div/form/div[1]/div/div/div[1]/input')
                riskPage.click()
                time.sleep(0.5)
                # 选择 风险等级
                selRiskLevel = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/ul/li[1]')
                selRiskLevel.click()
                time.sleep(0.5)
                # 输入审核意见
                inputReAduit = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[5]/div/div[2]/div/form/div[2]/div/div[1]/textarea')
                inputReAduit.send_keys(u"复审审核通过")
                # #选择文件上传
                # uploadBtn = driver.find_element_by_name('uploadFile')
                # uploadBtn.send_keys(u'G:\P2G-BUG\借款bug\登录2.png')
                # 提交
                submitBtn = driver.find_element_by_xpath(
                    '//*[@id="app"]/div/div[3]/div/div[5]/div/div[2]/div/form/div[4]/div/div/div[1]/button/span')
                submitBtn.click()
                time.sleep(2)
        except Exception as e:
            print(e)
            raise
        finally:
            result = True
            self.assertTrue(result,msg="审核流程测试通过")
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()