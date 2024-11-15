import pandas as pd


class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            # 读取Excel文件
            data = pd.read_excel(self.file_path)
            print("从 {} 成功加载数据".format(self.file_path))
            return data
        except FileNotFoundError:
            print("错误：未找到文件 {}".format(self.file_path))
            return None
        except Exception as e:
            print("读取文件时发生错误：{}".format(e))
            return None