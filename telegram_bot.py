import threading
import time
import ccxt
import requests

# আপনার টেলিগ্রাম বট টোকেন এবং চ্যাট আইডি
TELEGRAM_BOT_TOKEN = "8828383409:AAGzaDGCz4lQnCEIAUhImFyCnMIVj-0ZNso"
TELEGRAM_CHAT_ID = "6885238220"

# বাইন্যান্স ফিউচার্স এক্সচেঞ্জ কানেকশন (ডেটা চেক করার জন্য)
exchange = ccxt.binance({
    'options': {'defaultType': 'future'},
    'enableRateLimit': True,
})


def get_binance_candles_for_result(symbol):
  """বাইন্যান্স ফিউচার্স থেকে সিগন্যালের রেজাল্ট চেক করার জন্য ১ মিনিটের ক্যান্ডেল ডেটা আনা"""
  try:
    # ১ মিনিটের ক্যান্ডেল অনুযায়ী ফিউচার্স ডেটা ফেচ করা
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=5)
    if ohlcv and len(ohlcv) >= 2:
      # শেষ ক্লোজ হওয়া ক্যান্ডেলটি নেওয়ার জন্য
      last_candle = ohlcv[-2]
      # format: [timestamp, open, high, low, close, volume]
      return last_candle[1], last_candle[4]  # Open price, Close price
  except Exception as e:
    print(f"Binance Result Fetch Error: {e}")
  return None, None


def track_signal_result(symbol, signal_type):
  # ১ মিনিটের ক্যান্ডেলের জন্য ৬০ সেকেন্ড অপেক্ষা করা
  time.sleep(60)

  try:
    open_price, close_price = get_binance_candles_for_result(symbol)

    if open_price is not None and close_price is not None:
      # উইন নাকি লস নির্ধারণ লজিক (আপ/ডাউন অনুযায়ী)
      if close_price > open_price:
        actual_result = 'CALL'  # সবুজ ক্যান্ডেল (UP)
      elif close_price < open_price:
        actual_result = 'PUT'  # লাল ক্যান্ডেল (DOWN)
      else:
        actual_result = 'DOJI'

      if actual_result == signal_type:
        result_msg = (
            f'✅ **BINANCE RESULT: WIN 🎉**\n📊 Pair: `{symbol}`\n⚡ Signal was:'
            f' `{signal_type}`'
        )
      elif actual_result == 'DOJI':
        result_msg = (
            f'⚪ **BINANCE RESULT: DOJI (Tie) ⚠️**\n📊 Pair: `{symbol}`'
        )
      else:
        result_msg = (
            f'❌ **BINANCE RESULT: LOSS 💔**\n📊 Pair: `{symbol}`\n⚡ Signal was:'
            f' `{signal_type}`'
        )

      # টেলিগ্রামে রেজাল্ট পাঠানো
      url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
      payload = {
          'chat_id': TELEGRAM_CHAT_ID,
          'text': result_msg,
          'parse_mode': 'Markdown',
      }
      requests.post(url, json=payload)

  except Exception as e:
    print(f"Result Tracking Error: {e}")


def send_telegram_signal(symbol, setup_name, signal_type):
  """বট যখনই সিগন্যাল পাবে, তা টেলিগ্রামে পাঠাবে এবং রেজাল্ট ট্র্যাক করবে"""
  emoji = '🟢 LONG (CALL)' if signal_type == 'CALL' else '🔴 SHORT (PUT)'

  message = (
      f'🚨 **BINANCE FUTURES SIGNAL (1m)** 🚨\n\n'
      f'📊 **Pair:** `{symbol}`\n'
      f'🎯 **Strategy:** `{setup_name}`\n'
      f'⚡ **Direction:** {emoji}\n'
      f'⏱ **Timeframe:** 1 Minute\n\n'
      f'⚠️ *Binance Futures এ অটোমেটিক এক্সিকিউট হচ্ছে!*'
  )

  url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
  payload = {
      'chat_id': TELEGRAM_CHAT_ID,
      'text': message,
      'parse_mode': 'Markdown',
  }

  try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
      # ব্যাকগ্রাউন্ডে রেজাল্ট ট্র্যাক করার জন্য থ্রেড চালু করা
      t = threading.Thread(
          target=track_signal_result, args=(symbol, signal_type)
      )
      t.daemon = True
      t.start()

  except Exception as e:
    print(f'Telegram Alert Error: {e}')
      
