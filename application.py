from flask import Flask , render_template , redirect , url_for , flash
from flask_login import LoginManager , login_user , logout_user ,  current_user , login_required
from wtform_fields import * 
from models import * 

# configure app 
app = Flask( __name__)
app.secret_key = 'top secret'

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kykezvnkvxmhpl:323481a7dc7a496db337c41ff1542a9d81aa25b4f7e23f33402611a9c6a11cc2@ec2-174-129-255-35.compute-1.amazonaws.com:5432/d4ve4a3kl1pgck'
db = SQLAlchemy(app)

# configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id): 
	return User.query.get(int(id))


@app.route("/" , methods = [ 'GET' , 'POST'])
def index():
	reg_form = RegistrationForm()
	
	if reg_form.validate_on_submit() : 
		username = reg_form.username.data 
		password = reg_form.password.data
		# hash password 
		hashed_password = pbkdf2_sha256.hash(password)
		# add the user to database 
		user = User(username=username , password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Registered Successfully , Please Login .' , 'success')
		return redirect(url_for('login'))

	return render_template('index.html' , form=reg_form)

@app.route("/login" , methods = ['GET' , 'POST'])
def login(): 
	login_form = LoginForm() 
	if login_form.validate_on_submit() : 
		user_object = User.query.filter_by(username = login_form.username.data).first()
		login_user(user_object)
		return redirect(url_for('chat'))
	return render_template('login.html' , form=login_form)


@app.route("/chat" , methods=['GET' , 'POST'])
def chat():
	if not current_user.is_authenticated : 
		flash('Please Login!' , 'danger')
		return redirect(url_for('login'))
	return "Chat with Me ..."

@app.route("/logout" , methods=['GET'])
def logout():
	logout_user()
	flash('Yoy have Logged-out Successfully !' , 'success')

	return redirect(url_for('login'))

if __name__ == '__main__': 
    app.run(debug=True)