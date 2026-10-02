import requests
import time
from threading import Thread
import yfinance as yf

TELEGRAM_BOT_TOKEN = "8828383409:AAGzaDGCz4lQnCEIAUhImFyCnMIVj-0ZNso"
TELEGRAM_CHAT_ID = "6885238220"

# Yahoo Finance compatible Pairs mapping
YAHOO_PAIRS_MAP = {
    "EURUSDT": "EURUSD=X",
    "GBPUSDT": "GBPUSD=X",
    "AUDUSDT": "AUDUSD=X",
    "USDCAD": "USDCAD=X",
    "USDJPY": "USDJPY=X",
    "EURJPY": "EURJPY=X",
    "GBPJPY": "GBPJPY=X",
    "NZDUSDT": "NZDUSD=X",
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "SOLUSDT": "SOL-USD",
    "XRPUSDT": "XRP-USD"
}

def get_yahoo_candles_for_result(symbol):
    try:
        yahoo_symbol = YAHOO_PAIRS_MAP.get(symbol, symbol)
        ticker = yf.Ticker(yahoo_symbol)
        df = ticker.history(period="1d", interval="1m")
        if df is not None and not df.empty:
            return df
    except Exception as e:
        pass
    return None

def track_signal_result(symbol, signal_type, sent_time_str):
    # Quotex 1-Minute expiry এর জন্য ক্যান্ডেল ক্লোজ হওয়ার পর্যন্ত (৬০ সেকেন্ড) অপেক্ষা করা
    time.sleep(60)
    
    try:
        # লেটেস্ট ক্যান্ডেল ডাটা ফেচ করা রেজাল্ট চেক করার জন্য (Yahoo Finance থেকে)
        df = get_yahoo_candles_for_result(symbol=symbol)
        if df is not None and len(df) >= 2:
            # বিগত ক্যান্ডেলটির ওপেন এবং ক্লোজ প্রাইস তুলনা করা
            last_candle = df.iloc[-1]
            open_price = last_candle['Open']
            close_price = last_candle['Close']
            
            # উইন নাকি লস নির্ধারণ লজিক
            if close_price > open_price:
                actual_result = "CALL" # Green Candle
            elif close_price < open_price:
                actual_result = "PUT"  # Red Candle
            else:
                actual_result = "DOJI"
            
            if actual_result == signal_type:
                result_msg = f"✅ **RESULT: WIN 🎉**\n📊 Asset: {symbol}\n⚡ Signal was: {signal_type}"
            elif actual_result == "DOJI":
                result_msg = f"⚪ **RESULT: DOJI (Tie) ⚠️**\n📊 Asset: {symbol}"
            else:
                result_msg = f"❌ **RESULT: LOSS 💔**\n📊 Asset: {symbol}\n⚡ Signal was: {signal_type}"
                
            # টেলিগ্রামে রেজাল্ট মেসেজ পাঠানো
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": result_msg,
                "parse_mode": "Markdown"
            }
            requests.post(url, json=payload)
            
    except Exception as e:
        print(f"Result Tracking Error: {e}")

def send_telegram_signal(symbol, setup_name, signal_type):
    emoji = "🟢 CALL (UP)" if signal_type == "CALL" else "🔴 PUT (DOWN)"
    
    message = (
        f"🚨 **NEW TRADING SIGNAL (Non-OTC)** 🚨\n\n"
        f"📊 **Asset:** {symbol}\n"
        f"🎯 **Strategy:** {setup_name}\n"
        f"⚡ **Direction:** {emoji}\n"
        f"⏱ **Timeframe:** 1 Minute\n\n"
        f"⚠️ *Quotex-এ ক্যান্ডেল শুরু হওয়ার ১-২ সেকেন্ড আগে ট্রেড প্লেস করুন!*"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # সিগন্যাল সফলভাবে যাওয়ার পর ব্যাকগ্রাউন্ডে রেজাল্ট ট্র্যাক করার জন্য থ্রেড রান করা
            t = Thread(target=track_signal_result, args=(symbol, signal_type, time.time()))
            t.daemon = True
            t.start()
            
    except Exception as e:
        print(f"Telegram Alert Error: {e}")
                         
