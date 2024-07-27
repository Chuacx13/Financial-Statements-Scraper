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

roic_table_data = {}

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_form"))
)

chosen_stock = "AAPL"
input_ticker = driver.find_element(By.CLASS_NAME, "search-input")
input_ticker.clear()
input_ticker.send_keys(chosen_stock)

first_ticker = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tr.clickable-row"))
)
first_ticker.click()

time.sleep(2)

financials = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
)
financials.click()

time.sleep(2)

income_statement = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item"))
)
income_statement.click()

time.sleep(2)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#report-table tbody tr td a"))
)

years = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr td a")
operating_incomes = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(9) td.formatted-value")
tax_expenses = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(15) td.formatted-value")
earnings_before_taxes = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(14) td.formatted-value")
for i in range(len(years)):
    roic_table_data[years[i].text] = [0, float(operating_incomes[i+1].text.replace(',', '')), float(tax_expenses[i+1].text.replace(',', '')), float(earnings_before_taxes[i+1].text.replace(',', '')), 0, 0, 0, 0, 0, 0]

time.sleep(2)

financials = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
)
financials.click()

time.sleep(2)

balance_sheet = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item:nth-of-type(2)"))
)
balance_sheet.click()

time.sleep(2)

years = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr td a")
short_term_debts = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(19) td.formatted-value")
long_term_debts = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(25) td.formatted-value")
total_debts = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(37) td.formatted-value")
equities = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(28) td.formatted-value")
for i in range(len(years)):
    roic_table_data[years[i].text][4] = float(short_term_debts[i].text.replace(',', ''))
    roic_table_data[years[i].text][5] = float(long_term_debts[i].text.replace(',', ''))
    roic_table_data[years[i].text][6] = float(total_debts[i].text.replace(',', ''))
    roic_table_data[years[i].text][7] = float(equities[i].text.replace(',', ''))

metrics = ['ROIC', 'Operating Income', 'Tax Expense', 'Earnings Before Taxes', 'Short Term Debt', 'Long Term Debt', 'Debt', 'Equity', 'Tax Rate', 'Net Operating Profit After Taxes']
roic_table = pd.DataFrame(roic_table_data, index=metrics)

roic_table.loc['Tax Rate'] = roic_table.loc['Tax Expense'] / roic_table.loc['Operating Income']
roic_table.loc['Net Operating Profit After Taxes'] = roic_table.loc['Operating Income'] * (1 - roic_table.loc['Tax Rate'])
roic_table.loc['ROIC'] = roic_table.loc['Net Operating Profit After Taxes'] / (roic_table.loc['Equity'] + roic_table.loc['Debt']) * 100

roic_trend_data = {
    'ROIC 1-Year': roic_table.loc['ROIC'].iloc[0], 
    'ROIC 5-Year': roic_table.loc['ROIC'].iloc[0:5].sum() / 5, 
    'ROIC 10-Year': roic_table.loc['ROIC'].iloc[0:10].sum() / 10
}

roic_trend_table = pd.DataFrame(roic_trend_data, index=[0])

# Create directory if it does not exist
directory = f"Final_Results/{chosen_stock}/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save DataFrame to CSV file in the created directory
file_path = os.path.join(directory, f'{chosen_stock}_roic.csv')
roic_table.to_csv(file_path)

file_path = os.path.join(directory, f'{chosen_stock}_roic_trend.csv')
roic_trend_table.to_csv(file_path, index=False)
driver.quit()


