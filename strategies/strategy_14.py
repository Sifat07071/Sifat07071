def check_setup_14(df):
    """ Setup 14: Breakout Retest Setup (PUT) """
    if len(df) < 6: return None
    
    # SNR Support Level Calculation
    sup = df['low'].iloc[:-2].rolling(window=20, min_periods=5).min().iloc[-1]
    
    c1 = df.iloc[-2]  # 1no Red Breakout Candle
    c2 = df.iloc[-1]  # 2no Green Retest Candle
    
    # Candle Types
    is_c1_red = c1['close'] < c1['open']
    is_c2_green = c2['close'] > c2['open']
    
    if not (is_c1_red and is_c2_green):
        return None
        
    # Conditions
    c1_breaks_sup = c1['close'] < sup and c1['open'] > sup
    c2_retests_sup = c2['high'] >= sup and c2['close'] < sup
    
    if c1_breaks_sup and c2_retests_sup:
        return "PUT"
        
    return None
    
