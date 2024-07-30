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
current_eps = float(driver.find_element(By.CSS_SELECTOR, "div.company-container div.col-sm:nth-of-type(2) ul.list-group li:nth-of-type(5) span").text)
print(current_eps)

# EPS Growth Rate (Equity)
eps_trend = pd.read_csv(f'Final_Results/{chosen_stock}/{year}/{chosen_stock}_equity_trend_{year}.csv')
eps_growth_rate_10year = eps_trend.iloc[0, 3]/100 + 1

# EPS Growth Rate (Analyst)
eps_growth_rate_analyst_input = 1.2

# Default P/E for both potential EPS Growth Rate
pe_analyst = (eps_growth_rate_analyst_input - 1) * 200
pe_10year = (eps_growth_rate_10year - 1) * 200

# Max, Min and Median P/E 
median_pe_ratio = 0
max_pe_ratio = 0
min_pe_ratio = 0 
financials = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
)
financials.click()

time.sleep(2)

ratios = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item:nth-of-type(4)"))
)
ratios.click()

pe_ratios = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(2) td.formatted-value")
pe_ratios_list = []

if len(pe_ratios) >= 10:
    pe_ratios = pe_ratios[1:11]
elif len(pe_ratios) >= 5:
    last_index = len(pe_ratios) - 1
    pe_ratios = pe_ratios[1:last_index]
else:
    print('Data does not span over a large enough time horizon.')

for pe_ratio in pe_ratios:
    pe_ratios_list.append(float(pe_ratio.text.replace(',', '')))

pe_ratios_list.sort()
n = len(pe_ratios_list)
if n % 2 != 0 and n >= 5:
    median_index = n // 2
    median_pe_ratio = pe_ratios_list[median_index]
elif n % 2 == 0 and n >= 5:
    median_index_1 = n // 2 - 1
    median_index_2 = n // 2
    median_pe_ratio = (pe_ratios_list[median_index_1] + pe_ratios_list[median_index_2]) / 2

max_pe_ratio = max(pe_ratios_list)
min_pe_ratio = min(pe_ratios_list)

# Analyst Analysis
future_eps = current_eps * (eps_growth_rate_analyst_input ** 10)

future_stock_price_default_pe = future_eps * pe_analyst
future_stock_price_max_pe = future_eps * max_pe_ratio
future_stock_price_median_pe = future_eps * median_pe_ratio
future_stock_price_min_pe = future_eps * min_pe_ratio

sp15_default_pe = future_stock_price_default_pe * ((100/115)**10)
sp12_default_pe = future_stock_price_default_pe * ((100/112)**10)
sp10_default_pe = future_stock_price_default_pe * ((100/110)**10)

sp15_max_pe = future_stock_price_max_pe * ((100/115)**10)
sp12_max_pe = future_stock_price_max_pe * ((100/112)**10)
sp10_max_pe = future_stock_price_max_pe * ((100/110)**10)

sp15_median_pe = future_stock_price_median_pe * ((100/115)**10)
sp12_median_pe = future_stock_price_median_pe * ((100/112)**10)
sp10_median_pe = future_stock_price_median_pe * ((100/110)**10)

sp15_min_pe = future_stock_price_min_pe * ((100/115)**10)
sp12_min_pe = future_stock_price_min_pe * ((100/112)**10)
sp10_min_pe = future_stock_price_min_pe * ((100/110)**10)

columns_analyst = [f'Default_P/E_Ratio({pe_analyst})', f'Highest_P/E_Ratio({max_pe_ratio})', f'Median_P/E_Ratio({median_pe_ratio})', f'Lowest_P/E_Ratio({min_pe_ratio})']
index = ['Future_Stock_Price', 'Sticker_Price_15%', 'MOS_30%(15)', 'MOS_50%(15)',  'Sticker_Price_12%', 'MOS_30%(12)', 'MOS_50%(12)', 'Sticker_Price_10%', 'MOS_30%(10)', 'MOS_50%(10)']

final_analyst = pd.DataFrame(columns=columns_analyst, index=index)

final_analyst.loc['Future_Stock_Price'] = [future_stock_price_default_pe, future_stock_price_max_pe, future_stock_price_median_pe, future_stock_price_min_pe]
final_analyst.loc['Sticker_Price_15%'] = [sp15_default_pe, sp15_max_pe, sp15_median_pe, sp15_min_pe]
final_analyst.loc['Sticker_Price_12%'] = [sp12_default_pe, sp12_max_pe, sp12_median_pe, sp12_min_pe]
final_analyst.loc['Sticker_Price_10%'] = [sp10_default_pe, sp10_max_pe, sp10_median_pe, sp10_min_pe]

print(final_analyst)