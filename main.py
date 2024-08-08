from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from functions import generate_roic_table, generate_equity_trend, generate_eps_trend, generate_revenue_trend, generate_free_cash_flow_trend, generate_operating_cash_flow_trend, generate_analysis_results

service = Service(executable_path="C:/Users/chuac/chromedriver.exe")
driver = webdriver.Chrome(service=service)

march = {
    'BABA': 1.1, 
    'LOGI': 1.1, 
    'RBRK': 1.05, 
    'GRAB': 1.05
}

june = {
    'MSFT': 1.2, 
    'INTU': 1.05
}

september = {
    'AAPL': 1.2, 
    'MU': 1.1, 
    'V': 1.1
}

december = {
    'META': 1.2, 
    'INTC': 1.2, 
    'ADBE': 1.2, 
    'ASML': 1.1, 
    'AMZN': 1.2, 
    'TSM': 1.2, 
    'TTD': 1.1, 
    'TXN': 1.1, 
    'TSLA': 1.1, 
    'NVDA': 1.2, 
    'NFLX': 1.2, 
    'MCD': 1.1, 
    'DPZ': 1.05
}
# unsure = ['KLAC', 'LRCX', 'QCOM', 'AMAT', 'KEYS', 'SWKS', 'AKAM', 'CGNX', 'SSNC', 'TER']

driver.get("https://discountingcashflows.com/")

for ticker, growth_rate in march.items():
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

    try:
        generate_free_cash_flow_trend(driver, ticker, '2024')
    except Exception as e:
        print(f"Error generating Free Cash Flow Trend for {ticker}: {e}")

    try:   
        generate_operating_cash_flow_trend(driver, ticker, '2024')
    except Exception as e:
        print(f"Error generating Operating Cash Flow Trend for {ticker}: {e}")

    try:
        generate_analysis_results(driver, ticker, '2024', growth_rate)
    except Exception as e:
        print(f"Error generating final analysis for {ticker}: {e}")

    time.sleep(5)

for ticker, growth_rate in june.items():
    try:
        generate_roic_table(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating ROIC table for {ticker}: {e}")

    try:
        generate_equity_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Equity Trend for {ticker}: {e}")

    try:
        generate_eps_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating EPS Trend for {ticker}: {e}")

    try:
        generate_revenue_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Revenue Trend for {ticker}: {e}")

    try:
        generate_free_cash_flow_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Free Cash Flow Trend for {ticker}: {e}")

    try:   
        generate_operating_cash_flow_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Operating Cash Flow Trend for {ticker}: {e}")

    try:
        generate_analysis_results(driver, ticker, '2023', growth_rate)
    except Exception as e:
        print(f"Error generating final analysis for {ticker}: {e}")

    time.sleep(5)

for ticker, growth_rate in september.items():
    try:
        generate_roic_table(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating ROIC table for {ticker}: {e}")

    try:
        generate_equity_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Equity Trend for {ticker}: {e}")

    try:
        generate_eps_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating EPS Trend for {ticker}: {e}")

    try:
        generate_revenue_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Revenue Trend for {ticker}: {e}")

    try:
        generate_free_cash_flow_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Free Cash Flow Trend for {ticker}: {e}")

    try:   
        generate_operating_cash_flow_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Operating Cash Flow Trend for {ticker}: {e}")

    try:
        generate_analysis_results(driver, ticker, '2023', growth_rate)
    except Exception as e:
        print(f"Error generating final analysis for {ticker}: {e}")

    time.sleep(5)

for ticker, growth_rate in december.items():
    try:
        generate_roic_table(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating ROIC table for {ticker}: {e}")

    try:
        generate_equity_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Equity Trend for {ticker}: {e}")

    try:
        generate_eps_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating EPS Trend for {ticker}: {e}")

    try:
        generate_revenue_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Revenue Trend for {ticker}: {e}")

    try:
        generate_free_cash_flow_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Free Cash Flow Trend for {ticker}: {e}")

    try:   
        generate_operating_cash_flow_trend(driver, ticker, '2023')
    except Exception as e:
        print(f"Error generating Operating Cash Flow Trend for {ticker}: {e}")

    try:
        generate_analysis_results(driver, ticker, '2023', growth_rate)
    except Exception as e:
        print(f"Error generating final analysis for {ticker}: {e}")

    time.sleep(5)

driver.quit()
    