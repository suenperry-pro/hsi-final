import yfinance as yf
import pandas as pd
import requests
import sys

def check_hsi_signal():
    try:
        hsi = yf.Ticker("^HSI")
        df = hsi.history(period="5d", interval="15m")
        
        # 今日週末休市，直接發送通知
        if df.empty or len(df) < 10:
            url = "https://telegram.org🔍 恆指訊號安全檢查：新系統已上線！目前市場休市中，功能完全正常。"
            requests.post(url, timeout=10)
            return

        df['EMA_Fast'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_Slow'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_price = last_row['Close']
        
        if (prev_row['EMA_Fast'] <= prev_row['EMA_Slow']) and (last_row['EMA_Fast'] > last_row['EMA_Slow']):
            url = f"https://telegram.org🟢 恆指發出【看升】訊號！ 當前點數: {current_price:.2f}"
            requests.post(url, timeout=10)
        elif (prev_row['EMA_Fast'] >= prev_row['EMA_Slow']) and (last_row['EMA_Fast'] < last_row['EMA_Slow']):
            url = f"https://telegram.org🔴 恆指發出【看跌】訊號！ 當前點數: {current_price:.2f}"
            requests.post(url, timeout=10)
        else:
            url = "https://telegram.org🔍 恆指大盤訊號安全檢查完成，目前均線無交叉。"
            requests.post(url, timeout=10)
            
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    check_hsi_signal()
    sys.exit(0)
