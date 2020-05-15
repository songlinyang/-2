import os,sys
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
sys.path.append(BASE_PATH)
from utils.FireFoxDriverNOBrowser import FirefoxDriverNOBrowser
from PIL import Image
import time

# 获取系统当前时间
picture_now = time.strftime('%Y-%m-%d-%H', time.localtime(time.time()))
picture_day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
PICTRUE_PATH = os.path.dirname(os.path.abspath(__file__))
DATEFILE_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\" + "Picture" + "\\" + picture_day

class FireFoxScreener():

    def __init__(self,picture_url):
        self.driver = FirefoxDriverNOBrowser()
        self.picture_url = picture_url

    def screen_action(self):
        #打开网页
        self.driver.get(self.picture_url)
        #将界面最大化
        self.driver.maximize_window()

        #创建日期目录
        if os.path.exists(DATEFILE_PATH):
            self.picture_path = DATEFILE_PATH+"\\"+picture_now+"_picture_result.png"
        else:
            os.mkdir(DATEFILE_PATH)
            self.picture_path = DATEFILE_PATH+"\\"+picture_now+"_picture_result.png"


        self.driver.implicitly_wait(8)
        #等待2秒，等待页面元素渲染成功
        time.sleep(1.5)
        self.driver.save_screenshot(self.picture_path)



        #对应日期目录下，存放截图图片
        element = self.driver.find_elements_by_class_name("highcharts-background")[0]
        left = element.location['x']
        top = element.location['y']
        right = element.location['x'] + element.size['width']
        bottom = element.location['y'] + element.size['height']

        #创建结果百分比截图
        try:
            if os.path.exists(self.picture_path):
                im = Image.open(self.picture_path)
                im = im.crop((left,top,right,bottom))
                im.save(self.picture_path)
        except Exception as e:
            print(e)
        finally:
            os.system('taskkill /f /im firefox* >nul 2>nul')
            return self.picture_path





# if __name__ == "__main__":
#     ok = FireFoxScreener("http://ptzy3bf3w.bkt.clouddn.com/2019-07-01-19_00_07_result.html")
#     ok.screen_action()
