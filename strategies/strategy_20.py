def check_setup_20(df):
    """ Setup 20: Trend Continuation Setup (PUT) """
    if len(df) < 5: return None
    
    c_trend = df.iloc[-3] # Downtrend Candle
    c1 = df.iloc[-2]      # 1no Green Candle
    c2 = df.iloc[-1]      # 2no Red Inside Candle
    
    # Candle Types
    is_c_trend_red = c_trend['close'] < c_trend['open']
    is_c1_green = c1['close'] > c1['open']
    is_c2_red = c2['close'] < c2['open']
    
    if not (is_c_trend_red and is_c1_green and is_c2_red):
        return None
        
    # Condition: 2no Red candle stays inside 1no Green candle's body (no breakout of c1 body)
    c2_inside_c1 = c2['close'] > c1['open'] and c2['open'] < c1['close']
    
    if c2_inside_c1:
        return "PUT"
        
    return None
    
