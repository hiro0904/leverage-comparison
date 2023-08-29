import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 配列を渡して、分析する関数
def analysis_data(inputData):
    max_value = np.max(inputData)
    min_value = np.min(inputData)
    first_value = inputData[0]
    last_value = inputData[-1]
    total_price_change = last_value / first_value
    max_price_change = max_value / first_value
    min_price_change = min_value / first_value
    st.write(f"期間内トータルリターン{total_price_change:.3f}")
    st.write("初期価格ベースのmaxとmin")
    st.write(f"max:{max_price_change:.2f} min:{min_price_change:.3f}")


# Streamlitの設定
st.set_page_config(page_title="Stock Price Visualizer", layout="wide")

# ページのタイトル
st.title("Stock Leverage Comparison")

# ユーザーからのティッカー入力
ticker = st.text_input("Enter Ticker Symbol (e.g., SPY)", value="SPY")

# ユーザーからの期間入力
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2023-08-01"))

# Yahoo Financeから株価データを取得
data = yf.download(ticker, start=start_date, end=end_date)

# 終値の配列
closing_prices = data["Close"]

# チャートの表示
# st.subheader("Closing Prices")
# st.line_chart(closing_prices)

# レバレッジ比率の設定
leverageRatio = 3

# 初めの値を調整して配列にする
adjusted_prices = (closing_prices / closing_prices.iloc[0]) * 10000
st.line_chart(adjusted_prices)
analysis_data(adjusted_prices)

# 資金レバレッジ
leverage_prices = adjusted_prices * leverageRatio
st.subheader("資金レバレッジ")
# st.write(leverage_prices)
diff_prices = leverage_prices.diff()
diff_prices.fillna(0, inplace=True)

# st.subheader("差分表示")
# st.write(diff_prices)
# st.subheader("差分合計")
# st.write(np.cumsum(diff_prices))
leverage_equity_base = 10000 + np.cumsum(diff_prices)
st.subheader("自己資本ベースの値動き")
# st.write(leverage_equity_base)
st.line_chart(leverage_equity_base)
analysis_data(leverage_equity_base)
# 変化倍率の計算
price_changes = closing_prices.pct_change() + 1
price_changes.fillna(1, inplace=True)  # 最初の日は変化倍率が1とする

# 変化倍率を3倍する
price_changes_3x = price_changes.apply(lambda x: x ** leverageRatio)

# チャートの表示
# st.subheader("Price Change Multipliers (3x)")
# st.write(price_changes_3x)
# st.line_chart(price_changes_3x)

# 始めを10000にしてから変化倍率3倍チャートを表示
st.subheader("レバレッジETFの値動き")
cumprod_changes = np.cumprod(price_changes_3x)
adjusted_leverageETF = cumprod_changes * 10000
st.line_chart(adjusted_leverageETF)
analysis_data(adjusted_leverageETF)

