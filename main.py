from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = "secret"

db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.username


@app.route('/')
def index():
  if "username" in session:
    return render_template('home.html', user=session['username'])
  else:
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    ''''
    Checking the box: 
      unchecked checkboxes do not send any data. 
      On Flask's side, there will not be a key in form, since no value was received. 
      If you want to check if a single checkbox (with a unique name) is checked, just test if it's name is in form
    '''

    checked = False

    if 'remember' in request.form:
      checked = True

    user = User.query.filter_by(username=username).first()

    if user and (password == user.password):
      if checked == True:
        session['username'] = username
        return redirect("/")
      else:
        return render_template('/home.html')
    else:
      return render_template("/login.html",
                             error="Invalid username or password")
  else:
    return render_template('/login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form["confirm-password"]

    if password != confirm_password:
      return render_template("/signup.html", error="Passwords do not match!")

    user = User.query.filter_by(username=username).first()

    if user:
      return render_template("/signup.html", error="Username already exists.")

    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()

    session['username'] = username

    return redirect("/")
  else:
    return render_template('/signup.html')


@app.route('/logout')
def logout():
  session.pop('username', None)
  return render_template("/login.html")


if __name__ == "__main__":
  app.app_context()
  app.run(host='0.0.0.0', port=5001)
  #db.create_all()