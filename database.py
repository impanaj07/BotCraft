# database.py

import sqlite3

def create_connection():
    conn = sqlite3.connect('matchmaker.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            skills TEXT NOT NULL,
            interests TEXT NOT NULL
        )
    ''')

    # Create mentors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            mentor_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            skills TEXT NOT NULL,
            interests TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_profile(user_id, username, skills, interests):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO profiles (user_id, username, skills, interests)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username,
            skills=excluded.skills,
            interests=excluded.interests
    ''', (user_id, username, skills, interests))
    conn.commit()
    conn.close()

def add_mentor(mentor_id, name, skills, interests):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mentors (mentor_id, name, skills, interests)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(mentor_id) DO UPDATE SET
            name=excluded.name,
            skills=excluded.skills,
            interests=excluded.interests
    ''', (mentor_id, name, skills, interests))
    conn.commit()
    conn.close()

def get_profiles():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM profiles')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_mentors():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mentors')
    rows = cursor.fetchall()
    conn.close()
    return rows