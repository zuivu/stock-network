import pandas_datareader.data as web
import pandas as pd
import tqdm
import datetime

start_time = "23 Mar, 2020 13:00:05 +0000"
end_time = "03 Jan, 2022 13:00:05 +0000"

interval = [start_time, end_time]

interval_object = [datetime.datetime.strptime(date, "%d %b, %Y %H:%M:%S %z") for date in interval]
interval_timestamp = [int(datetime.datetime.timestamp(date_object)) for date_object in interval_object]

# def get_close(symbol):
#     print(web.DataReader(symbol, 'yahoo', "23 Mar, 2020 13:00:05 +0000", "25 Mar, 2020 13:00:05 +0000")["Adj Close"].values)
#     return web.DataReader(symbol, 'yahoo', "23 Mar, 2020 13:00:05 +0000", "25 Mar, 2020 13:00:05 +0000")["Adj Close"].values

# The first table on the Wikipedia page is the S&P 500 component stocks.
# The second one is the selected changes to the list of S&P 500 components.
wiki_link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

sp_500_table = pd.read_html(wiki_link)[0]
sp_500_symbols = sp_500_table['Symbol'].str.replace('.', '-', regex=False).values.tolist()
sp_500_adj_close= {}
for symbol in tqdm.tqdm(iterable=sp_500_symbols, desc="Get stock done", total=len(sp_500_symbols), unit="stock"):
    try:
        sp_500_adj_close[symbol] = web.DataReader(symbol, 'yahoo', start="2020-03-23", end="2022-01-03", retry_count=5, pause=0.2)["Adj Close"]
    except:
        print(symbol)
        sp_500_adj_close[symbol] = web.DataReader(symbol, 'yahoo', retry_count=5, pause=0.2)["Adj Close"]

df = pd.DataFrame(sp_500_adj_close)
print(df)
df.to_csv('S&P500-info.csv')

# df.to_csv('S&P500-Info.csv')