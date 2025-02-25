import sqlite3
import os
from registry_init import initialize_database  # Import the database setup function

DB_FILE = "registry_paths.db"

# Ensure database is initialized before querying
if not os.path.exists(DB_FILE):
  print("[!] Database not found. Initializing now...")
  initialize_database()

def find_paths_by_key(key):
  """Queries the database for a given registry key and prints matching paths."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()

  cursor.execute("""
    SELECT hive, path FROM registry_paths
    WHERE key_name = ?
  """, (key.lower(),))

  results = cursor.fetchall()
  conn.close()

  if results:
    print(f"\n[+] Found {len(results)} match(es) for '{key}':")
    for hive, path in results:
      print(f"  {hive}: {path}")
  else:
    print(f"\n[-] No matches found for '{key}'")

# Main loop for user input
while True:
  user_input = input("\nEnter a registry key (or type 'exit' to quit): ").strip().lower()

  if user_input == "exit":
    print("Goodbye!")
    break

  find_paths_by_key(user_input)
