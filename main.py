import time
from datetime import datetime
import yfinance as yf
from telegram_bot import send_telegram_signal

# 1 theke 20 shob setup-er unified import
from strategies.strategies.strategy_1 import check_setup_1
from strategies.strategies.strategy_2 import check_setup_2
from strategies.strategies.strategy_3 import check_setup_3
from strategies.strategies.strategy_4 import check_setup_4
from strategies.strategies.strategy_5 import check_setup_5
from strategies.strategies.strategy_6 import check_setup_6
from strategies.strategies.strategy_7 import check_setup_7
from strategies.strategies.strategy_8 import check_setup_8
from strategies.strategies.strategy_9 import check_setup_9
from strategies.strategies.strategy_10 import check_setup_10
from strategies.strategies.strategy_11 import check_setup_11
from strategies.strategies.strategy_12 import check_setup_12
from strategies.strategies.strategy_13 import check_setup_13
from strategies.strategies.strategy_14 import check_setup_14
from strategies.strategies.strategy_15 import check_setup_15
from strategies.strategies.strategy_16 import check_setup_16
from strategies.strategies.strategy_17 import check_setup_17
from strategies.strategies.strategy_18 import check_setup_18
from strategies.strategies.strategy_19 import check_setup_19
from strategies.strategies.strategy_20 import check_setup_20

STRATEGY_LIST = [
    ("Setup 1", check_setup_1),   
    ("Setup 2", check_setup_2),
    ("Setup 3", check_setup_3),   
    ("Setup 4", check_setup_4),
    ("Setup 5", check_setup_5),   
    ("Setup 6", check_setup_6),
    ("Setup 7", check_setup_7),   
    ("Setup 8", check_setup_8),
    ("Setup 9", check_setup_9),   
    ("Setup 10", check_setup_10),
    ("Setup 11", check_setup_11), 
    ("Setup 12", check_setup_12),
    ("Setup 13", check_setup_13), 
    ("Setup 14", check_setup_14),
    ("Setup 15", check_setup_15), 
    ("Setup 16", check_setup_16),
    ("Setup 17", check_setup_17), 
    ("Setup 18", check_setup_18),
    ("Setup 19", check_setup_19), 
    ("Setup 20", check_setup_20)
]

# Yahoo Finance compatible 12 Pairs (Forex er jonno =X ebong Crypto er jonno -USD)
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

def get_yahoo_candles(symbol):
    try:
        yahoo_symbol = YAHOO_PAIRS_MAP.get(symbol, symbol)
        ticker = yf.Ticker(yahoo_symbol)
        df = ticker.history(period="1d", interval="1m")
        if df is not None and not df.empty:
            return df
    except Exception as e:
        pass
    return None

def scan_all_strategies(df):
    for setup_name, func in STRATEGY_LIST:
        try:
            signal = func(df)
            if signal in ["CALL", "PUT"]:
                return setup_name, signal
        except Exception:
            continue
    return None, None

def start_bot():
    print("🤖 24/7 Yahoo Finance Live Scanning Bot Started...")
    print(f"📊 Monitoring {len(YAHOO_PAIRS_MAP)} pairs with 20 setups.")
    last_scanned_minute = -1

    while True:
        try:
            now = datetime.now()
            second = now.second
            minute = now.minute

            # Proti minute-er thik 58-th second-e scan korbe
            if second == 58 and minute != last_scanned_minute:
                last_scanned_minute = minute
                print(f"\n🔍 Scanning Market at {now.strftime('%H:%M:%S')}...")

                for symbol in YAHOO_PAIRS_MAP.keys():
                    try:
                        df = get_yahoo_candles(symbol=symbol)
                        
                        if df is not None and not df.empty:
                            setup_name, signal = scan_all_strategies(df)
                            
                            if signal:
                                print(f"✅ MATCH FOUND! [{symbol}] - {setup_name} -> {signal}")
                                send_telegram_signal(symbol, setup_name, signal)
                    except Exception as pair_err:
                        print(f"⚠️ Error scanning {symbol}: {pair_err}")
                
                time.sleep(3)

            time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped manually.")
            break
        except Exception as global_err:
            print(f"⚠️ Unexpected error in main loop: {global_err}")
            time.sleep(1)

if __name__ == "__main__":
    start_bot()
        
