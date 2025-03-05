import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import font

DB_FILE = "registry_paths.db"
recent_queries = []  # Store last 10 queries
my_font = ("Georgia", 12)

def find_paths_by_key(event=None):
  key = entry.get().strip().lower()
  result_text.delete(1.0, tk.END)  # Clear previous output
  entry.delete(0, tk.END)

  if not key:
    result_text.insert(tk.END, "Please enter a key.\n")
    return

  # Connect to db and retrieve data
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("SELECT hive, path FROM registry_paths WHERE key_name = ?", (key,))
  results = cursor.fetchall()
  conn.close()

  if results:
    result_text.insert(tk.END, f"Matches for '{key}':\n")
    for hive, path in results:
      result_text.insert(tk.END, f"  ", "bold")
      result_text.insert(tk.END, f"{hive}", "bold")
      result_text.insert(tk.END, f": {path}\n")
    
    # Store recent queries
    recent_queries.insert(0, (key, results))
    if len(recent_queries) > 10:
      recent_queries.pop()
    update_recent_queries()
  else:
    result_text.insert(tk.END, f"No matches found for '{key}'.\n")

def update_recent_queries():
  recent_text.delete(1.0, tk.END)
  recent_text.insert(tk.END, "Recently Used:\n")
  for key, results in recent_queries:
    recent_text.insert(tk.END, f"{key}:\n")
    for hive, path in results:
      recent_text.insert(tk.END, f"  ", "bold")
      recent_text.insert(tk.END, f"{hive}", "bold")
      recent_text.insert(tk.END, f": {path}\n")

# Set up the GUI
root = tk.Tk()
root.title("Registry Path Finder")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Enter Registry Key:", font=my_font).grid(row=0, column=0)
entry = ttk.Entry(frame, width=30, font=my_font)
entry.grid(row=0, column=1)
entry.bind("<Return>", find_paths_by_key)

search_button = ttk.Button(frame, text="Search", command=find_paths_by_key)
search_button.grid(row=0, column=2)

result_text = tk.Text(root, height=8, width=100, font=my_font)
result_text.grid(row=1, column=0, padx=50, pady=10)
result_text.tag_configure("bold", font=("Georgia", 12, "bold"))

# Recently used section
recent_text = tk.Text(root, height=20, width=100, font=my_font)
recent_text.grid(row=2, column=0, padx=50, pady=10)
recent_text.insert(tk.END, "Recently Used:\n")
recent_text.tag_configure("bold", font=("Georgia", 12, "bold"))

root.mainloop()
