def check_setup_2(df):
    """ Setup 2: Support Breakout (PUT) """
    if len(df) < 6: return None
    
    # Support Level Calculation
    sup = df['low'].iloc[:-2].rolling(window=20, min_periods=5).min().iloc[-1]
    
    c1 = df.iloc[-2]  # 1no Green Candle
    c2 = df.iloc[-1]  # 2no Red Breakout Candle
    
    # 1no Green candle touches Support
    is_c1_green = c1['close'] > c1['open']
    c1_touches_sup = c1['low'] <= sup and c1['close'] > sup
    
    # 2no Red candle breaks Support
    is_c2_red = c2['close'] < c2['open']
    c2_breaks_sup = c2['close'] < sup and c2['open'] > sup
    
    if is_c1_green and c1_touches_sup and is_c2_red and c2_breaks_sup:
        return "PUT"
    return None
    
