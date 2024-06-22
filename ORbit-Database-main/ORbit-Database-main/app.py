from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(name)
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
    mycursor.execute("SELECT * FROM equipments")
    row_headers=[x[0] for x in mycursor.description] 
    myresult = mycursor.fetchall()
    data={
         'message':"data retrieved",
         'rec':myresult,
          'header':row_headers}
    return render_template('equipment.html',data=myresult,pagetitle="Equipment")

@app.route('/search_equipment', methods=['GET', 'POST'])
def search_equipment():
    if request.method == 'POST':
        keyword = request.form['search']
        # Perform the search query using the keyword
        mycursor.execute("SELECT * FROM equipments WHERE id_code LIKE %s", ('%' + keyword + '%',))
        
        row_headers = [x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
         data = {
               'message': "Data retrieved",
               'rec': myresult,
               'header': row_headers
         }
         return render_template('equipment.html', data=myresult, keyword=keyword, header=row_headers,pagetitle="Equipment")
        else:
            error_message = "ID not found. Please enter a valid ID."
            return (error_message)
    else:
        # Render the server template without search results
        return render_template('equipment.html',pagetitle="Equipment")

@app.route('/delequip', methods = ['POST', 'GET'])
def delete_eq():
   if request.method=="POST":
      id = request.form['delete']
      delete_query = "DELETE FROM equipments WHERE id_code = %s"
      try:
         mycursor.execute(delete_query,(id,))
         mydb.commit()
         if mycursor.rowcount > 0:
            return render_template('home.html',pagetitle="Equipment")
         else:
            return "ID not found. Please enter a valid ID."
      except Exception as e:
         mydb.rollback()
         return "Failed to delete record. Error: " + str(e)
   else:
      return render_template('doctors.html',pagetitle="Doctors")

@app.route('/addequip',methods = ['POST', 'GET'])
def addequip():
   if request.method == 'POST':
      name = request.form['name']
      # id = request.form['ID']
      supp = request.form['supplier']   
      quant=request.form['quantity']
      pur = request.form['purchasedate']
      warr = request.form['warranty']
      main = request.form['maintanance']
      modelno = request.form['modelno']
      roomno = request.form['roomnum']
      print(name,id )
      sql = "INSERT INTO equipments (name ,supplier ,quantity,purchasedate ,warranty ,maintenance ,model_number,room_no  ) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)"
      val = (name, supp,quant,pur, warr, main,modelno, roomno)
      mycursor.execute(sql, val)
      mydb.commit()
           
      return render_template('home.html',pagetitle="Home Page")
   else:
      return render_template('addequip.html',pagetitle="Add Equipment")

@app.route('/doctors')
def doctors():
   #3ayez aselect eldata w ab3atha w azherha betareea kwayesaa
   mycursor.execute("SELECT * FROM doctor")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   data={
         'message':"data retrieved",
         'rec':myresult,
          'header':row_headers}
   
   return render_template('doctors.html',data=myresult,pagetitle="Docotrs")
#3mlt var dtata 3lashan ab3tha ll doctor

@app.route('/search_doctor', methods=['GET', 'POST'])
def search_doctor():
    if request.method == 'POST':
        keyword = request.form['search']
        # Perform the search query using the keyword
        mycursor.execute("SELECT * FROM doctor WHERE id LIKE %s", ('%' + keyword + '%',))
        
        row_headers = [x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
         data = {
               'message': "Data retrieved",
               'rec': myresult,
               'header': row_headers
         }
         return render_template('doctors.html', data=myresult, keyword=keyword, header=row_headers,pagetitle="Doctor")
        else:
            error_message = "ID not found. Please enter a valid ID."
            return (error_message)
    else:
        # Render the server template without search results
        return render_template('doctors.html',pagetitle="Doctors")

@app.route('/deletedoc', methods = ['POST', 'GET'])
def delete_doc():
   if request.method=="POST":
      # Retrieve the ID from the form data
      id = request.form['delete']

      # Create a cursor to interact with the database
      

      # try:
      #    # Execute the delete query
      delete_query = "DELETE FROM doctor WHERE id = %s"
      try:
         mycursor.execute(delete_query,(id,))
         mydb.commit()
         if mycursor.rowcount > 0:
            return render_template('home.html',pagetitle="Doctors")
         else:
            return "ID not found. Please enter a valid ID."
      # except:
      #    # Handle the case where the delete operation fails
      except Exception as e:
         mydb.rollback()
         return "Failed to delete record. Error: " + str(e)
   else:
      return render_template('home.html',pagetitle="Doctors")

@app.route('/adddoc',methods = ['POST', 'GET'])
def adddoc():
   if request.method == 'POST':
      fn = request.form['firstname']
      mn=request.form['midname']
      ln = request.form['lastname']
      # id = request.form['ID']
      ssn = request.form['SSN']
      tit = request.form['title']
      spec = request.form['specialization']
      bdate = request.form['Dbdate']
      print(fn,mn, ln, ssn, tit, spec, bdate)
      sql = "INSERT INTO doctor (fname ,mname ,lname ,ssn ,title ,specialization ,B_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
      val = (fn,mn, ln, ssn, tit, spec, bdate)
      mycursor.execute(sql, val)
      mydb.commit()   
      return render_template('home.html',pagetitle="Home Page")
   else:
      return render_template('adddoc.html',pagetitle="Add Doctor")

@app.route('/patient')
def patient():
   mycursor.execute("SELECT * FROM patient")
   row_headers=[x[0] for x in mycursor.description] 
   myresult = mycursor.fetchall()
   data={
         'message':"data retrieved",
         'rec':myresult,
          'header':row_headers}
   return render_template('patient.html', data=myresult,pagetitle="Patient")

@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if request.method == 'POST':
        keyword = request.form['search']
        mycursor.execute("SELECT * FROM patient WHERE id LIKE %s", ('%' + keyword + '%',))
        
        row_headers = [x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
         data = {
               'message': "Data retrieved",
               'rec': myresult,
               'header': row_headers
         }
         return render_template('patient.html', data=myresult, keyword=keyword, header=row_headers,pagetitle="Patient")
        else:
               error_message = "ID not found. Please enter a valid ID."
               return (error_message)
    else:
        return render_template('patient.html',pagetitle="Patient")

@app.route('/delpatient', methods = ['POST', 'GET'])
def delete_patient():
   if request.method=="POST":
      id = request.form['delete']
      delete_query = "DELETE FROM patient WHERE id = %s"
      try:
         mycursor.execute(delete_query,(id,))
         mydb.commit()
         if mycursor.rowcount > 0:
            return render_template('home.html',pagetitle="Patient")
         else:
            return "ID not found. Please enter a valid ID."
      except Exception as e:
         mydb.rollback()
         return "Failed to delete record. Error: " + str(e)
   else:
      return render_template('patient.html',pagetitle="Patient")

@app.route('/addpat',methods = ['POST', 'GET'])
def addpat():
   if request.method == 'POST':
      fn = request.form['firstname']
      ln = request.form['lastname']
      pl = request.form['lastname']
      ssn = request.form['SSN']
      sex = request.form['sex']
      ph = request.form['phone']
      pbdate = request.form['Pbdate']
      print(fn,ssn)  
      sql = "INSERT INTO patient (fname ,mname ,lname,ssn ,sex ,phone,B_date ) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
      val = (fn, ln,pl, ssn, sex,ph, pbdate)
      mycursor.execute(sql, val)
      mydb.commit()
      return render_template('home.html',pagetitle="Home Page")
   else:
      return render_template('addpat.html',pagetitle="Add Patient")
   
@app.route('/medicalrec')
def medicalrec():
   mycursor.execute("SELECT date,location,ssn,gender,Family_History_of_Diabetes FROM medrec")
   myresult = mycursor.fetchall()
   return render_template('medicalrec.html', data=myresult)

@app.route('/addmed',methods = ['POST', 'GET'])
def addmed():
    if request.method == 'POST':
        
        pssn = request.form['Pssn']
        gen = request.form['gender']
        loc = request.form['Location']
        date = request.form['date']
            
        # Family History checkboxes
        c1 = request.form.get('c1', 'no')
        c2 = request.form.get('c2', 'no')
        c3 = request.form.get('c3', 'no')
        c4 = request.form.get('c4', 'no')
        c5 = request.form.get('c5', 'no')
        c6 = request.form.get('c6', 'no')
            
            # Patient Medical History checkboxes
        c7 = request.form.get('c7', 'no')
        c8 = request.form.get('c8', 'no')
        c9 = request.form.get('c9', 'no')
        c10 = request.form.get('c10', 'no')
        c11 = request.form.get('c11', 'no')
        c12 = request.form.get('c12', 'no')
            
            # Past Surgical History checkboxes
        c13 = request.form.get('c13', 'no')
        c14 = request.form.get('c14', 'no')
        c15 = request.form.get('c15', 'no')
        c16 = request.form.get('c16', 'no')
            
            # Social History checkboxes
        c17 = request.form.get('c17', 'no')
        c18 = request.form.get('c18', 'no')
        c19 = request.form.get('c19', 'no')

            # SQL query to insert into patient_data table
        sql = """
        INSERT INTO patient_data (
            ssn, gender, location, date, 
            Family_History_of_Diabetes, Family_History_of_Genetic_Disorders, Family_History_of_Heart_Diseases, 
            Family_History_of_Cancer, Family_History_of_Hypertension, Family_History_of_Autoimmune_Diseases, 
            Patient_Medical_History_of_Diabetes, Patient_Medical_History_of_Hypertension, 
            Patient_Medical_History_of_Heart_Disease, Patient_Medical_History_of_post_Stroke, 
            Patient_Medical_History_of_Allergies, Patient_Medical_History_of_Medications, 
            Past_Surgical_History_of_Amputation, Past_Surgical_History_of_Transplant, 
            Past_Surgical_History_of_Cardiovascular_surgery, Past_Surgical_History_of_Fracture_Repair, 
            Social_History_of_Smoker, Social_History_of_Alcohol_consumer, Social_History_of_addiction
        ) VALUES (
            %s, %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, %s
        )
            """
        val = (
            pssn, gen, loc, date, 
            c1, c2, c3, 
            c4, c5, c6, 
            c7, c8, c9, 
            c10, c11, c12, 
            c13, c14, c15, 
            c16, c17, c18, c19
            )
        mycursor.execute(sql, val)
        mydb.commit() 
        return render_template('home.html')
    else:
        return render_template('addmed.html')
    

@app.route('/addapp', methods=['POST', 'GET'])
def addapp():
    if request.method == 'POST':
        patient_ssn = request.form['Pssn']
        doctor_ssn = request.form['Dssn']
        surgery_type = request.form['specialization']
        room_number = request.form['roomnum']
        surgery_date = request.form['surdate']

        sql = "INSERT INTO APPoinment (patient_ssn, doctor_ssn, surgery_type, room_number, surgery_date) VALUES (%s, %s, %s, %s, %s)"
        val = (patient_ssn, doctor_ssn, surgery_type, room_number, surgery_date)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('home.html')
    else:
        return render_template('addapp.html')
    
@app.route('/surgeryapps', methods=['POST', 'GET'])
def surgeryapps():
   return render_template('surgeryapps.html')


    

@app.route('/oproom')
def oproom():
   mycursor.execute("SELECT * FROM operating_room")
   myresult = mycursor.fetchall()
   return render_template('oproom.html', data=myresult)
   # return render_template('oproom.html')

@app.route('/search_operatingroom', methods=['GET', 'POST'])
def search_operatingroom():
    if request.method == 'POST':
        keyword = request.form['search']
        # Perform the search query using the keyword
        mycursor.execute("SELECT * FROM operating_room WHERE room_no LIKE %s", ('%' + keyword + '%',))
        
        row_headers = [x[0] for x in mycursor.description]
        myresult = mycursor.fetchall()
        
        data = {
            'message': "Data retrieved",
            'rec': myresult,
            'header': row_headers
        }
        return render_template('oproom.html', data=myresult, keyword=keyword, header=row_headers,pagetitle="Operating Room")
    else:
        # Render the server template without search results
        return render_template('oproom.html',pagetitle="Operating Room")
   
# Error handling for 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if name == 'main':
    app.run(debug=True)
