def check_setup_6(df):
    """ Setup 6: Resistance Doji Reversal (PUT) """
    if len(df) < 4: return None
    
    res = df['high'].rolling(window=20, min_periods=5).max().iloc[-1]
    c1 = df.iloc[-1]  # Doji Candle
    
    body = abs(c1['close'] - c1['open'])
    total_range = c1['high'] - c1['low']
    
    is_doji = body <= (total_range * 0.12) if total_range > 0 else False
    touches_resistance = c1['high'] >= res
    closes_below_resistance = max(c1['open'], c1['close']) <= res
    
    if is_doji and touches_resistance and closes_below_resistance:
        return "PUT"
    return None
    
