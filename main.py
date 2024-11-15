from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from data_loader import DataLoader
from auto_adjust.auto_adjust import AutomationAdjustment
from data_analysis.data_analysis import DataAnalysis

function_mapping = {
    "SP商品暂停": "pause_sp_product",
    # 可以根据实际情况添加更多映射关系
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # 设置上传文件的保存目录


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
        # 检查是否有文件上传
        if 'file' not in request.files:
            return "没有选择文件！"
        file = request.files['file']
        if file.filename == '':
            return "没有选择文件！"
        if file:
            # 确保文件名安全
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            loader = DataLoader(file_path)
            data = loader.load_data()
            if data is not None:
                optimization_system = AmazonAdOptimizationSystem(data, file_path)
                sp_function_name_cn = request.form.get('sp_function')
                optimization_system.run_optimization(sp_function_name_cn)
                new_file_path = file_path.rsplit('.', 1)[0] + '_' + 'SP商品暂停' + '.xlsx'
                return render_template('index.html', download_link=new_file_path)
            else:
                return "数据加载失败，请检查文件路径和文件格式。"
    return render_template('index.html')


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        # 发送文件给客户端下载
        response = send_file(file_path, as_attachment=True)
        # 删除原来文件夹下的文件
        os.remove(file_path)
        return response
    except FileNotFoundError:
        return "文件未找到！"


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)