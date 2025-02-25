import sqlite3
import tkinter as tk
from tkinter import ttk

DB_FILE = "registry_paths.db"

def find_paths_by_key(event=None):
  key = entry.get().strip().lower()
  result_text.delete(1.0, tk.END)  # Clear previous output
  entry.delete(0,tk.END)

  if not key:
    result_text.insert(tk.END, "Please enter a key.\n")
    return

  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("SELECT hive, path FROM registry_paths WHERE key_name = ?", (key,))
  results = cursor.fetchall()
  conn.close()

  if results:
    result_text.insert(tk.END, f"Matches for '{key}':\n")
    for hive, path in results:
      result_text.insert(tk.END, f"  {hive}: {path}\n")
  else:
    result_text.insert(tk.END, f"No matches found for '{key}'.\n")

# Set up the GUI
root = tk.Tk()
root.title("Registry Path Finder")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Enter Registry Key:").grid(row=0, column=0)
entry = ttk.Entry(frame, width=30)
entry.grid(row=0, column=1)
entry.bind("<Return>", find_paths_by_key)

search_button = ttk.Button(frame, text="Search", command=find_paths_by_key)
search_button.grid(row=0, column=2)

result_text = tk.Text(root, height=10, width=80)
result_text.grid(row=1, column=0, padx=50, pady=50)

root.mainloop()

