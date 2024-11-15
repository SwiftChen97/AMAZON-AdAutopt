from flask import Flask, render_template, request
import tkinter as tk
from tkinter import filedialog
import sys
from data_loader import DataLoader
from auto_adjust.auto_adjust import AutomationAdjustment
from data_analysis.data_analysis import DataAnalysis

function_mapping = {
    "SP商品暂停": "pause_sp_product",
    # 可以根据实际情况添加更多映射关系
}

app = Flask(__name__)


class AmazonAdOptimizationSystem:
    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path
        self.automation_adjustment = AutomationAdjustment(file_path)
        self.data_analysis = DataAnalysis()

    def run_optimization(self, sp_function=None):
        print("正在使用加载的数据进行优化操作。")
        actual_function_name = None
        if sp_function and sp_function in function_mapping:
            actual_function_name = function_mapping[sp_function]

        # 调用自动化调整模块
        self.automation_adjustment.adjust_all(actual_function_name)
        # 调用数据分析模块
        self.data_analysis.analyze_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file_path = request.form.get('file_path')
        sp_function_name_cn = request.form.get('sp_function')

        loader = DataLoader(file_path)
        data = loader.load_data()

        if data is not None:
            optimization_system = AmazonAdOptimizationSystem(data, file_path)
            optimization_system.run_optimization(sp_function_name_cn)
            return "优化操作完成，你可以在后台查看相关结果。"
        else:
            return "数据加载失败，请检查文件路径和文件格式。"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)