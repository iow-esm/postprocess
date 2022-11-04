def convert_to_decimal(value):
    if ":" not in value:
        return value
    
    tmp = value.split(":")
    decimal_value = float(tmp[0]) + float(tmp[1])/60.0 + float(tmp[2])/3600.0
    
    return str(decimal_value)