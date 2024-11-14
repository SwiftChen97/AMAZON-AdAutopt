import sys
from data_loader import DataLoader
from auto_adjust.auto_adjust import AutomationAdjustment
from data_analysis.data_analysis import DataAnalysis

class AmazonAdOptimizationSystem:
    def __init__(self,data,file_path):
        self.data = data
        self.path = file_path
        self.automation_adjustment = AutomationAdjustment(file_path)
        self.data_analysis = DataAnalysis()

    def run_optimization(self, sp_function=None):
        print("Running optimization with loaded data.")
        # 调用自动化调整模块
        self.automation_adjustment.adjust_all(sp_function)
        # 调用数据分析模块
        self.data_analysis.analyze_all()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_excel_file> [sp_function]")
    else:
        file_path = sys.argv[1]
        sp_function = sys.argv[2] if len(sys.argv) > 2 else None
        loader = DataLoader(file_path)
        data = loader.load_data()

        if data is not None:
            system = AmazonAdOptimizationSystem(data,file_path)
            system.run_optimization(sp_function)