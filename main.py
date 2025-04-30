import sqlite3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Define theme colors
DARK_BG = "#1a1a1a"           # Dark background
FOREST_GREEN = "#2c5f2d"      # Forest green for accents
LIGHT_GREEN = "#97bc62"       # Light accent color
TEXT_COLOR = "#e0e0e0"        # Light text for dark backgrounds
HIGHLIGHT = "#408040"         # Highlight green

DB_FILE = "registry_paths.db"  # Default
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registry_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT NOT NULL,
            hive TEXT NOT NULL,
            path TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

initialize_database()

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
        for hive, path, _ in results:
            recent_text.insert(tk.END, f"  ", "bold")
            recent_text.insert(tk.END, f"{hive}", "bold")
            recent_text.insert(tk.END, f": {path}\n")

def load_all_paths():
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
        status_label.config(text="Please fill in all fields.", fg=LIGHT_GREEN)
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registry_paths (key_name, hive, path, description) VALUES (?, ?, ?, ?)",
                   (key_name, hive, path, description))
    conn.commit()
    conn.close()

    key_entry.delete(0, tk.END)
    hive_entry.delete(0, tk.END)
    path_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    status_label.config(text="Path added successfully!", fg=LIGHT_GREEN)
    load_all_paths()

def select_database():
    global DB_FILE
    file_path = filedialog.askopenfilename(
        title="Select Database File",
        filetypes=[("SQLite Database", "*.db"), ("All Files", "*.*")]
    )
    if file_path:
        DB_FILE = file_path
        initialize_database()
        load_all_paths()
        messagebox.showinfo("Database Selected", f"Using database:\n{file_path}")

def apply_theme(root):
    """Apply the forest green theme to all widgets"""
    style = ttk.Style()
    
    # Configure the main theme
    style.theme_use('clam')  # Using clam as base theme
    
    # Configure colors for ttk widgets
    style.configure('TFrame', background=DARK_BG)
    style.configure('TLabel', background=DARK_BG, foreground=TEXT_COLOR)
    style.configure('TButton', background=FOREST_GREEN, foreground=TEXT_COLOR)
    style.map('TButton', 
              background=[('active', HIGHLIGHT), ('pressed', LIGHT_GREEN)],
              foreground=[('active', TEXT_COLOR), ('pressed', DARK_BG)])
    style.configure('TEntry', fieldbackground=DARK_BG, foreground=TEXT_COLOR, insertcolor=TEXT_COLOR)
    
    # Configure Notebook style
    style.configure('TNotebook', background=DARK_BG, tabmargins=[2, 5, 2, 0])
    style.configure('TNotebook.Tab', background=FOREST_GREEN, foreground=TEXT_COLOR, 
                   padding=[30, 5], focuscolor=FOREST_GREEN)
    style.map('TNotebook.Tab', 
              background=[('selected', HIGHLIGHT), ('active', LIGHT_GREEN)],
              foreground=[('selected', TEXT_COLOR), ('active', DARK_BG)])
    
    # Configure Treeview
    style.configure('Treeview', 
                   background=DARK_BG, 
                   foreground=TEXT_COLOR,
                   fieldbackground=DARK_BG)
    style.map('Treeview', 
             background=[('selected', FOREST_GREEN)],
             foreground=[('selected', TEXT_COLOR)])
    
    # Configure scrollbars
    style.configure('Vertical.TScrollbar', background=FOREST_GREEN, troughcolor=DARK_BG, 
                   arrowcolor=TEXT_COLOR)
    style.configure('Horizontal.TScrollbar', background=FOREST_GREEN, troughcolor=DARK_BG,
                   arrowcolor=TEXT_COLOR)
    
    # Apply theme to root window
    root.configure(bg=DARK_BG)
    
    # Apply theme to standard tkinter widgets that don't use ttk styling
    root.option_add('*Text.background', DARK_BG)
    root.option_add('*Text.foreground', TEXT_COLOR)
    root.option_add('*Text.insertBackground', TEXT_COLOR)  # cursor color
    
    return style

# Set up the GUI
root = tk.Tk()
root.title("Registry Path Finder")
root.geometry("900x700")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# Apply theme to the application
style = apply_theme(root)

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

select_db_button = ttk.Button(button_frame, text="Select Database", command=select_database)
select_db_button.pack(side="left", padx=5)

# Create notebook widget
notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# --- Search Tab ---
search_frame = ttk.Frame(notebook, padding=10)
notebook.add(search_frame, text="Search")
search_frame.columnconfigure(1, weight=1)

ttk.Label(search_frame, text="Enter Registry Key:", font=my_font).grid(row=0, column=0, pady=5, sticky="w")
entry = ttk.Entry(search_frame, font=my_font)
entry.grid(row=0, column=1, pady=5, sticky="ew")
entry.bind("<Return>", find_paths_by_key)

search_button = ttk.Button(search_frame, text="Search", command=find_paths_by_key)
search_button.grid(row=0, column=2, padx=5)

result_text = tk.Text(search_frame, height=8, font=my_font, bg=DARK_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
result_text.grid(row=1, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
result_text.tag_configure("bold", font=("Georgia", 12, "bold"), foreground=LIGHT_GREEN)
result_text.tag_configure("italic", font=("Georgia", 12, "italic"), foreground=LIGHT_GREEN)

recent_text = tk.Text(search_frame, height=10, font=my_font, bg=DARK_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
recent_text.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")
recent_text.insert(tk.END, "Recently Used:\n")
recent_text.tag_configure("bold", font=("Georgia", 12, "bold"), foreground=LIGHT_GREEN)

search_frame.rowconfigure(1, weight=1)
search_frame.rowconfigure(2, weight=1)

# --- Browse Tab ---
browse_frame = ttk.Frame(notebook, padding=10)
notebook.add(browse_frame, text="Browse All")
browse_frame.rowconfigure(0, weight=1)
browse_frame.columnconfigure(0, weight=1)

# Create a frame to hold the treeview and both scrollbars
tree_frame = ttk.Frame(browse_frame)
tree_frame.grid(row=0, column=0, sticky="nsew")
tree_frame.rowconfigure(0, weight=1)
tree_frame.columnconfigure(0, weight=1)

# Create the treeview with appropriate column widths
tree = ttk.Treeview(tree_frame, columns=("Key", "Hive", "Path"), show="headings")
tree.heading("Key", text="Registry Key")
tree.heading("Hive", text="Hive")
tree.heading("Path", text="Path")

# Set column widths - making Key and Hive smaller to give more space to Path
tree.column("Key", width=120, minwidth=80)
tree.column("Hive", width=80, minwidth=60)
tree.column("Path", width=500, minwidth=200)

# Vertical scrollbar
v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=v_scrollbar.set)

# Horizontal scrollbar
h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
tree.configure(xscroll=h_scrollbar.set)

# Place the treeview and scrollbars in the grid
tree.grid(row=0, column=0, sticky="nsew")
v_scrollbar.grid(row=0, column=1, sticky="ns")
h_scrollbar.grid(row=1, column=0, sticky="ew")

# --- Add Path Tab ---
add_frame = ttk.Frame(notebook, padding=10)
notebook.add(add_frame, text="Add Path")

for i in range(2):
    add_frame.columnconfigure(i, weight=1)

ttk.Label(add_frame, text="Registry Key:", font=my_font).grid(row=0, column=0, pady=5, sticky="w")
key_entry = ttk.Entry(add_frame, font=my_font)
key_entry.grid(row=0, column=1, pady=5, sticky="ew")

ttk.Label(add_frame, text="Hive:", font=my_font).grid(row=1, column=0, pady=5, sticky="w")
hive_entry = ttk.Entry(add_frame, font=my_font)
hive_entry.grid(row=1, column=1, pady=5, sticky="ew")

ttk.Label(add_frame, text="Path:", font=my_font).grid(row=2, column=0, pady=5, sticky="w")
path_entry = ttk.Entry(add_frame, font=my_font)
path_entry.grid(row=2, column=1, pady=5, sticky="ew")

ttk.Label(add_frame, text="Description:", font=my_font).grid(row=3, column=0, pady=5, sticky="w")
description_entry = ttk.Entry(add_frame, font=my_font)
description_entry.grid(row=3, column=1, pady=5, sticky="ew")

add_button = ttk.Button(add_frame, text="Add Path", command=add_new_path)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

status_label = tk.Label(add_frame, text="", font=my_font, bg=DARK_BG, fg=TEXT_COLOR)
status_label.grid(row=5, column=0, columnspan=2)

key_entry.bind("<Return>", add_new_path)
hive_entry.bind("<Return>", add_new_path)
path_entry.bind("<Return>", add_new_path)
description_entry.bind("<Return>", add_new_path)

load_all_paths()
root.mainloop()
