def transform_dict(obj):
    data = vars(obj).copy()
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = [vars(v) for v in value]
        elif hasattr(value, "__dict__"):
            data[key] = vars(value)
    return data
