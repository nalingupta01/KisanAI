"""
KisanAI - Database Layer
-------------------------
Uses SQLite (built into Python, zero setup) to store farmer profiles
and their crop-disease diagnosis history.
"""

import sqlite3
from datetime import datetime

DB_PATH = "kisanai.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't already exist. Call once at app startup."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
            state TEXT,
            district TEXT,
            crop TEXT,
            land_size REAL,
            land_unit TEXT,
            language TEXT DEFAULT 'en',
            created_at TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            disease_name TEXT,
            confidence REAL,
            created_at TEXT,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    """)

    conn.commit()
    conn.close()


def add_farmer(name, mobile, state, district, crop, land_size, land_unit, language="en"):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO farmers (name, mobile, state, district, crop, land_size, land_unit, language, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, mobile, state, district, crop, land_size, land_unit, language, datetime.now().isoformat()))
    conn.commit()
    farmer_id = cur.lastrowid
    conn.close()
    return farmer_id


def get_farmer_by_mobile(mobile):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmers WHERE mobile = ?", (mobile,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_farmers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmers ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_language(farmer_id, language):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE farmers SET language = ? WHERE id = ?", (language, farmer_id))
    conn.commit()
    conn.close()


def save_diagnosis(farmer_id, disease_name, confidence):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO diagnosis_history (farmer_id, disease_name, confidence, created_at)
        VALUES (?, ?, ?, ?)
    """, (farmer_id, disease_name, confidence, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_diagnosis_history(farmer_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM diagnosis_history WHERE farmer_id = ? ORDER BY created_at DESC", (farmer_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]