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

roic_table_data = {}

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_form"))
)

input_ticker = driver.find_element(By.CLASS_NAME, "search-input")
input_ticker.clear()
input_ticker.send_keys("AAPL")

first_ticker = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tr.clickable-row"))
)
first_ticker.click()

financials = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
)
financials.click()

income_statement = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item"))
)
income_statement.click()

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#report-table tbody tr td a"))
)

years = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr td a")
operating_incomes = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(9) td.formatted-value")
tax_expenses = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(15) td.formatted-value")
for i in range(len(years)):
    roic_table_data[years[i].text] = ['', operating_incomes[i].text, tax_expenses[i].text, '', '', '', '', '', '', '']

time.sleep(5)

metrics = ['ROIC', 'Operating Income', 'Tax Expense', 'Earnings Before Taxes', 'Short Term Debt', 'Long Term Debt', 'Debt', 'Equity', 'Tax Rate', 'Net Operating Profit After Taxes']
roic_table = pd.DataFrame(roic_table_data, index=metrics)

roic_table.to_csv('roic_table.csv')
driver.quit()


