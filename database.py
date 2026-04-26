import sqlite3
import os

# -------------------- DATABASE CONNECTION --------------------
def connect_db():
    db_path = os.path.join(os.path.dirname(__file__), "imagineink.db")
    return sqlite3.connect(db_path, timeout=10, check_same_thread=False)


# ==================== CREATE TABLES ====================
def create_tables():
    conn = connect_db()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_logout TIMESTAMP
    )
    """)

    # PROJECTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """)

    # PROMPTS TABLE (Story)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS prompts (
        prompt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        original_prompt TEXT,
        generated_story TEXT,
        mode TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(project_id) REFERENCES projects(project_id)
    )
    """)

    # COMICS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comics (
        comic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt_id INTEGER,
        comic_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(prompt_id) REFERENCES prompts(prompt_id)
    )
    """)

    conn.commit()
    conn.close()


# ==================== USERS FUNCTIONS ====================

def create_user(username, email, password_hash):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash)
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user


def get_users():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, email, created_at FROM users")
    data = cur.fetchall()
    conn.close()
    return data

def update_password(email, new_password_hash):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password_hash=? WHERE email=?",
        (new_password_hash, email)
    )

    conn.commit()
    conn.close()
# ==================== PROJECT FUNCTIONS ====================

def create_project(user_id, title, description):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO projects (user_id, title, description) VALUES (?, ?, ?)",
        (user_id, title, description)
    )
    conn.commit()

    project_id = cur.lastrowid  # GET PROJECT ID

    conn.close()
    return project_id           # RETURN IT

def get_projects(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE user_id = ?", (user_id,))
    data = cur.fetchall()
    conn.close()
    return data


# ==================== PROMPT + STORY FUNCTIONS ====================

def save_prompt(project_id, prompt, story, mode):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO prompts (project_id, original_prompt, generated_story, mode) VALUES (?, ?, ?, ?)",
        (project_id, prompt, story, mode)
    )
    conn.commit()

    # Get last inserted prompt_id
    prompt_id = cur.lastrowid

    conn.close()
    return prompt_id


def get_prompts(project_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM prompts WHERE project_id = ?", (project_id,))
    data = cur.fetchall()
    conn.close()
    return data


def delete_multiple_prompts(ids):
    conn = connect_db()
    cur = conn.cursor()
    query = "DELETE FROM prompts WHERE prompt_id IN ({})".format(
        ",".join("?" * len(ids))
    )
    cur.execute(query, ids)
    conn.commit()
    conn.close()


# ==================== COMIC FUNCTIONS ====================

def save_comic(prompt_id, comic_path):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO comics (prompt_id, comic_path) VALUES (?, ?)",
        (prompt_id, comic_path)
    )
    conn.commit()
    conn.close()


def get_comics(prompt_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT comic_path FROM comics WHERE prompt_id = ?", (prompt_id,))
    data = cur.fetchall()
    conn.close()
    return data


# ==================== HISTORY FUNCTION ====================

def get_user_history(user_id):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT projects.title, prompts.original_prompt, prompts.generated_story, prompts.mode, prompts.created_at
    FROM prompts
    JOIN projects ON prompts.project_id = projects.project_id
    WHERE projects.user_id = ?
    ORDER BY prompts.created_at DESC
    """, (user_id,))

    data = cur.fetchall()
    conn.close()
    return data


# ==================== SEARCH FUNCTION ==================== ✅ NAYA
def search_stories(user_id, keyword):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT prompts.original_prompt, prompts.generated_story, prompts.mode, prompts.created_at
        FROM prompts
        JOIN projects ON prompts.project_id = projects.project_id
        WHERE projects.user_id = ?
        AND (prompts.original_prompt LIKE ? OR prompts.generated_story LIKE ?)
        ORDER BY prompts.created_at DESC
    """, (user_id, f"%{keyword}%", f"%{keyword}%"))
    results = cur.fetchall()
    conn.close()
    return results


# Run once when file starts
create_tables()

def delete_story(user_id, prompt_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM prompts 
        WHERE prompt_id = (
            SELECT prompts.prompt_id FROM prompts
            JOIN projects ON prompts.project_id = projects.project_id
            WHERE projects.user_id = ? AND prompts.original_prompt = ?
            LIMIT 1
        )
    """, (user_id, prompt_id))
    conn.commit()
    conn.close()