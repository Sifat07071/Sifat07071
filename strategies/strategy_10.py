def check_setup_10(df):
    """ Setup 10: 2 Red + Green Engulfing Reversal (PUT) """
    if len(df) < 4: return None
    
    g0 = df.iloc[-4]  # Prior Green Candle
    r1 = df.iloc[-3]  # 1st Red Candle
    r2 = df.iloc[-2]  # 2nd Red Candle
    g3 = df.iloc[-1]  # Large Green Candle
    
    # Color sequence check
    if not (g0['close'] > g0['open'] and r1['close'] < r1['open'] and 
            r2['close'] < r2['open'] and g3['close'] > g3['open']):
        return None
    
    highest_red = max(r1['open'], r1['close'], r2['open'], r2['close'])
    closes_above_both = g3['close'] > highest_red
    is_not_gap_up = g3['open'] <= r2['open']  # Fake gap up filter
    
    if closes_above_both and is_not_gap_up:
        return "PUT"
    return None
    
