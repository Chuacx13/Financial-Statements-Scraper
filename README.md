# Financial Statements Scraper

## Project Overview

This project is a Python-based web scraper designed to extract financial data from https://discountingcashflows.com. The project leverages Selenium WebDriver to automate the data collection process before saving the scraped data in a CSV file. Additionally, using the scraped data, a stock analysis is conducted to determine the fair price of a stock, along with its margin of safety prices. This analysis is inspired by the value investing tips and strategies suggested by Phil Town's Rule No. 1 book.

## Features

- Automated scraping of financial statements of your chosen ticker.
- Output contains suggested Sticker Prices of a stock, along with its Margin of Safety Price.
- Output saved in CSV format for easy viewing.

## Limitations

1. Stock analysis is done with referenced to quantitative strategies mentioned in Phil Town's Rule No. 1 book. Actual fair price still have to be determined with other information such as the company's quality of management and economic moat.
2. Scraped data only contains some metrics found in the company's financial statements (eg. EPS, Free Cash Flow, Revenue and more). Extracted metrics are chosen based on the requirement of Phil Town's suggested valuation strategies.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Selenium (`pip install selenium`)
- WebDriver for your browser (e.g., ChromeDriver for Google Chrome)

## Installation

Clone the repository using the following command:

```bash
git clone git@github.com:Chuacx13/Financial-Statements-Scraper.git
```

Ensure that you are in the right directory by using the following command:

```bash
cd Financial-Statements-Scraper
```

Install these dependences by using the following command:

```bash
pip install -r requirements.txt
```

## Run the Code

Run the code by using the following command:

```bash
python main.py
```
