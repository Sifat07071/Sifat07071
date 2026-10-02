def check_setup_5(df):
    """ Setup 5: Support Doji Reversal (CALL) """
    if len(df) < 4: return None
    
    sup = df['low'].rolling(window=20, min_periods=5).min().iloc[-1]
    c1 = df.iloc[-1]  # Doji Candle
    
    body = abs(c1['close'] - c1['open'])
    total_range = c1['high'] - c1['low']
    
    # Doji condition: Body <= 12% of total range
    is_doji = body <= (total_range * 0.12) if total_range > 0 else False
    touches_support = c1['low'] <= sup
    closes_above_support = min(c1['open'], c1['close']) >= sup
    
    if is_doji and touches_support and closes_above_support:
        return "CALL"
    return None
    
