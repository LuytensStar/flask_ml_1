from flask import Flask

app = Flask(__name__)

from learn import routes
# from learn.routes import main_bp
# from auth.views import auth_bp
#
# def create_app():
#     learn = Flask(__name__)
#     learn.secret_key = 'your_secret_key'  # Додайте секретний ключ для сесій
#
#     # Регіструємо Blueprints
#     learn.register_blueprint(main_bp)
#     learn.register_blueprint(auth_bp, url_prefix='/auth')
#
#     return learn
