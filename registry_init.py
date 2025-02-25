import sqlite3
import os
import json

DB_FILE = "registry_paths.db"
DATA_FILE = "registry_data.json"

def load_registry_data():
  """Loads registry paths from a JSON file."""
  with open(DATA_FILE, "r") as f:
    return json.load(f)

def initialize_database():
  """Creates the database and populates it if it doesn't exist."""
  if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
      CREATE TABLE registry_paths (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_name TEXT NOT NULL COLLATE NOCASE,
        hive TEXT NOT NULL,
        path TEXT NOT NULL
      )
    """)

    # Load data from JSON and insert into DB
    registry_data = load_registry_data()
    cursor.executemany("INSERT INTO registry_paths (key_name, hive, path) VALUES (:key_name, :hive, :path)", registry_data)

    conn.commit()
    conn.close()
    print("[+] Database initialized and populated.")
  else:
    print("[+] Database already exists.")

# Run initialization
initialize_database()

