from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, logout_user, login_required


app = Flask(__name__)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User,user_id)
    #user = User.query.get(user_id)
    print(type(user))
    return user

@app.post('/login')
def login():
    
    data_login = request.json
    username = data_login.get('username')
    password = data_login.get('password')
    
    if username and password:
        user = User.query.filter_by(username= username).first()
        print(user)

        if user and user.password == password:
            login_user(user)
            return jsonify({
                "message": "user logged in"
            })
    
    return jsonify({
        "message": "credentials not completed"
    }), 400

@app.get('/logout')
@login_required
def logout():
    
    logout_user()
  
    return jsonify({
        "message": "user is now out of application !!!"
    })

@app.get("/")
@login_required
def hello_world():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)