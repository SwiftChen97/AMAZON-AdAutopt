import pandas as pd


def sp_product_pause(data):
    """定义第一种暂停广告的条件。"""
    condition1 = (data["点击量"] > 25) & (data["订单数量"] == 0)
    condition2 = (data["订单数量"] < 6) & (data["ACOS"] > 0.60)
    return (condition1 | condition2)