# DBMS Mini Project - Movie Booking System

## Overview
This project is a **Movie Booking System** built using **Flask** and **MySQL**. It allows users to:
- Register and log in.
- Search for movies by title or genre.
- View available movies.
- Book tickets for movies with seat selection.
- Generate QR codes for booking confirmation.
- Add, update, and delete movies (admin functionality).

## Features
- **User Authentication**: Secure login and logout functionality.
- **Movie Management**: Add, update, delete, and search movies.
- **Ticket Booking**: Book tickets with seat and showtime selection.
- **QR Code Generation**: Generate QR codes for booking confirmation.
- **Responsive Design**: User-friendly interface with responsive styles.

## Technologies Used
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS
- **QR Code**: Python `qrcode` library

## Setup Instructions

### Prerequisites
- Python 3.x
- MySQL Server
- Required Python libraries (install via `requirements.txt`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/dbms-mini-project.git
   cd dbms-mini-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database:
   - Create a MySQL database named `movie_db`.
   - Update the database credentials in `app.py` under `db_config`.

4. Import the database schema:
   - Use the provided SQL file (if available) to set up the database tables.

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the application:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## File Structure
```
DBMS Mini project/
├── app.py                     # Main Flask application
├── templates/                 # HTML templates
│   ├── login.html             # Login page
│   ├── movies.html            # Movies listing page
│   ├── search.html            # Search results page
│   ├── book_ticket.html       # Ticket booking page
│   ├── booking_confirmation.html # Booking confirmation with QR code
│   ├── qrcode.html            # QR code display page
│   ├── confirmation.html      # General confirmation page
├── static/                    # Static files (CSS, JS, images)
│   └── styles.css             # Stylesheet for the project
└── README.md                  # Project documentation
```

## Usage
1. **Register**: Create a new account.
2. **Login**: Log in with your credentials.
3. **Search Movies**: Use the search bar to find movies by title or genre.
4. **Book Tickets**: Select a movie, choose a theater, showtime, and seat to book a ticket.
5. **Manage Movies**: Add, update, or delete movies (admin functionality).

## Screenshots
- **Login Page**:
  ![Login Page](screenshots/login.png)
- **Movies Page**:
  ![Movies Page](screenshots/movies.png)
- **Booking Confirmation**:
  ![Booking Confirmation](screenshots/booking_confirmation.png)


## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.


## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- Flask documentation
- MySQL documentation
- Python `qrcode` library