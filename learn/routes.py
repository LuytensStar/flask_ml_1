import os
from sys import meta_path

from flask import Flask, render_template, request, redirect, url_for,Response, send_file
from werkzeug.utils import secure_filename
from learn import app
from .database import fs
import io
from bson import ObjectId


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')



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


@app.route('/get_image/<file_id>', methods=['GET'])
def get_image(file_id):
    try:
        # Знайти зображення у MongoDB за _id
        image_file = fs.get(ObjectId(file_id))

        # Повернути зображення у відповідному форматі
        return send_file(io.BytesIO(image_file.read()), mimetype='image/png')

    except Exception as e:
        return Response(f"Помилка: {str(e)}", status=404)


@app.route('/image', methods=['GET'])
def get_images():

    files = fs.find()

    file_list = []
    for file in files:
        file_list.append({
            'filename': file.filename, 'file_id': str(file._id)
        })

    return render_template('images.html', files=file_list)


