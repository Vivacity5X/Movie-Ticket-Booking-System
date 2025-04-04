from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mysqldb import MySQL
import mysql.connector
import qrcode
import io
import base64

app = Flask(__name__)

# Flask session configuration
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'user': 'root',
    'password': '230622',  # Your MySQL password
    'host': '127.0.0.1',
    'database': 'movie_db'
}

def get_db_connection():
    """Helper function to create a new database connection."""
    conn = mysql.connector.connect(**db_config)
    return conn

### **User Registration**
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    password = data['password']  # Store plaintext password (should be hashed!)

    try:
        query = "INSERT INTO Users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['name'], data['email'], password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

### **Login**
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("Email provided:", email)
        print("Password provided:", password)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check user credentials
        query = "SELECT * FROM Users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()  # Fetch user details

        if user:
            print("Stored password:", user['password'])

        cursor.close()  # Close cursor first
        conn.close()    # Then close the connection

        if user and user['password'] == password:
            session['user_id'] = user['user_id']
            session['user_name'] = user['name']
            return redirect(url_for('movies'))
        else:
            return "Invalid email or password!", 401

    return render_template('login.html')


### **Logout**
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

### **Search for a Movie**
@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search_results = []
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Movies WHERE title LIKE %s OR genre LIKE %s", 
                       (f"%{search_query}%", f"%{search_query}%"))
        search_results = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template('search.html', search_results=search_results)



### **Fetch Movies**
@app.route('/movies', methods=['GET'])
def movies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Movies")
    movies = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('movies.html', movies=movies)


### **Booking Route**

@app.route('/book_ticket/<int:movie_id>', methods=['GET', 'POST'])
def book_ticket(movie_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch movie details
    cursor.execute("SELECT * FROM movies WHERE movie_id = %s", (movie_id,))
    movie = cursor.fetchone()

    # Fetch available theaters and showtimes
    cursor.execute("SELECT * FROM theaters")
    theaters = cursor.fetchall()

    if request.method == 'POST':
        theater_id = request.form['theater_id']
        showtime = request.form['showtime']
        seat_number = request.form['seat_number']

        # Check seat availability
        cursor.execute("""
            SELECT * FROM bookings WHERE theater_id = %s AND showtime = %s AND seat_number = %s
        """, (theater_id, showtime, seat_number))

        existing_booking = cursor.fetchone()

        if existing_booking:
            flash("Seat is already booked. Please choose another seat.", "danger")
        else:
            # Insert booking into the database
            cursor.execute("""
                INSERT INTO bookings (movie_id, user_id, theater_id, showtime, seat_number) 
                VALUES (%s, %s, %s, %s, %s)
            """, (movie_id, session['user_id'], theater_id, showtime, seat_number))
            conn.commit()

            # Generate QR code with booking details
            qr_data = f"Movie: {movie['title']}, Theater: {theater_id}, Showtime: {showtime}, Seat: {seat_number}"
            qr = qrcode.make(qr_data)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

            cursor.close()
            conn.close()

            return render_template("booking_confirmation.html", qr_code=qr_base64, movie=movie, showtime=showtime, seat_number=seat_number)

    cursor.close()
    conn.close()
    return render_template("book_ticket.html", movie=movie, theaters=theaters)


### **Add Movie**
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    genre = request.form['genre']
    release_year = request.form['release_year']

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO Movies (title, genre, release_year) VALUES (%s, %s, %s)", 
                   (title, genre, release_year))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('movies'))

### **Update Movie**
@app.route('/update_movie/<int:movie_id>', methods=['POST'])
def update_movie(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    genre = request.form['genre']
    release_year = request.form['release_year']

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE Movies SET title = %s, genre = %s, release_year = %s WHERE movie_id = %s",
                   (title, genre, release_year, movie_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('movies'))

### **Delete Movie**
@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Movies WHERE movie_id = %s", (movie_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('movies'))

if __name__ == '__main__':
    app.run(debug=True)
