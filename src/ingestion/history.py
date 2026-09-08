import sqlite3

DB_PATH = "history.db"


def init_database():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_history(question, answer):
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO history (question, answer)
        VALUES (?, ?)
    """, (question, answer))

    connection.commit()
    connection.close()


def get_history():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, question, answer, created_at
        FROM history
        ORDER BY id DESC
    """)

    history = cursor.fetchall()

    connection.close()

    return history


def clear_history():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("DELETE FROM history")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_database()
    print("Baza de date a fost creată cu succes.")