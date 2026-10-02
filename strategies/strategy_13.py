def check_setup_13(df):
    """ Setup 13: Breakout Retest Setup (CALL) """
    if len(df) < 6: return None
    
    # SNR Resistance Level Calculation
    res = df['high'].iloc[:-2].rolling(window=20, min_periods=5).max().iloc[-1]
    
    c1 = df.iloc[-2]  # 1no Green Breakout Candle
    c2 = df.iloc[-1]  # 2no Red Retest Candle
    
    # Candle Types
    is_c1_green = c1['close'] > c1['open']
    is_c2_red = c2['close'] < c2['open']
    
    if not (is_c1_green and is_c2_red):
        return None
        
    # Conditions
    c1_breaks_res = c1['close'] > res and c1['open'] < res
    c2_retests_res = c2['low'] <= res and c2['close'] > res
    
    if c1_breaks_res and c2_retests_res:
        return "CALL"
        
    return None
    
