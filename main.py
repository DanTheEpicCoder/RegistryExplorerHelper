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
            result_text.insert(tk.END, f"  ", "bold")
            result_text.insert(tk.END, f"{hive}", "bold")
            result_text.insert(tk.END, f": {path}\n")
            if description:
                result_text.insert(tk.END, f"   {description}\n", "italic")

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
        for hive, path, _ in results:  # Fixed to only unpack hive and path
            recent_text.insert(tk.END, f"  ", "bold")
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

def add_new_path(event=None):
    key_name = key_entry.get().strip().lower()
    hive = hive_entry.get().strip()
    path = path_entry.get().strip()
    description = description_entry.get().strip()

    if not key_name or not hive or not path:
        status_label.config(text="Please fill in all fields.", fg="red")
        return

    # Insert the new path into the database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registry_paths (key_name, hive, path, description) VALUES (?, ?, ?, ?)",
                   (key_name, hive, path, description))
    conn.commit()
    conn.close()

    # Clear the input fields
    key_entry.delete(0, tk.END)
    hive_entry.delete(0, tk.END)
    path_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    # Update the status label
    status_label.config(text="Path added successfully!", fg="green")

    # Reload the paths in the treeview
    load_all_paths()

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

# --- Add Path Tab ---
add_frame = ttk.Frame(notebook)
notebook.add(add_frame, text="Add Path")

ttk.Label(add_frame, text="Registry Key:", font=my_font).grid(row=0, column=0)
key_entry = ttk.Entry(add_frame, width=30, font=my_font)
key_entry.grid(row=0, column=1)

ttk.Label(add_frame, text="Hive:", font=my_font).grid(row=1, column=0)
hive_entry = ttk.Entry(add_frame, width=30, font=my_font)
hive_entry.grid(row=1, column=1)

ttk.Label(add_frame, text="Path:", font=my_font).grid(row=2, column=0)
path_entry = ttk.Entry(add_frame, width=30, font=my_font)
path_entry.grid(row=2, column=1)

ttk.Label(add_frame, text="Description:", font=my_font).grid(row=3, column=0)
description_entry = ttk.Entry(add_frame, width=30, font=my_font)
description_entry.grid(row=3, column=1)

add_button = ttk.Button(add_frame, text="Add Path", command=add_new_path)
add_button.grid(row=4, column=0, columnspan=2)

# Status Label
status_label = ttk.Label(add_frame, text="", font=my_font)
status_label.grid(row=5, column=0, columnspan=2)

# Bind Enter key to add new path
key_entry.bind("<Return>", add_new_path)
hive_entry.bind("<Return>", add_new_path)
path_entry.bind("<Return>", add_new_path)
description_entry.bind("<Return>", add_new_path)

load_all_paths()  # Load data on startup

root.mainloop()

