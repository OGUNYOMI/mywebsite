from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
      
def get_db_connection():
    conn = sqlite3.connect('school.db')
    conn.row_factory = sqlite3.Row
    return conn
                       
@app.route('/')
def index():
    return render_template('index.html')
                              
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')
                                                                        
@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')
                                                                        
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')
                            
@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        class_id = request.form['class_id']
        user_id = session['user_id']
        conn = get_db_connection()
        conn.execute('INSERT INTO student_classes (student_id, class_id) VALUES (?, ?)', (user_id, class_id))
        conn.commit()
        conn.close()
        return "Enrolled Successfully!"
    return render_template('enroll.html')                            
if __name__ == '__main__':
    app.run(debug=True)
