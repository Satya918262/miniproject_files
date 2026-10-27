import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from user_dashboard import show_user_dashboard

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def validate_user(username, password):
    # Connect to SQLite3 database and validate user credentials
    conn = sqlite3.connect("car_details.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        empid=user[0]
        fname = user[1]
        return empid,fname
    return None

def employee_login_form():
    def login():
        username = entry_username.get()
        password = entry_password.get()

        result = validate_user(username, password)
        if result:
            empid,fname=result
            # If user is found, proceed to dashboard
            root.destroy()  # Close the login window
            show_user_dashboard(empid,fname)  # Pass username to home screen
        else:
            # If invalid credentials, show error message
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Initialize login window
    root = tk.Toplevel()
    root.title("Employee Form")
    center_window(root, 900, 550)
    root.minsize(400, 300)
    root.configure(bg="white")

    # Style configuration (same as provided in your code)
    style = ttk.Style()
    style.configure("Custom.TFrame", background="#2B579A")
    style.configure("Custom.TLabel", background="#2B579A", foreground="white", font=("Times New Roman", 24))
    style.configure("Custom.TButton", font=("Times New Roman", 16, "bold"), padding=(10, 5))

    main_frame = ttk.Frame(root, padding="5 5 5 5", style="Custom.TFrame")
    main_frame.pack(expand=True)

    outer_frame = tk.Frame(main_frame, background="#FFFFFF", borderwidth=0, relief="flat")
    outer_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    bordered_frame = ttk.Frame(outer_frame, padding="20", style="Custom.TFrame")
    bordered_frame.grid(row=0, column=0, sticky="nsew")

    label_heading = ttk.Label(bordered_frame, text="Employee Login", font=("Times New Roman", 35, "bold"), background="#2B579A", foreground="white", anchor='center')
    label_heading.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    label_username = ttk.Label(bordered_frame, text="Username:", font=("Times New Roman", 16), background="#2B579A", foreground="white")
    label_username.grid(row=1, column=0, sticky="w", pady=(10, 5))

    username_frame = tk.Frame(bordered_frame, background="white")
    username_frame.grid(row=2, column=0, pady=(10, 5), sticky="ew")
    entry_username = tk.Entry(username_frame, insertbackground='white', width=25, font=("Times New Roman", 16), bg="#2B579A", fg="white", bd=0, highlightthickness=0)
    entry_username.pack(fill="both", padx=2, pady=2)

    label_password = ttk.Label(bordered_frame, text="Password:", font=("Times New Roman", 16), background="#2B579A", foreground="white")
    label_password.grid(row=3, column=0, sticky="w", pady=(10, 5))

    password_frame = tk.Frame(bordered_frame, background="white")
    password_frame.grid(row=4, column=0, pady=(10, 5), sticky="ew")
    entry_password = tk.Entry(password_frame, show="*", insertbackground='white', width=25, font=("Arial", 16), bg="#2B579A", fg="white", bd=0, highlightthickness=0)
    entry_password.pack(fill="both", padx=2, pady=2)

    button_login = ttk.Button(bordered_frame, text="Login", command=login, style="Custom.TButton", width=20)
    button_login.grid(row=5, column=0, pady=20, sticky="ew")

    bordered_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()
