def check_setup_17(df):
    """ Setup 17: Exhaustion Engulfing Reversal (CALL) """
    if len(df) < 5: return None
    
    c1 = df.iloc[-4]  # 1no Red Candle (Large: ~100%)
    c2 = df.iloc[-3]  # 2no Red Candle (Medium: ~60%)
    c3 = df.iloc[-2]  # 3no Red Candle (Small: ~40%)
    c4 = df.iloc[-1]  # 4no Green Engulfing Candle
    
    # Candle Types
    is_c1_red = c1['close'] < c1['open']
    is_c2_red = c2['close'] < c2['open']
    is_c3_red = c3['close'] < c3['open']
    is_c4_green = c4['close'] > c4['open']
    
    if not (is_c1_red and is_c2_red and is_c3_red and is_c4_green):
        return None
        
    # Sizes Calculation
    s1 = abs(c1['close'] - c1['open'])
    s2 = abs(c2['close'] - c2['open'])
    s3 = abs(c3['close'] - c3['open'])
    
    # Conditions: Red candles decreasing in size & 4no candle engulfs 3no candle
    is_decreasing = s1 > s2 > s3
    c4_engulfs_c3 = c4['close'] > c3['open']
    
    if is_decreasing and c4_engulfs_c3:
        return "CALL"
        
    return None
    
