import os
from sys import meta_path

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from learn import app
from database import fs

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'mineral_image' not in request.files:
        return "Немає файлу для завантаження!"

    file = request.files['mineral_image']

    if file.filename == '':
        return "Файл не обрано!"

    if file and allowed_file(file.filename):
        # Забезпечує безпечне ім'я файлу

        filename = secure_filename(file.filename)
        # Зберігає файл в директорії "uploads"


        file_id = fs.put(file, filename=filename)
        # if not os.path.exists(app.config['UPLOAD_FOLDER']):
        #     os.makedirs(app.config['UPLOAD_FOLDER'])
        #
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f"Файл успішно завантажено! ID файлу: {file_id}"

    return "Неправильний формат файлу!"


@app.route('/image', methods=['GET'])
def get_images():

    files = fs.find()

    file_list = []
    for file in files:
        file_list.append({
            'filename': file.filename, 'file_id': str(file._id)
        })

    return render_template('images.html', files=file_list)

@app.route('/')
def index():
    return render_template('index.html')
