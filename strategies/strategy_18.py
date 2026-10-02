def check_setup_18(df):
    """ Setup 18: Exhaustion Engulfing Reversal (PUT) """
    if len(df) < 5: return None
    
    c1 = df.iloc[-4]  # 1no Green Candle (Large: ~100%)
    c2 = df.iloc[-3]  # 2no Green Candle (Medium: ~60%)
    c3 = df.iloc[-2]  # 3no Green Candle (Small: ~40%)
    c4 = df.iloc[-1]  # 4no Red Engulfing Candle
    
    # Candle Types
    is_c1_green = c1['close'] > c1['open']
    is_c2_green = c2['close'] > c2['open']
    is_c3_green = c3['close'] > c3['open']
    is_c4_red = c4['close'] < c4['open']
    
    if not (is_c1_green and is_c2_green and is_c3_green and is_c4_red):
        return None
        
    # Sizes Calculation
    s1 = abs(c1['close'] - c1['open'])
    s2 = abs(c2['close'] - c2['open'])
    s3 = abs(c3['close'] - c3['open'])
    
    # Conditions: Green candles decreasing in size & 4no candle engulfs 3no candle
    is_decreasing = s1 > s2 > s3
    c4_engulfs_c3 = c4['close'] < c3['open']
    
    if is_decreasing and c4_engulfs_c3:
        return "PUT"
        
    return None
    
