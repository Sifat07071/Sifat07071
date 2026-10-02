def check_setup_12(df):
    """ Setup 12: Fake Breakout Reversal (PUT) """
    if len(df) < 6: return None
    
    c1 = df.iloc[-4]  # 1no Green Candle
    c2 = df.iloc[-3]  # 2no Small Green Candle
    c3 = df.iloc[-2]  # 3no Red Engulfing Candle
    c4 = df.iloc[-1]  # 4no Retest Green Candle
    
    # Candle Types
    is_c1_green = c1['close'] > c1['open']
    is_c2_green = c2['close'] > c2['open']
    is_c3_red = c3['close'] < c3['open']
    is_c4_green = c4['close'] > c4['open']
    
    if not (is_c1_green and is_c2_green and is_c3_red and is_c4_green):
        return None
        
    sup_level = c1['open']
    
    # Conditions
    c2_body = abs(c2['close'] - c2['open'])
    c1_body = abs(c1['close'] - c1['open'])
    c2_has_wicks = (c2['high'] > max(c2['open'], c2['close'])) and (c2['low'] < min(c2['open'], c2['close']))
    
    c2_valid = c2_body < c1_body and c2_has_wicks
    c3_engulfs = c3['close'] < c1['low']
    c4_retests = c4['high'] >= sup_level and c4['close'] < sup_level
    
    if c2_valid and c3_engulfs and c4_retests:
        return "PUT"
        
    return None
    
