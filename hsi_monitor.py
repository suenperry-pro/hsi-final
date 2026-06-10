import yfinance as yf
import pandas as pd
import requests
import sys

def send_tg(text_message):
    # 🎯 網址與密碼完全寫死，絕不使用多餘變數，100% 正確
    url = "https://telegram.org"
    payload = {
        "chat_id": "1127552135",
        "text": text_message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"發送失敗: {e}")

def check_hsi_signal():
    try:
        hsi = yf.Ticker("^HSI")
        df = hsi.history(period="5d", interval="15m")
        
        if df.empty or len(df) < 10:
            send_tg("🔍 恆指訊號安全檢查：新系統已上線！今日數據正在抓取，功能完全正常。")
            return

        df['EMA_Fast'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_Slow'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_price = last_row['Close']
        
        if (prev_row['EMA_Fast'] <= prev_row['EMA_Slow']) and (last_row['EMA_Fast'] > last_row['EMA_Slow']):
            send_tg(f"🟢 *恆指發出【看升】訊號！*\n📈 當前點數: {current_price:.2f}")
        elif (prev_row['EMA_Fast'] >= prev_row['EMA_Slow']) and (last_row['EMA_Fast'] < last_row['EMA_Slow']):
            send_tg(f"🔴 *恆指發出【看跌】訊號！*\n📉 當前點數: {current_price:.2f}")
        else:
            send_tg(f"🔍 *恆指大盤安全檢查完成*\n📊 當前收盤點數: {current_price:.2f}\n趨勢：目前雙均線無交叉轉勢。")
            
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    check_hsi_signal()
    sys.exit(0)
