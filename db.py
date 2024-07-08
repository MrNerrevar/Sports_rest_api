import sqlite3

DATABASE = 'spectate_api.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sport_table (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                active BOOLEAN NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS event_table (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                active BOOLEAN NOT NULL,
                type TEXT NOT NULL,
                sport_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                scheduled_start TEXT NOT NULL,
                actual_start TEXT,
                logos TEXT,
                FOREIGN KEY (sport_id) REFERENCES sport_table (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selection_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                event_id INTEGER NOT NULL,
                price REAL NOT NULL,
                active BOOLEAN NOT NULL,
                outcome TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES event_table (id)
            )
        ''')
        conn.commit()


create_tables()
