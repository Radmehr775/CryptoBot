
import requests
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import os
from datetime import datetime
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def sessionStarter(url):
    os.environ['MOZ_HEADLESS'] = '1'
    options = Options()
    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html


def timeGetter():
    now = datetime.now()
    tim = now.strftime("%H:%M:%S")
    return tim


def apiGetter(name):
    key = ""
    symbolslug = symbolSlug(name)
    name = symbolslug[1]
    url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD&api_key={}".format(
        name, key)
    response = requests.get(url)
    time = timeGetter()
    price = response.json()
    return [price["USD"], time]


def scraper(name):
    url = "https://arzdigital.com/coins/page-{}/"
    num = 1
    symbol = []
    slug = []
    while len(symbol) == 0 and len(slug) == 0:
        html = sessionStarter(url.format(num))
        soup = BeautifulSoup(html, "html.parser")
        symbol = soup.find_all(attrs={'data-symbol': name})
        slug = soup.find_all(attrs={"data-slug": name.lower()})
        num += 1
        print(num)
        if len(slug) or len(symbol) > 0:
            break
        if num > 206:
            break
    return [slug, symbol]


def symbolSlug(name):

    data = scraper(name)
    slug = data[0]
    symbol = data[1]

    if len(slug) > 0:
        datas = str(slug[0]).split(" ")
        for i in range(len(datas)):
            if re.search("^data-symbol", datas[i]):
                symbol = datas[i].split("=")[1].strip('""')
                symbol = symbol.split('"')[0]
                slug = name
                break
            else:
                continue
    elif len(symbol) > 0:
        datas = str(symbol[0]).split(" ")
        for i in range(len(datas)):
            if re.search("^data-slug", datas[i]):
                slug = datas[i].split("=")[1].strip('""')
                symbol = name
                break
            else:
                continue
    return slug, symbol


def pricePageURLGetter(name):
    data = scraper(name)
    slug = data[0]
    symbol = data[1]
    if len(slug) > 0:
        url = "https://arzdigital.com/coins/{}".format(name)
    elif len(symbol) > 0:
        datas = str(symbol[0]).split(" ")
        for i in range(len(datas)):
            if re.search("^data-slug", datas[i]):
                slug = datas[i].split("=")[1].strip('""')
                url = "https://arzdigital.com/coins/{}".format(slug)
                break
            else:
                continue
    return url


def scraperPriceGetter(name):

    url = pricePageURLGetter(name)
    html = sessionStarter(url)
    soup = BeautifulSoup(html, 'html.parser')
    time = timeGetter()
    price = soup.find_all(
        "div", class_="arz-coin-page-data__coin-price coinPrice btcprice pulser")
    if len(price) == 0:
        price = soup.find_all(
            "div", class_="arz-coin-page-data__coin-price coinPrice pulser")
    price = re.split("[<>]", str(price[0]))
    return [price[2].strip("$"), time]


def scraperDataGetter(name):
    priceTime = scraperPriceGetter(name)
    slugSymbol = symbolSlug(name)
    price = priceTime[0].split(",")
    if len(price) > 1:
        priceSymplified = price[0] + price[1]
    else:
        priceSymplified = priceTime[0]
    data = {"name": slugSymbol[0].lower(), "Symbol": slugSymbol[1],
            "price": float(priceSymplified), "time": priceTime[1]}
    df = pd.DataFrame(data, index=[0])
    df.to_csv("{}.csv".format(slugSymbol[0]), index=False, mode='a')
    return data


def apiDataGetter(name):
    priceTime = apiGetter(name)
    slug = symbolSlug(name)
    data = {"name": slug[0].lower(), "symbol": slug[1],
            "price": priceTime[0], "time": priceTime[1]}
    df = pd.DataFrame(data, index=[0])
    df.to_csv("{}.csv".format(slug[0]), index=False, mode='a')
    return data
