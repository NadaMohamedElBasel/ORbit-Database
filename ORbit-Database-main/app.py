from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mohammed@2023'

# MySQL Database Configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="0000",
    database="ORbit"  
)
mycursor = mydb.cursor()

# Route for home page
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', pagetitle="Home Page")
    else:
        return redirect(url_for('login'))

# Route for login page
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        
        # Query for user with given email and password
        mycursor.execute("SELECT email, password FROM users WHERE email = %s AND password = %s", (username, password,))
        user = mycursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password! Please try again.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        password_repeat = request.form['psw-repeat']
        
        # Check if the email already exists in the database
        mycursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        result = mycursor.fetchone()
        if result:
            flash('Email already exists! Please use a different email.', 'error')
            return render_template('signup.html', email=email)  # Pass email to keep it in the form
        
        # Check if passwords match
        if password != password_repeat:
            flash('Passwords do not match! Please try again.', 'error')
            return render_template('signup.html', email=email, password=password)  # Pass email and password to keep them in the form
        
        # Insert new user into database including confirm_password
        sql = "INSERT INTO users (email, password, confirm_password) VALUES (%s, %s, %s)"
        val = (email, password, password_repeat)
        mycursor.execute(sql, val)
        mydb.commit()
        
        return redirect(url_for('login'))
    
    # Render the signup form with empty fields initially
    return render_template('signup.html', email='', password='')  # Pass empty email and password to the template

@app.route('/equipment')
def equipment():
    return render_template('equipment.html', pagetitle="Equipment")

@app.route('/doctors')
def doctors():
   return render_template('doctors.html', pagetitle="Doctors")

@app.route('/patient')
def patient():
   return render_template('patient.html', pagetitle="Patient")

@app.route('/oproom')
def oproom():
   return render_template('oproom.html', pagetitle="Operation Room")
   
# Error handling for 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
