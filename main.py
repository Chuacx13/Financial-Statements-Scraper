from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from functions import generate_roic_table, generate_equity_trend, generate_eps_trend, generate_revenue_trend

service = Service(executable_path="C:/Users/chuac/chromedriver.exe")
driver = webdriver.Chrome(service=service)

march = ['BABA', 'LOGI', 'RBRK', 'GRAB']
june = ['MSFT', 'INTU']
september = ['AAPL', 'MU', 'V']
december = ['META', 'INTC', 'ADBE', 'ASML', 'AMZN', 'TSM', 'TTD', 'TXN', 'TSLA', 'NVDA', 'NFLX', 'MCD', 'DPZ']
# unsure = ['KLAC', 'LRCX', 'QCOM', 'AMAT', 'KEYS', 'SWKS', 'AKAM', 'CGNX', 'SSNC', 'TER']

driver.get("https://discountingcashflows.com/")

for ticker in march:
    try:
        generate_roic_table(driver, ticker, '2024')
    except Exception as e:
        print(f"Error generating ROIC table for {ticker}: {e}")

    try:
        generate_equity_trend(driver, ticker, '2024')
    except Exception as e:
        print(f"Error generating Equity Trend for {ticker}: {e}")

    try:
        generate_eps_trend(driver, ticker, '2024')
    except Exception as e:
        print(f"Error generating EPS Trend for {ticker}: {e}")

    try:
        generate_revenue_trend(driver, ticker, '2024')
    except Exception as e:
        print(f"Error generating Revenue Trend for {ticker}: {e}")
    
    time.sleep(5)

# for ticker in june:
#     try:
#         generate_roic_table(driver, ticker, '2024')
#         time.sleep(10)
#     except Exception as e:
#         print(f"Error generating ROIC table for {ticker}: {e}")

# for ticker in september:
#     try:
#         generate_roic_table(driver, ticker, '2023')
#         time.sleep(10)
#     except Exception as e:
#         print(f"Error generating ROIC table for {ticker}: {e}")

# for ticker in december:
#     try:
#         generate_roic_table(driver, ticker, '2023')
#         time.sleep(10)
#     except Exception as e:
#         print(f"Error generating ROIC table for {ticker}: {e}")

driver.quit()
    