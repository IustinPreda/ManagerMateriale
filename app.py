import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    files = os.listdir(UPLOAD_FOLDER)
    file_info = []
    total_size_kb = 0
    for f in files:
        path = os.path.join(UPLOAD_FOLDER, f)
        size_kb = os.path.getsize(path) // 1024
        total_size_kb += size_kb
        ext = os.path.splitext(f)[1].upper().replace('.', '')
        file_info.append({
            "name": f,
            "ext": ext if ext else "FILE",
            "size_kb": size_kb,
        })

    categories = {"PDF": 0, "DOCX": 0, "PPTX": 0, "XLSX": 0, "Other": 0}
    for file in file_info:
        if file["ext"] in categories:
            categories[file["ext"]] += 1
        else:
            categories["Other"] += 1

    return render_template('index.html', files=file_info, total_size_kb=total_size_kb, categories=categories)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
