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

equity_trend_data = {}

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

equities = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(28) td.formatted-value")

if len(equities) >= 10:
    first_year = float(equities[0].text.replace(',', ''))
    second_year = float(equities[1].text.replace(',', ''))
    fifth_year = float(equities[4].text.replace(',', ''))
    tenth_year = float(equities[9].text.replace(',', ''))

    equity_trend_data = {
        '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
        '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
        '10-Year': [((first_year / tenth_year) ** (1/9) - 1) * 100, first_year, tenth_year]
    }

elif len(equities) >= 5:
    last_index = len(equities) - 1
    first_year = float(equities[0].text.replace(',', ''))
    second_year = float(equities[1].text.replace(',', ''))
    fifth_year = float(equities[4].text.replace(',', ''))
    last_year = float(equities[last_index].text.replace(',', ''))

    equity_trend_data = {
        '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
        '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
        f'{last_index + 1}-Year': [((first_year / last_year) ** (1/last_index) - 1) * 100, first_year, last_year]
    }

else: 
    last_index = len(equities) - 1
    equity_trend_data = {
        '1-Year': [0, 0, 0], 
        '5-Year': [0, 0, 0], 
        f'{last_index + 1}-Year': [0, 0, 0]
    }
    print('Data does not span over a large enough time horizon.')

metrics = ['Equity Growth Rate', 'Current Equity', 'Previous Equity']
equity_trend_table = pd.DataFrame(equity_trend_data, index=metrics)

# Create directory if it does not exist
directory = f"Final_Results/{chosen_stock}/{year}"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save DataFrame to CSV file in the created directory
file_path = os.path.join(directory, f"{chosen_stock}_equity_trend_{year}.csv")
equity_trend_table.to_csv(file_path, index=True)

driver.quit()



