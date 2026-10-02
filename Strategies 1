def check_setup_1(df):
    """ Setup 1: Resistance Breakout (CALL) """
    if len(df) < 6: return None
    
    # Resistance Level Calculation
    res = df['high'].iloc[:-2].rolling(window=20, min_periods=5).max().iloc[-1]
    
    c1 = df.iloc[-2]  # 1no Red Candle
    c2 = df.iloc[-1]  # 2no Green Breakout Candle
    
    # 1no Red candle touches/respects Resistance
    is_c1_red = c1['close'] < c1['open']
    c1_touches_res = c1['high'] >= res and c1['close'] < res
    
    # 2no Green candle breaks Resistance
    is_c2_green = c2['close'] > c2['open']
    c2_breaks_res = c2['close'] > res and c2['open'] < res
    
    if is_c1_red and c1_touches_res and is_c2_green and c2_breaks_res:
        return "CALL"
    return None
    
