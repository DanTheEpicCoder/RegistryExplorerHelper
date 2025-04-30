import sqlite3
import os
import json
import sys

def load_registry_data(data_file):
    """Load registry paths from the specified JSON file"""
    if not os.path.exists(data_file):
        print(f"[-] Error: '{data_file}' not found. Ensure the file exists before running this script.")
        return []
    
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("[-] Error: JSON file should contain a list of registry entries.")
                return []
            return data
    except json.JSONDecodeError as e:
        print(f"[-] Error: Failed to parse JSON file - {e}")
        return []

def initialize_database(db_file, data_file):
    """Create and initialize the database with data from the JSON file"""
    conn = sqlite3.connect(db_file)
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
        registry_data = load_registry_data(data_file)
        if registry_data:
            try:
                cursor.executemany("""
                    INSERT INTO registry_paths (key_name, hive, path, description) 
                    VALUES (:key_name, :hive, :path, :description)
                """, registry_data)
                conn.commit()
                print(f"[+] Database '{db_file}' initialized and populated with data from '{data_file}'.")
                print(f"[+] Added {len(registry_data)} registry path entries.")
            except sqlite3.Error as e:
                print(f"[-] SQLite error: {e}")
                conn.rollback()
        else:
            print("[-] No data inserted due to errors in JSON file.")
    else:
        print(f"[+] Database '{db_file}' already exists and contains {count} entries.")
    
    conn.close()

def get_user_input():
    """Get file paths from user input"""
    print("Registry Paths Database Initializer")
    print("==================================")
    
    json_file = input("Enter path to JSON data file: ")
    while not json_file or not os.path.exists(json_file):
        print(f"[-] Error: File '{json_file}' not found.")
        json_file = input("Enter path to JSON data file (or 'exit' to quit): ")
        if json_file.lower() == 'exit':
            sys.exit(0)
    
    db_file = input("Enter name for the database file: ")
    while not db_file:
        db_file = input("Enter name for the database file: ")
    
    # Add .db extension if not provided
    if not db_file.endswith('.db'):
        db_file += '.db'
    
    return json_file, db_file

def main():
    # Get input interactively
    json_file, db_file = get_user_input()
    
    # Initialize the database
    initialize_database(db_file, json_file)

if __name__ == "__main__":
    main()
