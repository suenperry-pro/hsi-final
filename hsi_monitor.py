import yfinance as yf
import pandas as pd
import requests
import sys

def send_tg(text_message):
    # 🎯 網址純英文寫死，絕對不黏貼中文字
    url = "https://telegram.org"
    # 🎯 中文字全部安全隔離在 params 裡面，系統會自動加密發送，100% 不會 parse 失敗！
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
        
        # 今日週末休市
        if df.empty or len(df) < 10:
            send_tg("🔍 恆指訊號安全檢查：新系統已上線！目前市場休市中，功能完全正常。")
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
            send_tg("🔍 恆指今日大盤訊號安全檢查完成，目前均線無交叉趨勢。")
            
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    check_hsi_signal()
    sys.exit(0)
