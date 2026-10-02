def check_setup_16(df):
    """ Setup 16: Box Resistance Sweep Reversal (PUT) """
    if len(df) < 8: return None
    
    # Box formation (Consolidation Resistance Level)
    box_candles = df.iloc[-7:-4]
    box_high = box_candles['high'].max()
    
    c_prev = df.iloc[-2] # Previous candle (Market moves down)
    c_last = df.iloc[-1] # Last candle sweeping liquidity
    
    # Candle Types
    is_c_prev_red = c_prev['close'] < c_prev['open']
    is_c_last_green = c_last['close'] > c_last['open']
    
    if not (is_c_prev_red and is_c_last_green):
        return None
        
    # Condition: Last green candle breaks and closes above box resistance level
    c_last_sweeps_resistance = c_last['close'] > box_high
    
    if c_last_sweeps_resistance:
        return "PUT"
        
    return None
    
