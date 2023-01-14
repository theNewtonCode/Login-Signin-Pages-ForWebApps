from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loginpage1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserLogin(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/loginpage", methods=['GET', 'POST'])
def loginpage():
    log_in = False
    data = {}
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        user = UserLogin(username=username, password=password)
        stmt = UserLogin.query.filter_by(username=username).all()
        for i in stmt:
            if(i.password==password):
                log_in = True
                print("loggedin")
                break
        if log_in == False:
            print("wrong credentials")
                
        data = {"username": username, "password":password, "log_in":log_in}
    return render_template('login.html', data=data)
    # return "Hello, World!"
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    signup = True
    data = {}
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        user = UserLogin(username=username, password=password)
        # allusers = UserLogin.query.all()
        stmt = UserLogin.query.filter_by(username=username).all()
        if len(stmt)!=0:
            signup = False
            # print("record already exists") #if signup is false user cannot signup as his username already exists
        if signup==True:
            db.session.add(user)
            db.session.commit()
                # print("added")

        # allusers = UserLogin.query.all()
        data = {"username": username, "password":password, "signup":signup}
    return render_template('signup.html', data=data)

@app.route("/thework/<string:username>", methods=['GET', 'POST'])
def success(username):
    userdata = UserLogin.query.filter_by(username=username).first()
    return render_template('logged_in.html', username=userdata.username)

if __name__ == "__main__":
    app.run(debug =True)