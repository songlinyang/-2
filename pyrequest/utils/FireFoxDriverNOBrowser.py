from selenium import webdriver
from selenium.webdriver.firefox.options import Options #使用无头模式

def FirefoxDriverNOBrowser():
   fireFox_options = Options()
   fireFox_options.add_argument('--headless')
   driverFirefox = webdriver.Firefox(firefox_options=fireFox_options)
   return driverFirefox
