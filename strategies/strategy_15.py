def check_setup_15(df):
    """ Setup 15: Box Support Liquidity Sweep Reversal (CALL) """
    if len(df) < 8: return None
    
    # Box formation (Consolidation Support Base)
    box_candles = df.iloc[-7:-4]
    box_low = box_candles['low'].min()
    
    c_prev = df.iloc[-2] # Previous candle (Market moves up)
    c_last = df.iloc[-1] # Last candle sweeping liquidity
    
    # Candle Types
    is_c_prev_green = c_prev['close'] > c_prev['open']
    is_c_last_red = c_last['close'] < c_last['open']
    
    if not (is_c_prev_green and is_c_last_red):
        return None
        
    # Condition: Last red candle breaks and closes below box support level
    c_last_sweeps_support = c_last['close'] < box_low
    
    if c_last_sweeps_support:
        return "CALL"
        
    return None
    
