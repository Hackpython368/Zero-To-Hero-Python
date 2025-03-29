from flask import Flask, render_template,request,redirect
import json
import smtplib
import mysql.connector as mysql


app = Flask(__name__)

# Database connection
db = mysql.connect(host="localhost", user="root", password="12345", database="library")
cursor = db.cursor()



@app.route('/')
def index():
    return redirect('/Login')

@app.route('/Login',methods=['GET', 'POST'])
def home():
    params = {
        'LoginSuccessful' : 0,
        'LoginFailed' : 0
    }
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        print(user_email,user_password)
        cursor.execute(f"SELECT * FROM USERS WHERE email = '{user_email}' AND password = '{user_password}'")
        result = cursor.fetchone()
        print(result)
        if result != None:
            print("Login successful")
            params['LoginSuccessful'] = 1
            cursor.execute(f"SELECT role FROM USERS WHERE email = '{user_email}'")
            role = cursor.fetchone()
            print(role)
            if role[0] == 'student':
                print("Redirecting to student dashboard")
                return redirect("/StudentDashBoard")
            if role[0] == 'admin':
                return redirect("/Login/Admin-DashBoard")
            else:
                print("Inside the else")            
        else:
            print("Login failed")


    return render_template('home.html')



@app.route('/StudentDashBoard')
def studentDashboard():
    return render_template('studentDashboard.html')

@app.route('/StudentDashBoard/Books')
def books():
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    return render_template('books.html',books=data)

@app.route('/StudentDashBoard/Borrowed')
def borrowed():
    return render_template('BorrowedBook.html')

@app.route('/StudentDashBoard/Profile')
def profile():
    cursor.execute("SELECT * FROM USERS where email = 'hNlJ8@example.com'")
    return render_template('StudentProfile.html')

@app.route('/signUp' ,methods=['GET', 'POST'])
def signUp():
    params = {
            'emailExists' : 0,
            'passwordMatch' : 0
        }
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        user_cpassword = request.form.get('cpassword')
        print("Checking email in database")
        cursor.execute(f"SELECT * FROM USERS WHERE email = '{user_email}'")
        result = cursor.fetchone()
        if result == None:
            if user_password == user_cpassword:
                cursor.execute(f"INSERT INTO USERS (name, email, password, role) VALUES('{user_name}', '{user_email}', '{user_password}', 'student')")
                db.commit()
                return render_template('signUp.html', params=params)
            else:
                params['passwordMatch'] = 1
                return render_template('signUp.html', params=params)
        else:
            params['emailExists'] = 1
            return render_template('signUp.html', params=params)
    return render_template('signUp.html',params=params)

def CreateOTP():
    import random
    return random.randint(100000, 999999)


@app.route('/resetPassword',methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        print("POST request received")
        if "Verify_OTP" in request.form:
            print("Verify OTP button clicked")
            User_OTP = request.form.get('otp')
            print(User_OTP)

            with open('Library Managment System/config/user_login.txt', 'r') as f:
                data = f.readlines()
            
            print(data,type(data))
            otp = data[1].strip()
            if User_OTP == otp:
                print("OTP matched")
                return render_template('verifyOTP.html', message="OTP verified successfully",checked_OTP=1,email=data[0])
            else:
                return render_template('verifyOTP.html', message="Invalid OTP")
        if "Send_OTP" in request.form:
            print("Send OTP button clicked")

            otp = CreateOTP()
            receiver_email_id = request.form.get('email')
            with open('Library Managment System/config/user_login.txt', 'w') as f:
                f.write(receiver_email_id + ' \n ' + str(otp))

            
            with open('Library Managment System/config/user.txt', 'r') as f:
                user_email = json.loads(f.readline())
                sender_email_id = user_email['email']
                sender_email_id_password = user_email['password']

            s = smtplib.SMTP('smtp.gmail.com', 587)  # creates SMTP session with host and port 
            print("SMTP session created")
            s.starttls() # start TLS for security encryption
            print("TLS started")
            s.login(sender_email_id, sender_email_id_password) # Authentication
            print("Logged in successfully")
            message = f"""Subject: Reset Your Library Management System Password

    Dear User,

    We received a request to reset your password for the Library Management System. Use the OTP below to reset your password:

    Your OTP: {otp}

    This OTP is valid for 10 minutes. If you did not request this, please ignore this email.

    Click the link below to reset your password:
    Reset Password

    If you need any help, feel free to contact support.

    Best regards,
    Study Center Team""" # message to be sent

            s.sendmail(sender_email_id, receiver_email_id, message)
            print("Mail sent successfully")

            s.quit() # terminating the session
            print("Session terminated")

            return render_template('verifyOTP.html', email=receiver_email_id)
        
    return render_template('resetPassword.html')




if __name__ == '__main__':
    app.run(debug=True)


