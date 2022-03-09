import pandas_datareader.data as web
import pandas as pd
import tqdm

start_day = "23 Mar, 2020"
end_day = "03 Jan, 2022"

# The first table on the Wikipedia page is the S&P 500 component stocks.
# The second one is the selected changes to the list of S&P 500 components.
wiki_link = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

sp_500_table = pd.read_html(wiki_link)[0]
sp_500_symbols = sorted(sp_500_table['Symbol'].str.replace('.', '-', regex=False).tolist())
print("S&P 500 stock symbols:")
print(sp_500_symbols, "\n")

sp_500_adj_close = {}
for symbol in tqdm.tqdm(iterable=sp_500_symbols, desc="Downloaded stocks", total=len(sp_500_symbols), unit="stock"):
    try:
        sp_500_adj_close[symbol] = web.DataReader(symbol, 'yahoo', start=start_day, end=end_day, retry_count=5, pause=0.2)["Adj Close"]
    except KeyError:
        try:
            print("\nFirst added date of stock", symbol, "is after the querying start date.", end='')
            sp_500_adj_close[symbol] = web.DataReader(symbol, 'yahoo', end=end_day, retry_count=5, pause=0.2)["Adj Close"]
            print(" Stock until querying end date:\n", sp_500_adj_close[symbol], "\n")
        except KeyError:
            print("..and end date. Hence, ignore!\n")

sp_500_adj_close_df = pd.DataFrame(sp_500_adj_close)
if sp_500_adj_close_df.index.name != "Date":
    sp_500_adj_close_df.set_index("Date", inplace=True)

unadded_stock = set(sp_500_symbols) - set(list(sp_500_adj_close_df.columns))
print("Unadded stocks:", unadded_stock)

sp_500_adj_close_df.to_csv("sp500-info.csv")
