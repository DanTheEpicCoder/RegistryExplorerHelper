import sqlite3
import tkinter as tk
from tkinter import ttk

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
    cursor.execute("SELECT hive, path, description FROM registry_paths WHERE key_name = ?", (key,))
    results = cursor.fetchall()
    conn.close()

    if results:
        result_text.insert(tk.END, f"Matches for '{key}':\n")
        for hive, path, description in results:
            result_text.insert(tk.END, "  ", "bold")
            result_text.insert(tk.END, f"{hive}", "bold")
            result_text.insert(tk.END, f": {path}\n")
            if description:
                result_text.insert(tk.END, f"   {description}\n", "italic")  # Fixed syntax

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
        for hive, path, _ in results:  # Fixed missing comma
            recent_text.insert(tk.END, "  ", "bold")
            recent_text.insert(tk.END, f"{hive}", "bold")
            recent_text.insert(tk.END, f": {path}\n")

def load_all_paths():
    """Load all registry paths into the Treeview."""
    tree.delete(*tree.get_children())  # Clear previous entries

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT key_name, hive, path FROM registry_paths ORDER BY hive, key_name")
    results = cursor.fetchall()
    conn.close()

    for key_name, hive, path in results:
        tree.insert("", "end", values=(key_name, hive, path))

# Set up the GUI
root = tk.Tk()
root.title("Registry Path Finder")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# --- Search Tab ---
search_frame = ttk.Frame(notebook)
notebook.add(search_frame, text="Search")

ttk.Label(search_frame, text="Enter Registry Key:", font=my_font).grid(row=0, column=0)
entry = ttk.Entry(search_frame, width=30, font=my_font)
entry.grid(row=0, column=1)
entry.bind("<Return>", find_paths_by_key)

search_button = ttk.Button(search_frame, text="Search", command=find_paths_by_key)
search_button.grid(row=0, column=2)

result_text = tk.Text(search_frame, height=8, width=100, font=my_font)
result_text.grid(row=1, column=0, columnspan=3, padx=50, pady=10)
result_text.tag_configure("bold", font=("Georgia", 12, "bold"))
result_text.tag_configure("italic", font=("Georgia", 12, "italic"))  # Added italic configuration

# Recently used section
recent_text = tk.Text(search_frame, height=10, width=100, font=my_font)
recent_text.grid(row=2, column=0, columnspan=3, padx=50, pady=10)
recent_text.insert(tk.END, "Recently Used:\n")
recent_text.tag_configure("bold", font=("Georgia", 12, "bold"))

# --- Browse Tab ---
browse_frame = ttk.Frame(notebook)
notebook.add(browse_frame, text="Browse All")

tree = ttk.Treeview(browse_frame, columns=("Key", "Hive", "Path"), show="headings")
tree.heading("Key", text="Registry Key")
tree.heading("Hive", text="Hive")
tree.heading("Path", text="Path")

tree.column("Key", width=200)
tree.column("Hive", width=100)
tree.column("Path", width=400)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(browse_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

load_all_paths()  # Load data on startup

root.mainloop()

