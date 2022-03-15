import requests
import json
import jsonify
import discord
import random
from scraper import getprice
import math
from bs4 import BeautifulSoup
from scraper import getmoversgain
from scraper import getmoversloss
client = discord.Client()


class user():
    def __init__(self, uuid):
        with open("./jsons/users.json", "r") as file:
            data = json.load(file)
            self.tickers = data[str(uuid)]["ticklist"]


def tickerexists(ticker):
    page = requests.get("https://www.google.com/finance/quote/" + ticker)
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.find(class_="WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb")
    if result is None:
        return True
    else:
        return False


def functionparse(message):
    splitmsg = message.content.split(" ")
    return splitmsg


def updatelist(uuid, type, ticker):
    with open("./jsons/users.json", "r") as file:
        data = json.load(file)
        file.close()
    with open("./jsons/users.json", "w") as file:
        try:
            ticklist = data[str(uuid)]["ticklist"]
            if type == "remove" or type == "r":
                ticklist.remove(ticker.upper())
                json.dump(data, file)
                file.close()
            if type == "add" or type == "a":
                ticklist.append(ticker.upper())
                json.dump(data, file)
                file.close()
        except:
            dictionary = {str(uuid): {"ticklist": [ticker.upper()]}}
            data.update(dictionary)
            json.dump(data, file)
            file.close()


@client.event
async def on_message(message):
    uuid = message.author.id
    args = functionparse(message)
    if message.content.startswith("$price"):
        ticker = args[1]
        ticker = ticker.upper()
        if args[1] == "list":
            author = user(uuid)
            ticklist = author.tickers
            string = ""
            for ticker in ticklist:
                price, name = getprice(ticker)
                string = string + name + "(" + ticker + ")" + " is currently valued at $" + price + ".\n"
            await message.channel.send(string)
        else:
            if ticker.count(":") > 0:
                exists = tickerexists(ticker)
                if exists:
                    price, name = getprice(ticker)
                    await message.channel.send("The price of a share of " + name + "(" + ticker + ") is: $" + price + ".")
                if not exists:
                    await message.channel.send(
                        "Ticker: " + ticker + " does not exists.")
            else:
                await message.channel.send("No stock exchange specified.")
    if message.content.startswith("$list"):
        ticker = args[2]
        if ticker.count(":") > 0:
            exists = tickerexists(ticker)
            if exists:
                type = args[1]
                if type == "add" or type == "a" or type == "remove" or type == "r":
                    updatelist(uuid, type, ticker)
                    await message.channel.send("Added ticker: " + ticker + " to your shortlist.")
                    string = "Your current list includes: "
                    ticklist = user(uuid).tickers
                    for tickers in ticklist:
                        if tickers == ticklist[-1]:
                            string = string + tickers + "."
                        else:
                            string = string + tickers + ", "
                    await message.channel.send(string)

                else:
                    await message.channel.send(
                        "Argument: " + type + "is not a valid argument, please try again. Use $help for a list of "
                                              "arguments.")
            if not exists:
                await message.channel.send("The ticker: " + args[2] + " does not exist.")
        else:
            await message.channel.send("No stock exchange specified.")
    if message.content.startswith("$movers"):
        gprices, gticks, gperchange, gstocknames = getmoversgain()
        lprices, lticks, lperchange, lstocknames = getmoversloss()
        string = ""
        for num in range(5):
            string = string + ":chart_with_upwards_trend: " + gstocknames[num] + "(" + gticks[num] + ") is trending upward; " + gperchange[num] + " for a current value of " + gprices[num] + "\n"
        for num in range(5):
            string = string + ":chart_with_downwards_trend: " + lstocknames[num] + "(" + lticks[num] + ") is trending downward " + lperchange[num] + " for a current value of " + lprices[num] + "\n"
        await message.channel.send(string)

    if message.content.startswith("$help"):
        await message.channel.send(":moneybag: $price: Gives the price of a current stock. (Syntax: $price "
                                   "ticker:exchange) Ticker should include a valid exchange at the end separated by a "
                                   "colon. (':') Another supported argument is 'list' (instead of ticker:exchange) "
                                   "which returns all of the prices on your current shortlist. (example usage: $price "
                                   "NVDA:NASDAQ or $price list)\n \n"
                                   ":chart: $movers: "
                                   "Gives the biggest movers by percent. Returns the "
                                   "5 largest gainers and losers by percent. (Syntax: $movers) Accepts no arguments. "
                                   "\n \n:scroll: $list: Allows you to add or remove stocks from your shortlist. ("
                                   "Syntax: $list type ticker:exchange) Type can be add(add or a is accepted) or "
                                   "remove(remove or r is accepted) and ticker:exchange is a valid ticker and the "
                                   "exchange it is posted on. Your shortlist can be used with the $price command to "
                                   "return "
                                   "the prices of all of the stocks in your shortlist. (example usage: $list add NVDA "
                                   "or $list remove NVDA)")





client.run("token")
