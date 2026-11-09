from contextlib import closing
import sqlite3

def init_db(db_path):
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS errors (
                session_id TEXT NOT NULL,
                error_type TEXT NOT NULL,
                sentence TEXT,
                correction TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def save_error(db_path, session_id, error_type, sentence, correction):
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute('''
            INSERT INTO errors (session_id, error_type, sentence, correction)
            VALUES (?, ?, ?, ?)
        ''', (session_id, error_type, sentence, correction))
        conn.commit()

def top_errors(db_path, session_id, limit=3):
    with closing(sqlite3.connect(db_path)) as conn:
        cursor = conn.execute('''
            SELECT error_type, COUNT(*)
            FROM errors 
            WHERE session_id = ? GROUP BY error_type ORDER BY COUNT(*) DESC LIMIT ?
        ''', (session_id, limit))
        return cursor.fetchall()