from binance import Client
import Constants as c
import pandas as pd
import numpy as np
import talib
from binance.enums import *
import time



def createDataFrame (client) :
 klines = client.get_historical_klines("BTCEUR", Client.KLINE_INTERVAL_3MINUTE, "1 hour ago UTC")
 df = pd.DataFrame(klines)
# name columns
 df.columns = ['Time', 'BTCEUR', '1', '2', '3', '4',"5","6","7","8","9","10"]
 # clean unneccesary data from dataframe
 for a in range (1,11) :
      string=  str(a)
      df.pop(string)
 return df



def calculateRSI (DataFrame,client): # calculates rsi and buys or sells depending on rsi
 openings = DataFrame.pop('BTCEUR')
 np_openings = np.array(openings)
 np_openings=np.ndarray.astype(np_openings, dtype=float)
 rsi = talib.RSI(np_openings,c.RSIPERIOD)
 aktuel_rsi = rsi[-1] #get the last element of the array
 if aktuel_rsi >= c.RSIOVERBOUGHT : # indicates we should sell
     if c.in_position:
         print("Selling because its  overbought right now")
         client.create_order(symbol='BTCEUR', side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=c.QUANTITY)
         c.in_position = False
     print("its overbought but we already sold waiting to buy")
 if aktuel_rsi< c.RSIOVERSOLD : # indicates we should buy
     if c.in_position== False :
         print("Buying some crypto becuase its oversold right now")
         client.create_order(symbol='BTCEUR', side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=c.QUANTITY)
         c.in_position = True
     else :
      print("its oversold but we  are already waiting to sell")
      print(aktuel_rsi)
 else :
     print("not buying nor selling")
     print(aktuel_rsi)



if __name__ == "__main__" :
    # create client with API keys from your own binance account
    client = Client(c.API_KEY, c.SECRET_KEY)
    while True:
        print("hello")
        df = createDataFrame(client)
        calculateRSI(DataFrame=df,client=client)
        time.sleep(180)
