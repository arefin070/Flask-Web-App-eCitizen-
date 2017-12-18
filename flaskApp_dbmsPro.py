from flask import Flask, render_template,request, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField,SelectField, PasswordField, validators
#rom passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

##Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflask_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Initi mysql

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template("home.html")


#About
@app.route('/about')
def about():
    return render_template("about.html")



 ##Register Class ##
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=20)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [
        validators.length(min=3, max=20),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

##Register ##
@app.route('/register', methods=['GET', 'POST'] )
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        ##Cursor
        cur = mysql.connection.cursor()

        #execute query
        cur.execute("INSERT INTO register(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        #commit
        mysql.connection.commit()

        cur.close()

        flash('You have registered successfully!', 'success')

        return redirect(url_for('index'))
    return render_template("register.html", form=form)

##Register Class ##
class RegisterForm2(Form):
    org_registration_no = StringField('Organization Regi. No.', [validators.Length(min=1, max=50)])
    org_name = StringField('Organization Name', [validators.Length(min=1, max=30)])
    org_type = StringField('Type of Organization', [validators.Length(min=1, max=20)])
    org_email = StringField('Email', [validators.Length(min=4, max=20)])
    org_phone = StringField('Phone', [validators.Length(min=4, max=20)])
    org_username = StringField('Username', [validators.Length(min=1, max=20)])
    org_password = PasswordField('Password', [
        validators.length(min=1, max=20),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

#Organization Registration
@app.route('/org.register', methods=['GET', 'POST'] )
def org_register():
    form2 = RegisterForm2(request.form)
    if request.method == 'POST' and form2.validate():
        org_registration_no = form2.org_registration_no.data
        org_name = form2.org_name.data
        org_type = form2.org_type.data
        org_email = form2.org_email.data
        org_phone = form2.org_phone.data
        org_username = form2.org_username.data
        org_password = form2.org_password.data


        ##Cursor
        cur= mysql.connection.cursor()

        #execute query
        cur.execute("INSERT INTO org_register(org_registration_no, org_name, org_type, org_email, org_phone, org_username, org_password) VALUES(%s, %s, %s, %s, %s, %s, %s)", (org_registration_no, org_name, org_type, org_email, org_phone, org_username, org_password))

        #commit
        mysql.connection.commit()

        cur.close()

        flash('You have registered successfully!', 'success')

        return redirect(url_for('index'))
    return render_template("org_register.html", form=form2)


#Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method== 'POST':
        #Get Forms fields
        username = request.form['username']
        password_candidate = request.form['password']

        #Cursor
        cur = mysql.connection.cursor()

        #Get User by User name
        result = cur.execute("SELECT * FROM register WHERE username = %s",[username])
        if result > 0:
            #Get Stored hash
            data = cur.fetchone()
            password = data['password']

            #compare password
            if (password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('index'))

            else:
                error = 'Invalid login'
                return render_template("login.html", error=error)
        else:
            error = 'User not found'
            return render_template("login.html", error=error)

    return render_template("login.html")

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))




#Challenge Class
class ChallengForm(Form):
    title = StringField('Title', [validators.length(min=1, max=200)])
    details = TextAreaField('Details',[validators.length(min=1)] )






#Dashboard (Challenge)
@app.route('/challengboard', methods=['GET', 'POST'])
@is_logged_in
def dashboard():
    form = ChallengForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        details = form.details.data

        #Cursor

        cur = mysql.connection.cursor()

        #Execute cursor
        cur.execute("INSERT INTO challenge(title, details, challenger) VALUES (%s, %s, %s)", (title, details, session['username']))
        mysql.connection.commit()

        cur.close()

        flash('Challenge has successfully submitted!', 'success')

        return render_template(url_for('index'))
    return render_template("add_article.html", form=form)

# Idea Board ...
@app.route('/ideaboard')
@is_logged_in
def idea_board():
    return render_template("articles.html")

# under Home ... Event Featuring

@app.route('/visit')
@is_logged_in
def event_visit():
    return render_template("visit.html")

## Challenge Board
@app.route('/challenges')
@is_logged_in
def challegne():
    return render_template("Challeges.html")



if __name__ == '__main__':
    app.secret_key='secret123456'
    app.run(debug=True)
