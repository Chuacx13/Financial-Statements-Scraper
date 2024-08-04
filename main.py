from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

service = Service(executable_path="C:/Users/chuac/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://discountingcashflows.com/")

march = ['BABA', 'LOGI']
june = ['MFST', 'INTU']
september = ['AAPL', 'MU', 'V']
december = ['META', 'INTC', 'ADBE', 'ASML', 'AMZN', 'TSM', 'TTD', 'TXN', 'TSLA', 'NVDA', 'NFLX', 'MCD', 'DPZ']
# unsure = ['KLAC', 'LRCX', 'QCOM', 'AMAT', 'KEYS', 'SWKS', 'AKAM', 'CGNX', 'SSNC', 'TER']
time.sleep(3)

driver.quit()