def check_setup_9(df):
    """ Setup 9: 2 Green + Red Engulfing Reversal (CALL) """
    if len(df) < 4: return None
    
    r0 = df.iloc[-4]  # Prior Red Candle
    g1 = df.iloc[-3]  # 1st Green Candle
    g2 = df.iloc[-2]  # 2nd Green Candle
    r3 = df.iloc[-1]  # Large Red Candle
    
    # Color sequence check
    if not (r0['close'] < r0['open'] and g1['close'] > g1['open'] and 
            g2['close'] > g2['open'] and r3['close'] < r3['open']):
        return None
    
    lowest_green = min(g1['open'], g1['close'], g2['open'], g2['close'])
    closes_below_both = r3['close'] < lowest_green
    is_not_gap_down = r3['open'] >= g2['open']  # Fake gap down filter
    
    if closes_below_both and is_not_gap_down:
        return "CALL"
    return None
    
