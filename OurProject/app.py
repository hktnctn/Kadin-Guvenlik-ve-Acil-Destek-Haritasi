from flask import Flask
from flask_cors import CORS  # CORS'u import et
from config import Config
from db import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# CORS'u tüm route'lar için etkinleştir
CORS(app)  # Bu satırı eklediğinden emin ol

# Blueprint'i kaydet
app.register_blueprint(routes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)