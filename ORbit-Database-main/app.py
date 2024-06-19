from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mohammed@2023'

# MySQL Database Configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="0000",
    database="ORbit"  # Ensure this matches your database name
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
        mycursor.execute("SELECT email FROM users")
        usernames = [x[0] for x in mycursor]
        myresult = mycursor.fetchall()
        if username in usernames:
            mycursor.execute(f"SELECT password FROM users WHERE email = '{username}'")
            passwords = [x[0] for x in mycursor]
            pass_valid = mycursor.fetchall()
            if password in passwords:
                session['username'] = username
                return redirect(url_for('home'))
            else:
                flash('Invalid password! Please try again.', 'error')
                return render_template('login.html')
        else:
            flash('Username not found! Please sign up.', 'error')
            return render_template('login.html')
    return render_template('login.html')

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['psw']
        confirm_password = request.form['psw-repeat']
        
        # Check if the email already exists in the database
        mycursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        result = mycursor.fetchone()
        if result:
            flash('Email already exists! Please use a different email.', 'error')
            return render_template('signup.html')
        
        # Insert new user into database
        sql = "INSERT INTO users (email, password, confirm_password) VALUES (%s, %s, %s)"
        val = (email, password, confirm_password)
        mycursor.execute(sql, val)
        mydb.commit()
        
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/equipment')
def equipment():
    return render_template('equipment.html',pagetitle="Equipment")

@app.route('/doctors')
def doctors():
   return render_template('doctors.html',pagetitle="Docotrs")

@app.route('/patient')
def patient():
   return render_template('patient.html',pagetitle="Patient")

@app.route('/oproom')
def oproom():
   return render_template('oproom.html')
   
# Error handling for 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
