import yfinance as yf
import pandas as pd
import sys

def check_hsi_signal():
    try:
        hsi = yf.Ticker("^HSI")
        df = hsi.history(period="5d", interval="15m")
        
        # 為了測試連線，我們今天開機就強行故意報錯，逼手機 GitHub App 彈出通知！
        raise Exception("⚡ 恆指雲端連線成功！微軟原生 App 通道已徹底打通！")

        if df.empty or len(df) < 10:
            return

        df['EMA_Fast'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_Slow'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        current_price = last_row['Close']
        
        # 判斷交叉訊號，一旦轉勢就故意自殺報錯，把訊號直接彈出在手機通知欄！
        if (prev_row['EMA_Fast'] <= prev_row['EMA_Slow']) and (last_row['EMA_Fast'] > last_row['EMA_Slow']):
            raise Exception(f"🟢 恆指均線黃金交叉！【看升】訊號發出！當前點數: {current_price:.2f}")
        elif (prev_row['EMA_Fast'] >= prev_row['EMA_Slow']) and (last_row['EMA_Fast'] < last_row['EMA_Slow']):
            raise Exception(f"🔴 恆指均線死亡交叉！【看跌】訊號發出！當前點數: {current_price:.2f}")
        else:
            print("目前均線平穩，無交叉。")
            
    except Exception as e:
        # 把錯誤訊息往上拋，強行激活 GitHub App 的手機警報通知！
        raise RuntimeError(str(e))

if __name__ == "__main__":
    check_hsi_signal()
