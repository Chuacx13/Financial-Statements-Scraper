from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

service = Service(executable_path="C:/Users/chuac/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://discountingcashflows.com/")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_form"))
)

input_ticker = driver.find_element(By.CLASS_NAME, "search-input")
input_ticker.clear()
input_ticker.send_keys("AAPL")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "clickable-row"))
)

first_ticker = driver.find_element(By.CLASS_NAME, "clickable-row")
first_ticker.click()

time.sleep(5)

driver.quit()