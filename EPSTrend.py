from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
import sys

service = Service(executable_path="C:/Users/chuac/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://discountingcashflows.com/")

eps_trend_data = {}

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "SearchKeyword"))
)

year = '2024'
chosen_stock = "AAPL"
input_ticker = driver.find_element(By.ID, "SearchKeyword")
input_ticker.clear()
input_ticker.send_keys(chosen_stock) 

first_ticker = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#SearchResults ul li:first-child a"))
)
first_ticker.click()

time.sleep(2)

financials = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "financialsIcon"))
)
financials.click()

time.sleep(2)

income_statement = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "details.dropdown.dropdown-start ul li:first-child a"))
)
income_statement.click()

time.sleep(2)

eps = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(21) td.formatted-value")

if len(eps) >= 10:
    first_year = float(eps[1].text.replace(',', ''))
    second_year = float(eps[2].text.replace(',', ''))
    fifth_year = float(eps[5].text.replace(',', ''))
    tenth_year = float(eps[10].text.replace(',', ''))
    
    if first_year < 0 or second_year < 0 or fifth_year < 0 or tenth_year < 0: 
        eps_trend_data = {
            '1-Year': [((first_year - second_year)/second_year) * 100, first_year, second_year], 
            '5-Year': [((first_year - fifth_year)/fifth_year) * 100, first_year, fifth_year], 
            '10-Year': [((first_year - tenth_year)/tenth_year) * 100, first_year, tenth_year]
        }
    else:
        eps_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            '10-Year': [((first_year / tenth_year) ** (1/9) - 1) * 100, first_year, tenth_year]
        }

elif len(eps) >= 5:
    last_index = len(eps) - 1
    first_year = float(eps[0].text.replace(',', ''))
    second_year = float(eps[1].text.replace(',', ''))
    fifth_year = float(eps[4].text.replace(',', ''))
    last_year = float(eps[last_index].text.replace(',', ''))

    if first_year < 0 or second_year < 0 or fifth_year < 0 or last_year < 0: 
        eps_trend_data = {
            '1-Year': [((first_year - second_year)/second_year) * 100, first_year, second_year], 
            '5-Year': [((first_year - fifth_year)/fifth_year) * 100, first_year, fifth_year], 
            '10-Year': [((first_year - last_year)/last_year) * 100, first_year, last_year]
        }
    else:
        eps_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            f'{last_index + 1}-Year': [((first_year / last_year) ** (1/last_index) - 1) * 100, first_year, last_year]
        }

else: 
    print(f'{chosen_stock}\'s data does not span over a long enough time horizon.')
    sys.exit()

metrics = ['EPS Growth Rate', 'Current EPS', 'Previous EPS']
eps_trend_table = pd.DataFrame(eps_trend_data, index=metrics)

# Create directory if it does not exist
directory = f"Final_Results/{chosen_stock}/{year}"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save DataFrame to CSV file in the created directory
file_path = os.path.join(directory, f"{chosen_stock}_eps_trend_{year}.csv")
eps_trend_table.to_csv(file_path, index=True)

driver.quit()



