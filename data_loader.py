import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        try:
            # 读取Excel文件
            data = pd.read_excel(self.file_path)
            print("Data loaded successfully from:", self.file_path)
            return data
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None