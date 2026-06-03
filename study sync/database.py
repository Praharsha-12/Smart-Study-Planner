import sqlite3

def init_db():
    """Creates the database and tasks table if they do not exist."""
    conn = sqlite3.connect("planner.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task TEXT NOT NULL,
            deadline TEXT,
            priority TEXT,
            duration INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()

    cursor.execute("PRAGMA table_info(tasks)")
    columns = [row[1] for row in cursor.fetchall()]
    if "duration" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN duration INTEGER DEFAULT 0")
        conn.commit()

    conn.close()

def add_task_to_db(subject, task, deadline, priority, duration):
    """Inserts a new study task into the database."""
    conn = sqlite3.connect("planner.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (subject, task, deadline, priority, duration, status)
        VALUES (?, ?, ?, ?, ?, 'Pending')
    """, (subject, task, deadline, priority, duration))
    conn.commit()
    conn.close()

def get_all_tasks():
    """Retrieves all tasks from the database."""
    conn = sqlite3.connect("planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, subject, task, deadline, priority, duration, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows

def complete_task_in_db(task_id):
    """Updates a task's status to 'Completed' using its ID."""
    conn = sqlite3.connect("planner.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Run this file directly to initialize the database
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
