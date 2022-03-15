import requests
from bs4 import BeautifulSoup
import datetime


def googlevalueparse(string):
    arr = string.split("> ")
    try:
        return (arr[0].split("\n"))[1].replace(" ", "", 1)
    except:
        return None


def getprice(ticker):
    page = requests.get("https://www.google.com/finance/quote/" + ticker)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="YMlKec fxKbKc")
    unparsed = results.prettify()
    price = googlevalueparse(unparsed)
    price = price.replace("$", "")
    results = soup.find(class_="zzDege")
    unparsed = results.prettify()
    name = googlevalueparse(unparsed)
    return price, name


def getmoversgain():
    page = requests.get("https://www.google.com/finance/markets/gainers")
    soup = BeautifulSoup(page.content, "html.parser")
    currentpriceshtml = soup.find_all(class_="YMlKec")
    tickershtml = soup.find_all(class_="COaKTb")
    percentchangehtml = soup.find_all(class_="JwB6zf")
    stocknamehtml = soup.find_all(class_="ZvmM7")
    prices, tickers, percentchange, stocknames = [], [], [], []
    for num in range(len(currentpriceshtml)):
        if num > 10:
            value = currentpriceshtml[num - 1]
            unparsed = value.prettify()
            price = googlevalueparse(unparsed)
            prices.append(price)
        else:
            continue
    for value in tickershtml:
        unparsed = value.prettify()
        ticker = googlevalueparse(unparsed)
        tickers.append(ticker)
    for num in range(len(percentchangehtml)):
        if num > 16:
            val = percentchangehtml[num - 1]
            val = str(val)
            arr = val.split("/span>")
            try:
                parsed = arr[1].split("</div>")
                percentchange.append(parsed[0])
            except:
                continue
        else:
            continue
    for value in stocknamehtml:
        unparsed = value.prettify()
        name = googlevalueparse(unparsed)
        stocknames.append(name)

    return prices, tickers, percentchange, stocknames


def getmoversloss():
    page = requests.get("https://www.google.com/finance/markets/losers")
    soup = BeautifulSoup(page.content, "html.parser")
    currentpriceshtml = soup.find_all(class_="YMlKec")
    tickershtml = soup.find_all(class_="COaKTb")
    percentchangehtml = soup.find_all(class_="JwB6zf")
    stocknamehtml = soup.find_all(class_="ZvmM7")
    prices, tickers, percentchange, stocknames = [], [], [], []
    for num in range(len(currentpriceshtml)):
        if num > 10:
            value = currentpriceshtml[num - 1]
            unparsed = value.prettify()
            price = googlevalueparse(unparsed)
            prices.append(price)
        else:
            continue
    for value in tickershtml:
        unparsed = value.prettify()
        ticker = googlevalueparse(unparsed)
        tickers.append(ticker)
    for num in range(len(percentchangehtml)):
        if num > 16:
            val = percentchangehtml[num - 1]
            val = str(val)
            arr = val.split("/span>")
            try:
                parsed = arr[1].split("</div>")
                percentchange.append(parsed[0])
            except:
                continue
        else:
            continue
    for value in stocknamehtml:
        unparsed = value.prettify()
        name = googlevalueparse(unparsed)
        stocknames.append(name)

    return prices, tickers, percentchange, stocknames

