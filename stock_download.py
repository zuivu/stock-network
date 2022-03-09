import pandas_datareader.data as web
import pandas as pd
import tqdm

def get_stock_close_price(source, col_name, start_day, end_day, result_csv_dir):
    stock_table = pd.read_html(source)[0]
    stock_symbols = sorted(stock_table[col_name].str.replace('.', '-', regex=False).tolist())
    print("Stock symbols:")
    print(stock_symbols, "\n")

    stock_adj_close = {}
    for symbol in tqdm.tqdm(iterable=stock_symbols, desc="Downloaded stocks", total=len(stock_symbols), unit="stock"):
        try:
            stock_adj_close[symbol] = web.DataReader(symbol, 'yahoo', start=start_day, end=end_day, retry_count=5, pause=0.2)["Adj Close"]
        except KeyError:
            try:
                print("\nFirst added date of stock", symbol, "is after the querying start date.", end='')
                stock_adj_close[symbol] = web.DataReader(symbol, 'yahoo', end=end_day, retry_count=5, pause=0.2)["Adj Close"]
                print(" Stock until querying end date:\n", stock_adj_close[symbol], "\n")
            except KeyError:
                print("..and end date. Hence, ignore!\n")

    stock_adj_close_df = pd.DataFrame(stock_adj_close)
    if stock_adj_close_df.index.name != "Date":
        stock_adj_close_df.set_index("Date", inplace=True)

    unadded_stock = set(stock_symbols) - set(list(stock_adj_close_df.columns))
    print("Unadded stocks:", unadded_stock)

    stock_adj_close_df.to_csv(result_csv_dir)
    return stock_adj_close_df

if __name__ == "__main__":
    start_day = "23 Mar, 2020"
    end_day = "03 Jan, 2022"
    source = "https://en.wikipedia.org/wiki/List_of_S%26P_400_companies" # "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    col_name = "Ticker symbol" # "Symbol"
    download_data_name = "sp400-info.csv"
    stock_df = get_stock_close_price(source, col_name, start_day, end_day, download_data_name)
