import numpy as np

def clean_data(df, out_df_dir=""):
    df.dropna(axis=1, inplace=True)
    
    if out_df_dir:
        df.to_csv(out_df_dir)

    return df

def log_change(series):
    return np.log(series[1]/series[0])

def calculate_cor(df):
    return df.rolling(
        window=2,
        min_periods=2
    ).apply(
        log_change,
        raw=True
    ).corr(method='pearson')
