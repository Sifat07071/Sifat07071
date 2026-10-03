import ccxt

# আপনার বাইন্যান্সের অরিজিনাল এপিআই কি এবং সিক্রেট কোড এখানে বসিয়ে দিন
BINANCE_API_KEY = "JRBhGm1EE3NJGNfRNY8oYJAmd14hptYCn3swXY3M9wQ4ycTCtyUC3SRUbDULhO0V"
BINANCE_SECRET_KEY = "80Yzz8LCOR6YCYrBSk8z3Z8LEoGRDo08mzxTaV3sDVtyWyt3X3bZVo9J5ab79BkF"

# বাইন্যান্স ফিউচার্স এক্সচেঞ্জ কানেকশন ইনিশিয়ালাইজ করা
exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET_KEY,
    'options': {'defaultType': 'future'},  # ফিউচার্স ট্রেডিং মোড
    'enableRateLimit': True,  # রেট লিমিট প্রটেকশন
})


def set_leverage(symbol, leverage=10):
  """নির্দিষ্ট পেয়ারে লেভারেজ সেট করার ফাংশন"""
  try:
    formatted_symbol = symbol.replace('/', '')
    exchange.fapiPrivate_post_leverage({
        'symbol': formatted_symbol,
        'leverage': leverage,
    })
  except Exception:
    pass


def get_binance_futures_candles(symbol, timeframe='10m', limit=100):
  """বাইন্যান্স ফিউচার্স থেকে লাইভ ক্যান্ডেল ডেটা ফেচ করার ফাংশন"""
  try:
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    if ohlcv:
      import pandas as pd

      df = pd.DataFrame(
          ohlcv,
          columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'],
      )
      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
      return df
  except Exception:
    pass
  return None
