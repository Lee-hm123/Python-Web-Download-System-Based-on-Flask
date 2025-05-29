from flask import Flask, render_template, abort, send_file
import os

app = Flask(__name__,template_folder='.')

# 设置你的文件目录
UPLOAD_FOLDER = r'D:\Dev\Python\Practice\网页下载\For_Download'
# UPLOAD_FOLDER = r'./For_Download'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 获取文件列表并检查文件夹是否存在
def get_file_list():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # 如果文件夹不存在，则创建它
    try:
        # 返回文件夹内的文件列表
        return [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    except Exception as e:
        return []

# 首页，显示所有文件
@app.route('/')
def index():
    files = get_file_list()
    folder_path = os.path.abspath(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files, folder_path=folder_path)


# 文件下载路由（返回文件内容）
@app.route('/download/<filename>')
def download_file(filename):
    if filename not in get_file_list():
        abort(404)  # 如果文件不存在，返回 404 错误
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(file_path,as_attachment=True)
    except Exception:
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
