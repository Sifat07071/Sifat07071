def check_setup_8(df):
    """ Setup 8: False Support Breakout Fakeout (PUT) """
    if len(df) < 5: return None
    
    sup = df['low'].iloc[:-3].rolling(window=20, min_periods=5).min().iloc[-1]
    
    c1 = df.iloc[-3]  # 1no Red Candle breaking Support
    c2 = df.iloc[-2]  # 2no Red Candle
    c3 = df.iloc[-1]  # 3no Green Candle
    
    is_c1_red = c1['close'] < c1['open'] and c1['close'] < sup
    is_c2_red = c2['close'] < c2['open']
    is_c3_green = c3['close'] > c3['open']
    
    engulfs_c2 = c3['close'] > c2['open']
    touches_sup = c3['high'] >= sup
    closes_below_sup = c3['close'] <= sup
    
    if is_c1_red and is_c2_red and is_c3_green and engulfs_c2 and touches_sup and closes_below_sup:
        return "PUT"
    return None
    
