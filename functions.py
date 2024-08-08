from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os 

def generate_roic_table(driver, ticker, year):
    """
    Generates a Return on Invested Capital (ROIC) table for a specified company and year, using data from a financial website.

    Parameters:
    driver (selenium.webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the ROIC table for.
    year (str): The year for which the ROIC table is to be generated.

    The function will scrape financial data such as Operating Income, Tax Expense, Earnings Before Taxes, Total Debt and Equity from the website. 
    It then calculates Tax Rate, Net Operating Profit After Taxes and ROIC and saves them as CSV files in a structured directory format.
    """

    roic_table_data = {}

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_form"))
    )

    input_ticker = driver.find_element(By.CLASS_NAME, "search-input")
    input_ticker.clear()
    input_ticker.send_keys(ticker)

    first_ticker = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tr.clickable-row"))
    )
    first_ticker.click()

    time.sleep(3)

    financials = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
    )
    financials.click()

    time.sleep(3)

    income_statement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item"))
    )
    income_statement.click()

    time.sleep(3)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#report-table tbody tr td a"))
    )

    years = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr td a")
    if len(years) < 5: 
        print(f'{ticker}\'s data does not span over a long enough time horizon.')
        return

    operating_incomes = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(9) td.formatted-value")
    tax_expenses = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(15) td.formatted-value")
    earnings_before_taxes = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(14) td.formatted-value")
    for i in range(len(years)):
        roic_table_data[years[i].text] = [0, float(operating_incomes[i+1].text.replace(',', '')), float(tax_expenses[i+1].text.replace(',', '')), float(earnings_before_taxes[i+1].text.replace(',', '')), 0, 0, 0, 0, 0, 0]

    time.sleep(3)

    financials = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
    )
    financials.click()

    time.sleep(3)

    balance_sheet = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item:nth-of-type(2)"))
    )
    balance_sheet.click()

    time.sleep(3)

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

    # Calculate average ROIC growth over different time horizons
    if len(years) >= 10:
        roic_trend_data = {
            'ROIC 1-Year': roic_table.loc['ROIC'].iloc[0], 
            'ROIC 5-Year': roic_table.loc['ROIC'].iloc[0:5].sum() / 5, 
            'ROIC 10-Year': roic_table.loc['ROIC'].iloc[0:10].sum() / 10
        }   
    elif len(years) >= 5:
        last_index = len(equities)
        roic_trend_data = {
            'ROIC 1-Year': roic_table.loc['ROIC'].iloc[0], 
            'ROIC 5-Year': roic_table.loc['ROIC'].iloc[0:5].sum() / 5, 
            f'ROIC {last_index}-Year': roic_table.loc['ROIC'].iloc[0:last_index].sum() / last_index
        } 

    roic_trend_table = pd.DataFrame(roic_trend_data, index=[0])

    # Create directory if it does not exist
    directory = f"Final_Results/{ticker}/{year}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f'{ticker}_roic_{year}.csv')
    roic_table.to_csv(file_path)

    file_path = os.path.join(directory, f'{ticker}_roic_trend_{year}.csv')
    roic_trend_table.to_csv(file_path, index=False)

def generate_equity_trend(driver, ticker, year):

    """
    Generates a trend analysis of equity values over different time periods, using data from a financial website.

    Parameters:
    driver (webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the equity trend for.
    year (str): The year for which the equity trend data is to be generated.

    The function will scrape Equity data from the website. 
    It then calculates Equity Growth Rates over different time horizons and saves them as CSV files in a structured directory format.
    """

    equities = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(28) td.formatted-value"))
    )
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
        return

    metrics = ['Equity Growth Rate', 'Current Equity', 'Previous Equity']
    equity_trend_table = pd.DataFrame(equity_trend_data, index=metrics)

    directory = f"Final_Results/{ticker}/{year}"
    
    file_path = os.path.join(directory, f"{ticker}_equity_trend_{year}.csv")
    equity_trend_table.to_csv(file_path, index=True)

def generate_eps_trend(driver, ticker, year): 
    """
    Generates a trend analysis of eps values over different time periods, using data from a financial website.

    Parameters:
    driver (webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the eps trend for.
    year (str): The year for which the eps trend data is to be generated.

    The function will scrape EPS data from the website. 
    It then calculates EPS Growth Rates over different time horizons and saves them as CSV files in a structured directory format.
    """
    eps_trend_data = {}

    financials = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
    )
    financials.click()

    time.sleep(3)

    income_statement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item"))
    )
    income_statement.click()

    time.sleep(3)

    eps = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(20) td.formatted-value")

    if len(eps) >= 10:
        first_year = float(eps[1].text.replace(',', ''))
        second_year = float(eps[2].text.replace(',', ''))
        fifth_year = float(eps[5].text.replace(',', ''))
        tenth_year = float(eps[10].text.replace(',', ''))
        
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

        eps_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            f'{last_index + 1}-Year': [((first_year / last_year) ** (1/last_index) - 1) * 100, first_year, last_year]
        }

    else: 
        return

    metrics = ['EPS Growth Rate', 'Current EPS', 'Previous EPS']
    eps_trend_table = pd.DataFrame(eps_trend_data, index=metrics)

    directory = f"Final_Results/{ticker}/{year}"

    file_path = os.path.join(directory, f"{ticker}_eps_trend_{year}.csv")
    eps_trend_table.to_csv(file_path, index=True)

def generate_revenue_trend(driver, ticker, year):
    """
    Generates a trend analysis of revenue values over different time periods, using data from a financial website.

    Parameters:
    driver (webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the revenue trend for.
    year (str): The year for which the revenue trend data is to be generated.

    The function will scrape Revenue data from the website. 
    It then calculates Revenue Growth Rates over different time horizons and saves them as CSV files in a structured directory format.
    """

    revenues = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(2) td.formatted-value"))
    )

    if len(revenues) >= 10:
        first_year = float(revenues[1].text.replace(',', ''))
        second_year = float(revenues[2].text.replace(',', ''))
        fifth_year = float(revenues[5].text.replace(',', ''))
        tenth_year = float(revenues[10].text.replace(',', ''))
        
        revenue_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            '10-Year': [((first_year / tenth_year) ** (1/9) - 1) * 100, first_year, tenth_year]
        }

    elif len(revenues) >= 5:
        last_index = len(revenues) - 1
        first_year = float(revenues[0].text.replace(',', ''))
        second_year = float(revenues[1].text.replace(',', ''))
        fifth_year = float(revenues[4].text.replace(',', ''))
        last_year = float(revenues[last_index].text.replace(',', ''))

        revenue_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            f'{last_index + 1}-Year': [((first_year / last_year) ** (1/last_index) - 1) * 100, first_year, last_year]
        }

    else: 
        return

    metrics = ['Revenue Growth Rate', 'Current Revenue', 'Previous Revenue']
    revenue_trend_table = pd.DataFrame(revenue_trend_data, index=metrics)

    directory = f"Final_Results/{ticker}/{year}"

    file_path = os.path.join(directory, f"{ticker}_revenue_trend_{year}.csv")
    revenue_trend_table.to_csv(file_path, index=True)

def generate_free_cash_flow_trend(driver, ticker, year):
    """
    Generates a trend analysis of free cash flow values over different time periods, using data from a financial website.

    Parameters:
    driver (webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the free cash flow trend for.
    year (str): The year for which the free cash flow trend data is to be generated.

    The function will scrape Free Cash Flow data from the website. 
    It then calculates Free Cash Flow Growth Rates over different time horizons and saves them as CSV files in a structured directory format.
    """

    financials = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dropdownMenuFinancials"))
    )
    financials.click()

    time.sleep(3)

    cash_flow_statement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.dropdown-item:nth-of-type(3)"))
    )
    cash_flow_statement.click()

    time.sleep(3)

    cash_flows = driver.find_elements(By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(30) td.formatted-value")

    if len(cash_flows) >= 10:
        first_year = float(cash_flows[1].text.replace(',', ''))
        second_year = float(cash_flows[2].text.replace(',', ''))
        fifth_year = float(cash_flows[5].text.replace(',', ''))
        tenth_year = float(cash_flows[10].text.replace(',', ''))
        
        cash_flow_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            '10-Year': [((first_year / tenth_year) ** (1/9) - 1) * 100, first_year, tenth_year]
        }

    elif len(cash_flows) >= 5:
        last_index = len(cash_flows) - 1
        first_year = float(cash_flows[0].text.replace(',', ''))
        second_year = float(cash_flows[1].text.replace(',', ''))
        fifth_year = float(cash_flows[4].text.replace(',', ''))
        last_year = float(cash_flows[last_index].text.replace(',', ''))

        cash_flow_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            f'{last_index + 1}-Year': [((first_year / last_year) ** (1/last_index) - 1) * 100, first_year, last_year]
        }

    else: 
        return

    metrics = ['Cash Flow Growth Rate', 'Current Cash Flow', 'Previous Cash Flow']
    cash_flow_trend_table = pd.DataFrame(cash_flow_trend_data, index=metrics)

    directory = f"Final_Results/{ticker}/{year}"
    file_path = os.path.join(directory, f"{ticker}_cash_flow_trend_{year}.csv")
    cash_flow_trend_table.to_csv(file_path, index=True)

def generate_operating_cash_flow_trend(driver, ticker, year):
    """
    Generates a trend analysis of operating cash flow values over different time periods, using data from a financial website.

    Parameters:
    driver (webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the operating cash flow trend for.
    year (str): The year for which the operating cash flow trend data is to be generated.

    The function will scrape Operating Cash Flow data from the website. 
    It then calculates Operating Cash Flow Growth Rates over different time horizons and saves them as CSV files in a structured directory format.
    """

    operating_cash_flows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#report-table tbody tr:nth-of-type(3) td.formatted-value"))
    )

    if len(operating_cash_flows) >= 10:
        first_year = float(operating_cash_flows[1].text.replace(',', ''))
        second_year = float(operating_cash_flows[2].text.replace(',', ''))
        fifth_year = float(operating_cash_flows[5].text.replace(',', ''))
        tenth_year = float(operating_cash_flows[10].text.replace(',', ''))
        
        operating_cash_flow_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            '10-Year': [((first_year / tenth_year) ** (1/9) - 1) * 100, first_year, tenth_year]
        }

    elif len(operating_cash_flows) >= 5:
        last_index = len(operating_cash_flows) - 1
        first_year = float(operating_cash_flows[0].text.replace(',', ''))
        second_year = float(operating_cash_flows[1].text.replace(',', ''))
        fifth_year = float(operating_cash_flows[4].text.replace(',', ''))
        last_year = float(operating_cash_flows[last_index].text.replace(',', ''))

        operating_cash_flow_trend_data = {
            '1-Year': [((first_year / second_year) - 1) * 100, first_year, second_year], 
            '5-Year': [((first_year / fifth_year) ** (1/4) - 1) * 100, first_year, fifth_year], 
            f'{last_index + 1}-Year': [((first_year / last_year) ** (1/last_index) - 1) * 100, first_year, last_year]
        }

    else: 
        return

    metrics = ['Operating Cash Flow Growth Rate', 'Current Operating Cash Flow', 'Previous Operating Cash Flow']
    operating_cash_flow_trend_table = pd.DataFrame(operating_cash_flow_trend_data, index=metrics)

    directory = f"Final_Results/{ticker}/{year}"
    file_path = os.path.join(directory, f"{ticker}_operating_cash_flow_trend_{year}.csv")
    operating_cash_flow_trend_table.to_csv(file_path, index=True)

def generate_analysis_results(driver, ticker, year, input_growth_rate):
    """
    This function scrapes financial data from a website using Selenium and performs an analysis to
    calculate various financial metrics like Future Stock Price, Sticker Price before applying a Margin of Safety of 50% or 30%. 
    Two EPS growth rates will be used, namely a user input growth rate and a historical growth rate.
    P/E ratios used to calculate Future Stock Price are Default P/E ratio, Highest P/E ratio in the last 5-10 years, Lowest P/E ratio in the last 5-10 years and Median P/E ratio in the last 5-10 years.
    The results are saved as CSV files.

    Parameters:
    driver: Selenium WebDriver instance used for webpage interaction.
    ticker: Stock ticker symbol of the company being analyzed.
    tear: The year for which the analysis is performed (used in naming output files).

    Parameters:
    driver (webdriver.Chrome): The Selenium WebDriver instance used for web automation.
    ticker (str): The ticker symbol of the company to generate the final analysis report for.
    year (str): The year for which the final analysis report is to be generated.
    input_growth_rate (float): Estimated growth rate decided by the user. 
    """
     
    chart_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Chart"))
    )
    chart_link.click()

    time.sleep(3)

    # Current EPS
    current_eps = float(driver.find_element(By.CSS_SELECTOR, "div.company-container div.col-sm:nth-of-type(2) ul.list-group li:nth-of-type(5) span").text)

    # EPS Growth Rate (Historical)
    eps_trend = pd.read_csv(f'Final_Results/{ticker}/{year}/{ticker}_equity_trend_{year}.csv')
    eps_growth_rate_10year = eps_trend.iloc[0, 3]/100 + 1

    # EPS Growth Rate (Analyst)
    eps_growth_rate_analyst_input = input_growth_rate

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

    time.sleep(3)

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
        return

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

    directory = f"Final_Results/{ticker}/{year}"
    file_path = os.path.join(directory, f"{ticker}_final_analyst({round(eps_growth_rate_analyst_input*100, 2)}%)_analysis_{year}.csv")
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
    final_hist.loc['MOS_30%(10)'] = [mos3010_default_pe_hist, mos3010_max_pe_hist, mos3010_median_pe_hist, mos3010_min_pe_hist]
    final_hist.loc['MOS_50%(10)'] = [mos5010_default_pe_hist, mos5010_max_pe_hist, mos5010_median_pe_hist, mos5010_min_pe_hist]

    file_path = os.path.join(directory, f"{ticker}_final_hist({round(eps_growth_rate_10year*100, 2)}%)_analysis_{year}.csv")
    final_hist.to_csv(file_path, index=True)



