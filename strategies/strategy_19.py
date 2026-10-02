def check_setup_19(df):
    """ Setup 19: Trend Continuation Setup (CALL) """
    if len(df) < 5: return None
    
    c_trend = df.iloc[-3] # Uptrend Candle
    c1 = df.iloc[-2]      # 1no Red Candle
    c2 = df.iloc[-1]      # 2no Green Inside Candle
    
    # Candle Types
    is_c_trend_green = c_trend['close'] > c_trend['open']
    is_c1_red = c1['close'] < c1['open']
    is_c2_green = c2['close'] > c2['open']
    
    if not (is_c_trend_green and is_c1_red and is_c2_green):
        return None
        
    # Condition: 2no Green candle stays inside 1no Red candle's body (no breakout of c1 body)
    c2_inside_c1 = c2['close'] < c1['open'] and c2['open'] > c1['close']
    
    if c2_inside_c1:
        return "CALL"
        
    return None
    
