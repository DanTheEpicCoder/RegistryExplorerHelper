import sqlite3
import os
import json

DB_FILE = "registry_paths.db"
DATA_FILE = "registry_data.json"

# Load registry paths from JSON file
def load_registry_data():
    if not os.path.exists(DATA_FILE):
        print(f"[-] Error: '{DATA_FILE}' not found. Ensure the file exists before running this script.")
        return []
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("[-] Error: JSON file should contain a list of registry entries.")
                return []
            return data
    except json.JSONDecodeError as e:
        print(f"[-] Error: Failed to parse JSON file - {e}")
        return []

# Creates database and populates if empty
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registry_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT NOT NULL COLLATE NOCASE,
            hive TEXT NOT NULL,
            path TEXT NOT NULL,
            description TEXT
        )
    """)

    # Check if database is already populated
    cursor.execute("SELECT COUNT(*) FROM registry_paths")
    count = cursor.fetchone()[0]

    if count == 0:
        registry_data = load_registry_data()
        if registry_data:
            cursor.executemany("""
                INSERT INTO registry_paths (key_name, hive, path, description) 
                VALUES (:key_name, :hive, :path, :description)
            """, registry_data)
            conn.commit()
            print("[+] Database initialized and populated.")
        else:
            print("[-] No data inserted due to errors in JSON file.")
    else:
        print("[+] Database already exists and contains data.")

    conn.close()

# Run initialization
initialize_database()

