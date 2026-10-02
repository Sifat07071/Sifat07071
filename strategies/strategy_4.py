def check_setup_4(df):
    """ Setup 4: Exhaustion Green Candle Reversal (PUT) """
    if len(df) < 4: return None
    
    c1, c2, c3, c4 = df.iloc[-4], df.iloc[-3], df.iloc[-2], df.iloc[-1]
    
    # 4-ti Green Candle hote hobe
    if not (c1['close'] > c1['open'] and c2['close'] > c2['open'] and 
            c3['close'] > c3['open'] and c4['close'] > c4['open']):
        return None
    
    s1 = abs(c1['close'] - c1['open'])
    s2 = abs(c2['close'] - c2['open'])
    s3 = abs(c3['close'] - c3['open'])
    s4 = abs(c4['close'] - c4['open'])
    
    combined_size = s1 + s2 + s3
    if 0.85 * combined_size <= s4 <= 1.25 * combined_size:
        return "PUT"
    return None
    
