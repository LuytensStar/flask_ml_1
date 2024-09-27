import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from learn import app

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

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Файл успішно завантажено!"

    return "Неправильний формат файлу!"


@app.route('/')
def index():
    return render_template('index.html')
