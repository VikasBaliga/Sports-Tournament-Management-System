## 1. CREATE TABLE USERS. LOOK AT HOW TO CONNECT WITH OTHER TABLES. USERS WILL HAVE USERNAME, PASSWORD, IS_ADMIN (bool) MINIMUM
## 2. NEED TO ADD ALL HTML FILES CORRESPONDING TO THE NAMES IN THIS FILE
## 3. ADD CSS EVERYWHERE. LAST THING TO DO
## 4. 

from flask import Flask, render_template, request, redirect, session, url_for, flash
from db import get_db, close_db
from admin_routes import admin_bp               # calling admin_route.py
from user_routes import user_bp                 # calling user_routes.py
from config import Config


app= Flask(__name__)
app.secret_key = "ab43"      # adding this because throwing error otherwise

# This code handles error handling and routes (/), 

app.register_blueprint(admin_bp)    #check use and remove if needed
app.register_blueprint(user_bp)


@app.route('/')
def Webpage():
    return render_template('Webpage.html')      #changed landing to Webpage

@app.route('/test_db', methods=['GET'])
def test_db():
    with app.app_context:
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("SELECT DATABASE();")  # Test query
            db_name = cur.fetchone()
            cur.close()
            return f"Connected to database: {db_name[0]}"
        except Exception as e:
            return f"Database connection failed: {e}"

@app.route('/home')
def home():
    print("BALL: ", session)
    if 'username' in session:                
        if session.get('is_admin')==True:
            print(1)
            return redirect(url_for('admin'))
        else:
            print(2)
            return redirect(url_for('user'))
    else:
        print(session, "has big balls")
        return redirect(url_for('login'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route entered")
    db = None  # Initialize db to avoid undefined variable errors in finally block
    try:
        if request.method == 'POST':
            print("POST method detected")
            db = get_db()
            print("Database connection acquired")
            cur = db.cursor()
            print("Cursor acquired")
            username = request.form['username']
            password = request.form['password']
            print(f"Received username: {username}, password: {password}")

            # Execute query
            cur.execute(
                'SELECT username, password, is_admin FROM user WHERE username = %s',
                (username,)
            )
            print("Query executed")
            user = cur.fetchone()
            print(f"User fetched: {user}")

            cur.close()
            print("Cursor closed")

            if user and password == user[1]:
                print("Login successful")
                session['username'] = user[0]
                session['is_admin'] = user[2]
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'ERROR')
                return redirect(url_for('login'))
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred during login. Please try again.', 'ERROR')
        return redirect(url_for('login'))
    finally:
        if db:
            close_db(db)
            print("Database connection closed in finally block")
    return render_template('login.html')
    


@app.route('/register', methods=['GET', 'POST'])        
def register():     # registering users
    if request.method == 'POST':
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('register'))
        try:
            db = get_db()
            cur = db.cursor()
            username = request.form['username']
            password = request.form['password']

            # Check if the username already exists
            db=get_db()
            cur=db.cursor()
            cur.execute('SELECT * FROM user WHERE username = %s',(username, ))
            existing_user=cur.fetchone()
            if existing_user:
                flash('username already taken. Try again', 'ERROR')
                return redirect(url_for('register'))

            cur.execute(
                'INSERT INTO user (username, password, is_admin) VALUES (%s, %s, %s)',
                (username, password, False))
            db.commit()
            cur.close()
            flash('Registration successful', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            print("Error: ", str(e))
            flash('Registration failed', 'error')
            return redirect(url_for('register'))
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return render_template('Webpage.html')


@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/user')
def user():
    if 'username' not in session:
        return redirect(url_for('login'))
#    db = get_db()
 #   cur = db.cursor()
  #  cur.execute('SELECT * FROM user;')     # use this? 
   # user = cur.fetchall()                  # what do these exactly do here?
    #cur.close()
    return render_template('user.html', user=user)
  
@app.route('/AboutUs')
def AboutUs():
    return render_template('AboutUs.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')



if __name__ == '__main__':
    app.run(debug=True)