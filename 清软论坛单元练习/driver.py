from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# You need to change this to your actual binary path.
# options.binary_location = "C:\\Program Files\\Google\\Chrome Dev\\Application\\chrome.exe" # noqa: E501
# You need to change this to your actual web driver path.
driver = webdriver.Chrome(
    'drivers/chromedriver', chrome_options=options)
driver.get("http://www.baidu.com")
assert "百度" in driver.title
elem = driver.find_element(By.NAME, "wd")
elem.clear()
elem.send_keys("软件工程")
elem.send_keys(Keys.RETURN)
time.sleep(10)
driver.close()