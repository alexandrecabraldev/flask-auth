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
    #user = User.query.get(user_id) deprecated

    return user

@app.post('/login')
def login():
    
    data_login = request.json
    username = data_login.get('username')
    password = data_login.get('password')
    
    if username and password:
        user = User.query.filter_by(username= username).first()

        if user and user.password == password:
            login_user(user)
            return jsonify({
                "message": "user logged in"
            })
    
    return jsonify({
        "message": "credentials not completed"
    }), 400

@app.post('/user')
@login_required
def user_registration():
    user = request.json
    username= user.get("username")
    password= user.get('password')

    print(user)
    if not username or not password:
        return jsonify({
            "message": "invalid data"
        }), 400
    
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "message": "user registrated !!!"
    })

@app.get('/user/<int:user_id>')
@login_required
def get_specific_user(user_id):
    user = db.session.get(User,user_id)

    if not user:
        return jsonify({"message": "user not found"}), 404
    
    print(user)
    return jsonify({"username": user.username})


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