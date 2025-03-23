from app.auth import auth_bp
from app.db import initialize_db
from flask import Flask

app = Flask(__name__)
initialize_db()
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
