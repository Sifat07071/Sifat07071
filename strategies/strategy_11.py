def check_setup_11(df):
    """ Setup 11: Fake Breakout Reversal (CALL) """
    if len(df) < 6: return None
    
    c1 = df.iloc[-4]  # 1no Red Candle
    c2 = df.iloc[-3]  # 2no Small Red Candle
    c3 = df.iloc[-2]  # 3no Green Engulfing Candle
    c4 = df.iloc[-1]  # 4no Retest Red Candle
    
    # Candle Types
    is_c1_red = c1['close'] < c1['open']
    is_c2_red = c2['close'] < c2['open']
    is_c3_green = c3['close'] > c3['open']
    is_c4_red = c4['close'] < c4['open']
    
    if not (is_c1_red and is_c2_red and is_c3_green and is_c4_red):
        return None
        
    res_level = c1['open']
    
    # Conditions
    c2_body = abs(c2['close'] - c2['open'])
    c1_body = abs(c1['close'] - c1['open'])
    c2_has_wicks = (c2['high'] > max(c2['open'], c2['close'])) and (c2['low'] < min(c2['open'], c2['close']))
    
    c2_valid = c2_body < c1_body and c2_has_wicks
    c3_engulfs = c3['close'] > c1['high']
    c4_retests = c4['low'] <= res_level and c4['close'] > res_level
    
    if c2_valid and c3_engulfs and c4_retests:
        return "CALL"
        
    return None
    
