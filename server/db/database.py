import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# --- TAGS ---
def get_all_tags():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tags")
    result = cursor.fetchall()
    conn.close()
    return result

def add_tag(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tags (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

# --- CALLS ---
def create_call(description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO calls (description) VALUES (%s)", (description,))
    conn.commit()
    call_id = cursor.lastrowid
    conn.close()
    return call_id

def get_all_calls():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM calls ORDER BY created_at DESC")
    result = cursor.fetchall()
    conn.close()
    return result

def assign_tag_to_call(call_id, tag_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO call_tags (call_id, tag_id) VALUES (%s, %s)", (call_id, tag_id))
    conn.commit()
    conn.close()

# --- TASKS ---
def create_task(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name) VALUES (%s)", (name,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def assign_task_to_call(call_id, task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO call_tasks (call_id, task_id) VALUES (%s, %s)", (call_id, task_id))
    conn.commit()
    conn.close()

def update_task_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
    conn.commit()
    conn.close()

def get_tasks_for_call(call_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tasks.id, tasks.name, tasks.status
        FROM tasks
        JOIN call_tasks ON tasks.id = call_tasks.task_id
        WHERE call_tasks.call_id = %s
    """, (call_id,))
    result = cursor.fetchall()
    conn.close()
    return result
    
# --- USERS ---
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, display_name, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, display_name, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user
