import os
import pandas as pd
import conditions.condition as con
import conditions.filters as filter
from openpyxl import load_workbook
from openpyxl.styles import numbers


class SPModule:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data()  # 直接调用加载数据方法，避免重复代码

    def load_data(self):
        """从包含'商品推广'的工作表名称中加载数据。"""
        try:
            xls = pd.ExcelFile(self.file_path)
            sheet_name = next((name for name in xls.sheet_names if "商品推广活动" in name), None)
            if sheet_name:
                print(f"加载数据来自工作表: {sheet_name}")
                self.data = pd.read_excel(xls, sheet_name=sheet_name, engine="openpyxl")
            else:
                print("未找到匹配的工作表。")
            return self.data  # 返回加载的数据，方便外部知晓是否加载成功
        except FileNotFoundError:
            print(f"文件 {self.file_path} 不存在，请检查文件路径。")
            return None
        except pd.errors.ParserError:
            print(f"文件 {self.file_path} 格式可能不正确，无法正确解析。")
            return None
        except Exception as e:
            print(f"加载数据时出现其他未知错误: {e}")
            return None

    def pause_sp_product(self):
        """根据特定条件暂停广告，并仅保存修改后的行到新文件。"""
        if self.data is None:
            print("数据未加载，无法执行暂停广告操作。")
            return
        # 筛选符合暂停条件的广告
        to_pause = filter.sp_product_pause_filters(self.data, con.sp_product_pause)
        # 检查是否有按条件筛选的行需要暂停
        if not to_pause.empty:
            # 将符合条件的行的 "状态" 标记为 "已暂停"
            self.data.loc[to_pause.index, "状态"] = "已暂停"
            self.data.loc[to_pause.index, "操作"] = "Create"
            # 提取仅包含修改后的行
            modified_rows = self.data.loc[to_pause.index]
            # 获取上传文件所在目录（确保目录存在）
            upload_dir = os.path.dirname(self.file_path)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            # 构建新文件路径，使用原文件名加上后缀
            new_file_name = os.path.basename(self.file_path).rsplit('.', 1)[0] + '_' + 'SP商品暂停' + '.xlsx'
            output_file_path = os.path.join(upload_dir, new_file_name)
            # 保存修改后的行到新文件
            self.save_modified_rows(modified_rows, output_file_path)
        else:
            print("没有符合条件的广告需要暂停。")

    def save_modified_rows(self, modified_rows, output_file_path):
        """
        将修改后的行保存到指定的新文件中。
        :param modified_rows: 包含修改后的数据行的DataFrame
        :param output_file_path: 要保存的新文件路径
        """
        try:
            modified_rows.to_excel(output_file_path, index=False, engine="openpyxl")
            print(f"包含修改行的文件已保存为: {output_file_path}")
        except Exception as e:
            print(f"保存更新文件出错: {e}")

    def call_function(self, function_name):
        """通过名称动态调用函数。"""
        func = getattr(self, function_name, None)
        if callable(func):
            func()
        else:
            print(f"未找到函数 '{function_name}'。")