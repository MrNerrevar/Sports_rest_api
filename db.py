import os
import sqlite3
from functools import cache

from models import Sport, Event, Selection
from utils import as_value

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
                sport INTEGER NOT NULL,
                status TEXT NOT NULL,
                scheduled_start TEXT NOT NULL,
                actual_start TEXT,
                logos TEXT,
                FOREIGN KEY (sport) REFERENCES sports (id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selections (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                event INTEGER NOT NULL,
                price REAL NOT NULL,
                active BOOLEAN NOT NULL,
                outcome TEXT NOT NULL,
                FOREIGN KEY (event) REFERENCES events (id)
            )
        ''')
        connection.commit()


create_tables()


def db_drop_table(table_name: str):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS {};".format(table_name))
    return cursor.fetchall()


def db_get_all_entries(table_name: str):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {}".format(table_name))
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


# Update method to take in all sql update values as parameters to work generically for sports, events and selections
def db_update(table_name: str, entity_id: int, **kwargs):
    connection = get_db()
    cursor = connection.cursor()
    for key, value in kwargs.items():
        query = "UPDATE {} SET {} = {} WHERE id = {}".format(
            table_name, key, as_value(value), entity_id)
        cursor.execute(query)
        connection.commit()
    return cursor.rowcount


# Probably still doesn't work for multiple queries at once
@cache
def db_search(table_name: str, **kwargs):
    connection = get_db()
    cursor = connection.cursor()
    for key, value in kwargs.items():
        query = "SELECT * FROM {} WHERE 1=1 {}".format(
            table_name,
            "".join([
                f" AND {key} LIKE {as_value(value, wildcard=True)}"
            ])
        )
        cursor.execute(query)
    return cursor.fetchall()


def db_add_event(event: Event):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start, logos)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (event.Name, event.Slug, event.Active, event.Type.value, event.Sport, event.Status.value,
         event.ScheduledStart.isoformat(), event.ActualStart.isoformat() if event.ActualStart else None, event.Logos)
    )
    connection.commit()
    return cursor.lastrowid


def db_add_selection(selection: Selection):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
        '''INSERT INTO selections (name, event, price, active, outcome)
           VALUES (?, ?, ?, ?, ?)''',
        (selection.Name, selection.Event, float(selection.Price), selection.Active, selection.Outcome.value)
    )
    connection.commit()
    return cursor.lastrowid
