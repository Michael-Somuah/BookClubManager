import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import hashlib
from datetime import datetime

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#>c1t$@%sobolo",
        database="bookclubdb"
    )

# ---------------------------
# PASSWORD SECURITY
# ---------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------
# CREATE TABLES IF NOT EXIST
# ---------------------------
def ensure_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        role VARCHAR(50) DEFAULT 'member',
        created_at DATETIME DEFAULT NOW()
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        genre VARCHAR(100),
        pages_total INT,
        pages_read INT DEFAULT 0,
        status VARCHAR(50) DEFAULT 'Not Started',
        rating DECIMAL(3,1),
        meeting_date DATE,
        created_at DATETIME DEFAULT NOW()
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS discussions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT NOT NULL,
        comment TEXT NOT NULL,
        username VARCHAR(100),
        created_at DATETIME DEFAULT NOW(),
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
    );
    """)

    # Default admin (Group12 / Devops)
    cursor.execute("SELECT COUNT(*) FROM users WHERE username='Group12'")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
            ("Group12", hash_password("Devops"), "admin")
        )
        conn.commit()

    conn.close()

# ---------------------------
# FETCH / INSERT FUNCTIONS
# ---------------------------
def fetch_books_df():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM books", conn)
    conn.close()
    return df

def add_book(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, genre, pages_total, pages_read, status, rating, meeting_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["title"], data["author"], data["genre"], data["pages_total"],
        data["pages_read"], data["status"], data["rating"], data["meeting_date"]
    ))
    conn.commit()
    conn.close()

def update_book(book_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books SET title=%s, author=%s, genre=%s, pages_total=%s,
        pages_read=%s, status=%s, rating=%s, meeting_date=%s WHERE id=%s
    """, (
        data["title"], data["author"], data["genre"], data["pages_total"],
        data["pages_read"], data["status"], data["rating"], data["meeting_date"], book_id
    ))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    conn.close()

def add_discussion(book_id, username, comment):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO discussions (book_id, username, comment)
        VALUES (%s, %s, %s)
    """, (book_id, username, comment))
    conn.commit()
    conn.close()

def fetch_discussions(book_id):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM discussions WHERE book_id={book_id}", conn)
    conn.close()
    return df

# ---------------------------
# LOGIN SYSTEM
# ---------------------------
def login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and user["password"] == hash_password(password):
        return user
    return None

# ---------------------------
# STREAMLIT CONFIG
# ---------------------------
st.set_page_config(
    page_title=" Book Club Manager",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject dark theme style
st.markdown("""
    <style>
    body {background-color: #0e1117; color: #fafafa;}
    .stApp {background-color: #0e1117;}
    .css-18e3th9 {background-color: #0e1117;}
    .css-1d391kg {background-color: #1e1e1e;}
    .stButton>button {background-color: #ff4b4b; color: white; border-radius: 8px;}
    .stTextInput>div>div>input {background-color: #1e1e1e; color: #fafafa;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# MAIN APP
# ---------------------------
ensure_tables()

if "user" not in st.session_state:
    st.session_state.user = None

# LOGIN PAGE
if not st.session_state.user:
    st.title(" Login to Book Club Manager")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(username, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome, {user['username']} ")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# MAIN DASHBOARD
user = st.session_state.user
st.sidebar.title(" Book Club Manager")
st.sidebar.write(f"Logged in as: **{user['username']} ({user['role']})**")

menu = st.sidebar.radio("Navigation", ["View Books", "Add Book", "Edit/Delete Books", "Discussions", "Analytics"])

# ---------------------------
#  VIEW BOOKS
# ---------------------------
if menu == "View Books":
    st.title(" Book Catalogue")
    books = fetch_books_df()
    if books.empty:
        st.info("No books found. Add your first book from the sidebar.")
    else:
        st.dataframe(books)

# ---------------------------
#  ADD BOOK
# ---------------------------
elif menu == "Add Book":
    st.title(" Add a New Book")
    with st.form("add_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Romance", "Drama", "Poetry", "Other"])
        pages_total = st.number_input("Total Pages", min_value=1)
        pages_read = st.number_input("Pages Read", min_value=0)
        status = st.selectbox("Status", ["Not Started", "In Progress", "Finished"])
        rating = st.slider("Rating", 0.0, 5.0, 0.0, 0.1)
        meeting_date = st.date_input("Meeting Date")
        submitted = st.form_submit_button("Save Book")
        if submitted:
            if pages_read > pages_total:
                st.error("Pages read cannot exceed total pages.")
            else:
                add_book({
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "pages_total": pages_total,
                    "pages_read": pages_read,
                    "status": status,
                    "rating": rating,
                    "meeting_date": meeting_date.strftime("%Y-%m-%d")
                })
                st.success(" Book added successfully!")

# ---------------------------
# EDIT / DELETE BOOKS
# ---------------------------
elif menu == "Edit/Delete Books":
    st.title(" Manage Books")
    books = fetch_books_df()
    if books.empty:
        st.info("No books found.")
    else:
        selected = st.selectbox("Select a Book", books["title"])
        row = books[books["title"] == selected].iloc[0]
        with st.form("edit_form"):
            title = st.text_input("Book Title", row["title"])
            author = st.text_input("Author", row["author"])
            genre = st.text_input("Genre", row["genre"])
            pages_total = st.number_input("Total Pages", value=row["pages_total"], min_value=1)
            pages_read = st.number_input("Pages Read", value=row["pages_read"], min_value=0)
            status = st.selectbox("Status", ["Not Started", "In Progress", "Finished"], index=["Not Started", "In Progress", "Finished"].index(row["status"]))
            rating = st.slider("Rating", 0.0, 5.0, float(row["rating"] or 0), 0.1)
            meeting_date = st.date_input("Meeting Date", value=row["meeting_date"])
            save = st.form_submit_button(" Save Changes")
            delete = st.form_submit_button(" Delete Book")

            if save:
                update_book(row["id"], {
                    "title": title,
                    "author": author,
                    "genre": genre,
                    "pages_total": pages_total,
                    "pages_read": pages_read,
                    "status": status,
                    "rating": rating,
                    "meeting_date": meeting_date.strftime("%Y-%m-%d")
                })
                st.success(" Book updated successfully!")
            if delete:
                delete_book(row["id"])
                st.warning("Book deleted.")
                st.rerun()

# ---------------------------
#  DISCUSSIONS
# ---------------------------
elif menu == "Discussions":
    st.title(" Book Discussions")
    books = fetch_books_df()
    if books.empty:
        st.info("No books available.")
    else:
        selected = st.selectbox("Choose a Book", books["title"])
        book_row = books[books["title"] == selected].iloc[0]
        st.subheader(f" Discussions for '{book_row['title']}'")
        discussions = fetch_discussions(book_row["id"])
        if discussions.empty:
            st.write("No comments yet.")
        else:
            for _, d in discussions.iterrows():
                st.write(f"**{d['username']}**: {d['comment']} ({d['created_at']})")

        comment = st.text_input("Add your comment")
        if st.button("Post Comment"):
            if comment.strip():
                add_discussion(book_row["id"], user["username"], comment.strip())
                st.success(" Comment added!")
                st.rerun()
            else:
                st.error("Please write a comment before posting.")

# ---------------------------
# ANALYTICS
# ---------------------------
elif menu == "Analytics":
    st.title(" Analytics Dashboard")
    books = fetch_books_df()
    if books.empty:
        st.info("No data available.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            genre_chart = px.bar(books, x="genre", title="Books per Genre", color="genre")
            st.plotly_chart(genre_chart, use_container_width=True)
        with col2:
            progress_chart = px.histogram(books, x="pages_read", title="Reading Progress")
            st.plotly_chart(progress_chart, use_container_width=True)
        st.download_button(" Download Books CSV", books.to_csv(index=False), file_name="books.csv")
