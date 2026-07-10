import sqlite3
from datetime import datetime

DB_NAME = "drivesafe.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        timestamp TEXT,

        ear REAL,

        mar REAL,

        head_pose TEXT,

        risk_score INTEGER,

        risk_level TEXT,

        drowsy INTEGER,

        yawning INTEGER

    )
    """)

    conn.commit()
    conn.close()


def log_event(
    ear,
    mar,
    head_pose,
    risk_score,
    risk_level,
    drowsy,
    yawning
):

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO sessions(
        timestamp,
        ear,
        mar,
        head_pose,
        risk_score,
        risk_level,
        drowsy,
        yawning
    )
    VALUES(?,?,?,?,?,?,?,?)
    """, (

        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        ear,

        mar,

        head_pose,

        risk_score,

        risk_level,

        int(drowsy),

        int(yawning)

    ))

    conn.commit()
    conn.close()


def fetch_data():

    conn = sqlite3.connect(DB_NAME)

    cur = conn.cursor()

    cur.execute("SELECT * FROM sessions")

    rows = cur.fetchall()

    conn.close()

    return rows