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

# EPS Growth Rate (Historical)
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
future_eps_analyst = current_eps * (eps_growth_rate_analyst_input ** 10)

## Future Stock Price
fsp_default_pe_analyst = future_eps_analyst * pe_analyst
fsp_max_pe_analyst = future_eps_analyst * max_pe_ratio
fsp_median_pe_analyst = future_eps_analyst * median_pe_ratio
fsp_min_pe_analyst = future_eps_analyst * min_pe_ratio

## Sticker Price - 15% Returns 
sp15_default_pe_analyst = fsp_default_pe_analyst * ((100/115)**10)
sp15_max_pe_analyst = fsp_max_pe_analyst * ((100/115)**10)
sp15_median_pe_analyst = fsp_median_pe_analyst * ((100/115)**10)
sp15_min_pe_analyst = fsp_min_pe_analyst * ((100/115)**10)

## Sticker Price - 12% Returns 
sp12_default_pe_analyst = fsp_default_pe_analyst * ((100/112)**10)
sp12_max_pe_analyst = fsp_max_pe_analyst * ((100/112)**10)
sp12_median_pe_analyst = fsp_median_pe_analyst * ((100/112)**10)
sp12_min_pe_analyst = fsp_min_pe_analyst * ((100/112)**10)

## Sticker Price - 10% Returns 
sp10_default_pe_analyst = fsp_default_pe_analyst * ((100/110)**10)
sp10_max_pe_analyst = fsp_max_pe_analyst * ((100/110)**10)
sp10_median_pe_analyst = fsp_median_pe_analyst * ((100/110)**10)
sp10_min_pe_analyst = fsp_min_pe_analyst * ((100/110)**10)

## MOS (30%) of Sticker Price - 15% Returns 
mos3015_default_pe_analyst = sp15_default_pe_analyst * 0.7
mos3015_max_pe_analyst = sp15_max_pe_analyst * 0.7
mos3015_median_pe_analyst = sp15_median_pe_analyst * 0.7
mos3015_min_pe_analyst = sp15_min_pe_analyst * 0.7

## MOS (50%) of Sticker Price - 15% Returns 
mos5015_default_pe_analyst = sp15_default_pe_analyst * 0.5
mos5015_max_pe_analyst = sp15_max_pe_analyst * 0.5
mos5015_median_pe_analyst = sp15_median_pe_analyst * 0.5
mos5015_min_pe_analyst = sp15_min_pe_analyst * 0.5

## MOS (30%) of Sticker Price - 12% Returns 
mos3012_default_pe_analyst = sp12_default_pe_analyst * 0.7
mos3012_max_pe_analyst = sp12_max_pe_analyst * 0.7
mos3012_median_pe_analyst = sp12_median_pe_analyst * 0.7
mos3012_min_pe_analyst = sp12_min_pe_analyst * 0.7

## MOS (50%) of Sticker Price - 12% Returns 
mos5012_default_pe_analyst = sp12_default_pe_analyst * 0.5
mos5012_max_pe_analyst = sp12_max_pe_analyst * 0.5
mos5012_median_pe_analyst = sp12_median_pe_analyst * 0.5
mos5012_min_pe_analyst = sp12_min_pe_analyst * 0.5

## MOS (30%) of Sticker Price - 10% Returns 
mos3010_default_pe_analyst = sp10_default_pe_analyst * 0.7
mos3010_max_pe_analyst = sp10_max_pe_analyst * 0.7
mos3010_median_pe_analyst = sp10_median_pe_analyst * 0.7
mos3010_min_pe_analyst = sp10_min_pe_analyst * 0.7

## MOS (50%) of Sticker Price - 10% Returns 
mos5010_default_pe_analyst = sp10_default_pe_analyst * 0.5
mos5010_max_pe_analyst = sp10_max_pe_analyst * 0.5
mos5010_median_pe_analyst = sp10_median_pe_analyst * 0.5
mos5010_min_pe_analyst = sp10_min_pe_analyst * 0.5

columns_analyst = [f'Default_P/E_Ratio({pe_analyst})', f'Highest_P/E_Ratio({max_pe_ratio})', f'Median_P/E_Ratio({median_pe_ratio})', f'Lowest_P/E_Ratio({min_pe_ratio})']
index = ['Future_Stock_Price', 'Sticker_Price_15%', 'MOS_30%(15)', 'MOS_50%(15)',  'Sticker_Price_12%', 'MOS_30%(12)', 'MOS_50%(12)', 'Sticker_Price_10%', 'MOS_30%(10)', 'MOS_50%(10)']

final_analyst = pd.DataFrame(columns=columns_analyst, index=index)

final_analyst.loc['Future_Stock_Price'] = [fsp_default_pe_analyst, fsp_max_pe_analyst, fsp_median_pe_analyst, fsp_min_pe_analyst]
final_analyst.loc['Sticker_Price_15%'] = [sp15_default_pe_analyst, sp15_max_pe_analyst, sp15_median_pe_analyst, sp15_min_pe_analyst]
final_analyst.loc['Sticker_Price_12%'] = [sp12_default_pe_analyst, sp12_max_pe_analyst, sp12_median_pe_analyst, sp12_min_pe_analyst]
final_analyst.loc['Sticker_Price_10%'] = [sp10_default_pe_analyst, sp10_max_pe_analyst, sp10_median_pe_analyst, sp10_min_pe_analyst]
final_analyst.loc['MOS_30%(15)'] = [mos3015_default_pe_analyst, mos3015_max_pe_analyst, mos3015_median_pe_analyst, mos3015_min_pe_analyst]
final_analyst.loc['MOS_50%(15)'] = [mos5015_default_pe_analyst, mos5015_max_pe_analyst, mos5015_median_pe_analyst, mos5015_min_pe_analyst]
final_analyst.loc['MOS_30%(12)'] = [mos3012_default_pe_analyst, mos3012_max_pe_analyst, mos3012_median_pe_analyst, mos3012_min_pe_analyst]
final_analyst.loc['MOS_50%(12)'] = [mos5012_default_pe_analyst, mos5012_max_pe_analyst, mos5012_median_pe_analyst, mos5012_min_pe_analyst]
final_analyst.loc['MOS_30%(10)'] = [mos3010_default_pe_analyst, mos3010_max_pe_analyst, mos3010_median_pe_analyst, mos3010_min_pe_analyst]
final_analyst.loc['MOS_50%(10)'] = [mos5010_default_pe_analyst, mos5010_max_pe_analyst, mos5010_median_pe_analyst, mos5010_min_pe_analyst]

# Create directory if it does not exist
directory = f"Final_Results/{chosen_stock}/{year}"
if not os.path.exists(directory):
    os.makedirs(directory)

# Save DataFrame to CSV file in the created directory
file_path = os.path.join(directory, f"{chosen_stock}_final_analyst({round(eps_growth_rate_analyst_input, 2)*100}%)_analysis_{year}.csv")
final_analyst.to_csv(file_path, index=True)

# Historical Analysis
future_eps_hist = current_eps * (eps_growth_rate_10year ** 10)

## Future Stock Price
fsp_default_pe_hist = future_eps_hist * pe_10year
fsp_max_pe_hist = future_eps_hist * max_pe_ratio
fsp_median_pe_hist = future_eps_hist * median_pe_ratio
fsp_min_pe_hist = future_eps_hist * min_pe_ratio

## Sticker Price - 15% Returns 
sp15_default_pe_hist = fsp_default_pe_hist * ((100/115)**10)
sp15_max_pe_hist = fsp_max_pe_hist * ((100/115)**10)
sp15_median_pe_hist = fsp_median_pe_hist * ((100/115)**10)
sp15_min_pe_hist = fsp_min_pe_hist * ((100/115)**10)

## Sticker Price - 12% Returns 
sp12_default_pe_hist = fsp_default_pe_hist * ((100/112)**10)
sp12_max_pe_hist = fsp_max_pe_hist * ((100/112)**10)
sp12_median_pe_hist = fsp_median_pe_hist * ((100/112)**10)
sp12_min_pe_hist = fsp_min_pe_hist * ((100/112)**10)

## Sticker Price - 10% Returns 
sp10_default_pe_hist = fsp_default_pe_hist * ((100/110)**10)
sp10_max_pe_hist = fsp_max_pe_hist * ((100/110)**10)
sp10_median_pe_hist = fsp_median_pe_hist * ((100/110)**10)
sp10_min_pe_hist = fsp_min_pe_hist * ((100/110)**10)

## MOS (30%) of Sticker Price - 15% Returns 
mos3015_default_pe_hist = sp15_default_pe_hist * 0.7
mos3015_max_pe_hist = sp15_max_pe_hist * 0.7
mos3015_median_pe_hist = sp15_median_pe_hist * 0.7
mos3015_min_pe_hist = sp15_min_pe_hist * 0.7

## MOS (50%) of Sticker Price - 15% Returns 
mos5015_default_pe_hist = sp15_default_pe_hist * 0.5
mos5015_max_pe_hist = sp15_max_pe_hist * 0.5
mos5015_median_pe_hist = sp15_median_pe_hist * 0.5
mos5015_min_pe_hist = sp15_min_pe_hist * 0.5

## MOS (30%) of Sticker Price - 12% Returns 
mos3012_default_pe_hist = sp12_default_pe_hist * 0.7
mos3012_max_pe_hist = sp12_max_pe_hist * 0.7
mos3012_median_pe_hist = sp12_median_pe_hist * 0.7
mos3012_min_pe_hist = sp12_min_pe_hist * 0.7

## MOS (50%) of Sticker Price - 12% Returns 
mos5012_default_pe_hist = sp12_default_pe_hist * 0.5
mos5012_max_pe_hist = sp12_max_pe_hist * 0.5
mos5012_median_pe_hist = sp12_median_pe_hist * 0.5
mos5012_min_pe_hist = sp12_min_pe_hist * 0.5

## MOS (30%) of Sticker Price - 10% Returns 
mos3010_default_pe_hist = sp10_default_pe_hist * 0.7
mos3010_max_pe_hist = sp10_max_pe_hist * 0.7
mos3010_median_pe_hist = sp10_median_pe_hist * 0.7
mos3010_min_pe_hist = sp10_min_pe_hist * 0.7

## MOS (50%) of Sticker Price - 10% Returns 
mos5010_default_pe_hist = sp10_default_pe_hist * 0.5
mos5010_max_pe_hist = sp10_max_pe_hist * 0.5
mos5010_median_pe_hist = sp10_median_pe_hist * 0.5
mos5010_min_pe_hist = sp10_min_pe_hist * 0.5

columns_hist = [f'Default_P/E_Ratio({pe_10year})', f'Highest_P/E_Ratio({max_pe_ratio})', f'Median_P/E_Ratio({median_pe_ratio})', f'Lowest_P/E_Ratio({min_pe_ratio})']

final_hist = pd.DataFrame(columns=columns_hist, index=index)

final_hist.loc['Future_Stock_Price'] = [fsp_default_pe_hist, fsp_max_pe_hist, fsp_median_pe_hist, fsp_min_pe_hist]
final_hist.loc['Sticker_Price_15%'] = [sp15_default_pe_hist, sp15_max_pe_hist, sp15_median_pe_hist, sp15_min_pe_hist]
final_hist.loc['Sticker_Price_12%'] = [sp12_default_pe_hist, sp12_max_pe_hist, sp12_median_pe_hist, sp12_min_pe_hist]
final_hist.loc['Sticker_Price_10%'] = [sp10_default_pe_hist, sp10_max_pe_hist, sp10_median_pe_hist, sp10_min_pe_hist]
final_hist.loc['MOS_30%(15)'] = [mos3015_default_pe_hist, mos3015_max_pe_hist, mos3015_median_pe_hist, mos3015_min_pe_hist]
final_hist.loc['MOS_50%(15)'] = [mos5015_default_pe_hist, mos5015_max_pe_hist, mos5015_median_pe_hist, mos5015_min_pe_hist]
final_hist.loc['MOS_30%(12)'] = [mos3012_default_pe_hist, mos3012_max_pe_hist, mos3012_median_pe_hist, mos3012_min_pe_hist]
final_hist.loc['MOS_50%(12)'] = [mos5012_default_pe_hist, mos5012_max_pe_hist, mos5012_median_pe_hist, mos5012_min_pe_hist]
final_hist.loc['MOS_30%(10)'] = [mos3010_default_pe_analyst, mos3010_max_pe_hist, mos3010_median_pe_hist, mos3010_min_pe_hist]
final_hist.loc['MOS_50%(10)'] = [mos5010_default_pe_hist, mos5010_max_pe_hist, mos5010_median_pe_hist, mos5010_min_pe_hist]

file_path = os.path.join(directory, f"{chosen_stock}_final_hist({round(eps_growth_rate_10year,2)*100}%)_analysis_{year}.csv")
final_hist.to_csv(file_path, index=True)

