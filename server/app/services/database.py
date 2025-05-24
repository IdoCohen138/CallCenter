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

def rename_tag(tag_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tags SET name = %s WHERE id = %s", (new_name, tag_id))
    conn.commit()
    conn.close()

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

def get_tags_for_call_db(call_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tags.id, tags.name
        FROM tags
        JOIN call_tags ON tags.id = call_tags.tag_id
        WHERE call_tags.call_id = %s
    """, (call_id,))
    result = cursor.fetchall()
    conn.close()
    return result


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

def assign_suggested_task_to_call(call_id, task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT IGNORE INTO call_tasks (call_id, task_id) VALUES (%s, %s)", (call_id, task_id))
    conn.commit()
    conn.close()

def get_untagged_tasks():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM tasks
        WHERE id NOT IN (SELECT DISTINCT task_id FROM task_tags)
    """)
    tasks = cursor.fetchall()
    conn.close()
    return tasks 

def link_suggested_task_to_tag(task_id, tag_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT IGNORE INTO task_tags (task_id, tag_id) VALUES (%s, %s)",
        (task_id, tag_id)
    )
    conn.commit()
    conn.close()

def rename_task(task_id, new_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET name = %s WHERE id = %s", (new_name, task_id))
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    result = cursor.fetchall()
    conn.close()
    return result

def link_task_to_tag(task_id, tag_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT IGNORE INTO task_tags (task_id, tag_id)
        VALUES (%s, %s)
    """, (task_id, tag_id))
    cursor.execute("""
        SELECT call_id FROM call_tags WHERE tag_id = %s
    """, (tag_id,))
    calls = cursor.fetchall()
    for (call_id,) in calls:
        cursor.execute("""
            INSERT IGNORE INTO call_tasks (call_id, task_id)
            VALUES (%s, %s)
        """, (call_id, task_id))
    conn.commit()
    conn.close()

def get_tasks_by_tag(tag_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.id, t.name, t.status
        FROM tasks t
        JOIN task_tags tt ON t.id = tt.task_id
        WHERE tt.tag_id = %s
    """, (tag_id,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_task_tag_links():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            t.name AS taskName,
            tg.name AS tagName
        FROM task_tags tt
        JOIN tasks t ON tt.task_id = t.id
        JOIN tags tg ON tt.tag_id = tg.id
        ORDER BY tg.name, t.name
    """)
    results = cursor.fetchall()
    conn.close()
    return results
