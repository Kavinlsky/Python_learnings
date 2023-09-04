import time

from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

url="https://www.google.com/maps/search/Hotels/@11.324206,77.7337621,15z/data=!3m1!4b1?entry=ttu"

driver=webdriver.Chrome()
driver.get(url)

driver.find_element(By.XPATH,value='//*[@id="assistive-chips"]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div[1]/button')

time.sleep(10)