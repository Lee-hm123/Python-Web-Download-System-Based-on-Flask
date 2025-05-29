from flask import Flask, render_template_string, abort
import os

app = Flask(__name__, template_folder='.')

# 设置你的文件目录
UPLOAD_FOLDER = r'./For_Download'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 获取文件列表并检查文件夹是否存在
def get_file_list():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])  # 如果文件夹不存在，则创建它
    try:
        # 返回文件夹内的文件列表
        return [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if
                os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    except Exception as e:
        return []


# HTML 模板（使用 render_template_string 直接渲染）
html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文件下载</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7fc;
            margin: 0;
            padding: 20px;
        }

        h1 {
            color: #333;
            text-align: center;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }

        .file-list {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }

        .file-list li {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #f9f9f9;
            transition: background-color 0.3s;
        }

        .file-list li:hover {
            background-color: #f1f1f1;
        }

        .file-list input[type="checkbox"] {
            margin-right: 10px;
        }

        .actions {
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        button {
            padding: 10px 15px;
            font-size: 16px;
            border: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #45a049;
        }

        .download-links {
            margin-top: 20px;
        }

        .download-links button {
            background-color: #007BFF;
        }

        .download-links button:hover {
            background-color: #0056b3;
        }

        .download-links a {
            color: white;
            text-decoration: none;
        }

        .download-links button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }

        .error-message {
            color: red;
            font-size: 16px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>文件下载</h1>

        {% if not files %}
        <div class="error-message">
            当前目录 {{ folder_path }} 无文件！
        </div>
        {% endif %}

        <div>
            <h2>请选择文件</h2>
            <ul class="file-list">
                {% for file in files %}
                    <li>
                        <label>
                            <input type="checkbox" name="files" value="{{ file }}" /> {{ file }}
                        </label>
                    </li>
                {% endfor %}
            </ul>
        </div>

        <div class="actions">
            <button onclick="selectAllFiles()">全选</button>
            <button id="download-selected" onclick="downloadSelectedFiles()" disabled>下载选中的文件</button>
        </div>

        <div class="download-links" id="download-links"></div>
    </div>

    <script>
        function selectAllFiles() {
            const checkboxes = document.querySelectorAll('input[name="files"]');
            const isChecked = checkboxes[0].checked;
            checkboxes.forEach(checkbox => {
                checkbox.checked = !isChecked;
            });
        }

        function downloadSelectedFiles() {
            const selectedFiles = [];
            const checkboxes = document.querySelectorAll('input[name="files"]:checked');
            checkboxes.forEach((checkbox) => {
                selectedFiles.push(checkbox.value);
            });

            if (selectedFiles.length === 0) {
                alert('请至少选择一个文件！');
                return;
            }

            selectedFiles.forEach((file) => {
                const a = document.createElement('a');
                a.href = `/download/${file}`;
                a.download = file;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            });
        }

        document.querySelectorAll('input[name="files"]').forEach((checkbox) => {
            checkbox.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('input[name="files"]:checked');
                const downloadButton = document.getElementById('download-selected');
                downloadButton.disabled = checkboxes.length === 0;
            });
        });
    </script>
</body>
</html>
'''


# 首页，显示所有文件
@app.route('/')
def index():
    files = get_file_list()
    folder_path = os.path.abspath(app.config['UPLOAD_FOLDER'])
    return render_template_string(html, files=files, folder_path=folder_path)


# 文件下载路由（返回文件内容）
@app.route('/download/<filename>')
def download_file(filename):
    if filename not in get_file_list():
        abort(404)  # 如果文件不存在，返回 404 错误
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'rb') as f:
            file_content = f.read()
        return file_content
    except Exception:
        abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
