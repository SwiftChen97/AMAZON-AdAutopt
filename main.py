import tkinter as tk
from tkinter import filedialog
import sys
from data_loader import DataLoader
from auto_adjust.auto_adjust import AutomationAdjustment
from data_analysis.data_analysis import DataAnalysis

function_mapping = {
    "SP商品暂停": "pause_sp_product",
    # "功能二": "function2",
    # 根据实际函数添加更多映射关系
}

class AmazonAdOptimizationSystem:
    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path
        self.automation_adjustment = AutomationAdjustment(file_path)
        self.data_analysis = DataAnalysis()

    def run_optimization(self, sp_function_name_cn=None):
        print("正在使用加载的数据进行优化操作。")
        actual_function_name = None
        if sp_function_name_cn and sp_function_name_cn in function_mapping:
            actual_function_name = function_mapping[sp_function_name_cn]

        # 调用自动化调整模块
        self.automation_adjustment.adjust_all(actual_function_name)
        # 调用数据分析模块
        self.data_analysis.analyze_all()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.system = None

    def create_widgets(self):
        self.file_path_label = tk.Label(self, text="请选择Excel文件路径：")
        self.file_path_label.pack()

        self.file_path_entry = tk.Entry(self)
        self.file_path_entry.pack()

        self.browse_button = tk.Button(self, text="浏览", command=self.browse_file)
        self.browse_button.pack()

        self.sp_function_label = tk.Label(self, text="请输入sp_function（可选，中文名）：")
        self.sp_function_label.pack()

        self.sp_function_entry = tk.Entry(self)
        self.sp_function_entry.pack()

        self.optimize_button = tk.Button(self, text="执行优化", command=self.execute_optimization)
        self.optimize_button.pack()

        self.result_text = tk.Text(self)
        self.result_text.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.file_path_entry.insert(0, file_path)

    def execute_optimization(self):
        file_path = self.file_path_entry.get()
        sp_function_name_cn = self.sp_function_entry.get()

        loader = DataLoader(file_path)
        data = loader.load_data()

        if data is not None:
            self.system = AmazonAdOptimizationSystem(data, file_path)
            self.result_text.insert(tk.END, "数据加载成功，开始执行优化操作...\n")
            self.system.run_optimization(sp_function_name_cn)
            self.result_text.insert(tk.END, "优化操作完成。\n")
        else:
            self.result_text.insert(tk.END, "数据加载失败，请检查文件路径和文件格式。\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()