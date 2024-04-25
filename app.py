from flask import Flask
from models.user import User
from database import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

# @app.post('/login')
# def login():
    
#     pass

@app.get("/")
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)