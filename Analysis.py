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

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_form"))
)

year = '2023'
chosen_stock = "AAPL"
input_ticker = driver.find_element(By.CLASS_NAME, "search-input")
input_ticker.clear()
input_ticker.send_keys(chosen_stock) 

first_ticker = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tr.clickable-row"))
)
first_ticker.click()

time.sleep(2)

# Current EPS
current_eps = driver.find_element(By.CSS_SELECTOR, "div.company-container div.col-sm:nth-of-type(2) ul.list-group li:nth-of-type(5) span")

# EPS Growth Rate (Equity)
eps_trend = pd.read_csv(f'Final_Results/{chosen_stock}/{year}/{chosen_stock}_equity_trend_{year}.csv')
eps_growth_rate_10year = eps_trend.iloc[0, 3]/100 + 1

# EPS Growth Rate (Analyst)
eps_growth_rate_manual_input = 1.2

metrics = ['Current EPS, EPS Growth Rate (Equity), EPS Growth Rate (Analyst), Default P/E, Historical P/E, P/E used, Future EPS, Future Stock Price, Sticker Price, MOS 50%, MOS 30%']
