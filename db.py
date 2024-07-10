import sqlite3
from models import Sport, Event, Selection
from typing import Optional

DATABASE = 'spectate_api.db'


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    with get_db() as connection:
        cursor = connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sports (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                active BOOLEAN NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
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
                FOREIGN KEY (sport_id) REFERENCES sports (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selections (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                event_id INTEGER NOT NULL,
                price REAL NOT NULL,
                active BOOLEAN NOT NULL,
                outcome TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        ''')
        connection.commit()


create_tables()


def db_get_sports():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sports")
    return cursor.fetchall()


def db_add_sport(sport: Sport):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO sports (name, slug, active) VALUES (?, ?, ?)",
        (sport.Name, sport.Slug, sport.Active)
    )
    connection.commit()
    return cursor.lastrowid


# Needs to be cleaned up, possibly iterate through input params rather than multiple ifs
# The use of optionals allows for using PATCH request. Did not work without optionals and using single sql update
def db_update_sport(sport_id: int, name: Optional[str], slug: Optional[str], active: Optional[bool]):
    connection = get_db()
    cursor = connection.cursor()
    if name:
        cursor.execute("UPDATE sports SET name = ? WHERE id = ?", (name, sport_id))
    if slug:
        cursor.execute("UPDATE sports SET slug = ? WHERE id = ?", (slug, sport_id))
    if active is not None:
        cursor.execute("UPDATE sports SET active = ? WHERE id = ?", (active, sport_id))
    connection.commit()
    return cursor.rowcount


# Does not work for multiple queries yet
def db_search_sports(name: Optional[str], slug: Optional[str]):
    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT * FROM sports WHERE 1=1"
    params = []
    if name:
        query += " AND name LIKE ?"
        params.append(f'%{name}%')
    if slug:
        query += " AND slug LIKE ?"
        params.append(f'%{slug}%')
    cursor.execute(query, params)
    return cursor.fetchall()


def db_get_events():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events")
    return cursor.fetchall()


def db_add_event(event: Event):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO events (name, slug, active, type, sport_id, status, scheduled_start, actual_start, logos)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (event.Name, event.Slug, event.Active, event.Type.value, event.Sport, event.Status.value,
         event.ScheduledStart.isoformat(), event.ActualStart.isoformat() if event.ActualStart else None, event.Logos)
    )
    connection.commit()
    return cursor.lastrowid


def db_update_event(event: Event):
    return


def db_get_selections():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM selections")
    return cursor.fetchall()


def db_add_selection(selection: Selection):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO selections (name, event_id, price, active, outcome)
           VALUES (?, ?, ?, ?, ?)''',
        (selection.Name, selection.Event, float(selection.Price), selection.Active, selection.Outcome.value)
    )
    connection.commit()
    return cursor.lastrowid


def db_update_selection(selection: Selection):
    return
