import pandas as pd


def sp_product_pause_filters(data, pause_conditions_func):
    """根据指定的暂停条件函数和其他通用条件筛选出需要暂停的广告。"""
    return data[
        (data["广告活动状态（仅供参考）"] == "已启用") &
        (data["广告组状态（仅供参考）"] == "已启用") &
        (data["状态"] == "已启用") &
        (data["SKU"].notna()) &
        pause_conditions_func(data)
    ]