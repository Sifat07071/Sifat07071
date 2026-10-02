def check_setup_7(df):
    """ Setup 7: False Resistance Breakout Fakeout (CALL) """
    if len(df) < 5: return None
    
    res = df['high'].iloc[:-3].rolling(window=20, min_periods=5).max().iloc[-1]
    
    c1 = df.iloc[-3]  # 1no Green Candle breaking Resistance
    c2 = df.iloc[-2]  # 2no Green Candle
    c3 = df.iloc[-1]  # 3no Red Candle
    
    is_c1_green = c1['close'] > c1['open'] and c1['close'] > res
    is_c2_green = c2['close'] > c2['open']
    is_c3_red = c3['close'] < c3['open']
    
    engulfs_c2 = c3['close'] < c2['open']
    touches_res = c3['low'] <= res
    closes_above_res = c3['close'] >= res
    
    if is_c1_green and is_c2_green and is_c3_red and engulfs_c2 and touches_res and closes_above_res:
        return "CALL"
    return None
    
