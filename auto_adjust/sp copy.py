import pandas as pd

class SPModule:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """从包含'商品推广'的工作表名称中加载数据。"""
        try:
            xls = pd.ExcelFile(self.file_path)
            sheet_name = next((name for name in xls.sheet_names if "商品推广" in name), None)
            if sheet_name:
                print(f"加载数据来自工作表: {sheet_name}")
                return pd.read_excel(xls, sheet_name=sheet_name, engine="openpyxl")
            else:
                print("未找到匹配的工作表。")
                return None
        except Exception as e:
            print(f"加载数据出错: {e}")
            return None

    def _get_pause_conditions(self):
        """定义暂停广告的条件。"""
        if self.data is None:
            return pd.Series([False] * len(self.data))  # 无数据时返回False的序列

        condition1 = (self.data["点击量"] > 25) & (self.data["订单数量"] == 0)
        condition2 = (self.data["订单数量"] < 6) & (self.data["ACOS"] > 60)
        return (condition1 | condition2)

    def pause_ad(self):
        """根据特定条件暂停广告，并仅保存修改后的行到新文件。"""
        if self.data is None:
            print("数据未加载。")
            return

        # 筛选符合暂停条件的广告
        to_pause = self.data[
            (self.data["广告活动状态（仅供参考）"] == "已启用") &
            (self.data["广告组状态（仅供参考）"] == "已启用") &
            (self.data["状态"] == "已启用") &
            (self.data["SKU"].notna()) &
            self._get_pause_conditions()
        ]

        # 检查是否有符合条件的行需要暂停
        if not to_pause.empty:
            # 将符合条件的行的 "状态" 标记为 "已暂停"
            self.data.loc[to_pause.index, "状态"] = "已暂停"

            # 提取仅包含修改后的行
            modified_rows = self.data.loc[to_pause.index]

            # 仅保存修改后的行到新文件
            output_file_path = self.file_path.replace(".xlsx", "_SP_Product.xlsx")
            try:
                modified_rows.to_excel(output_file_path, index=False, engine="openpyxl")
                print(f"包含修改行的文件已保存为: {output_file_path}")
            except Exception as e:
                print(f"保存更新文件出错: {e}")
        else:
            print("没有符合条件的广告需要暂停。")

    def call_function(self, function_name):
        """通过名称动态调用函数。"""
        func = getattr(self, function_name, None)
        if callable(func):
            func()
        else:
            print(f"未找到函数 '{function_name}'。")