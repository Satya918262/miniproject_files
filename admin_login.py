import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from admin_dashboard import show_admin_dashboard

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_login_form():
    def login():
        username = entry_username.get()
        password = entry_password.get()
        if username=='root' and password=='123':
            root.withdraw()
            show_admin_dashboard()
        else:
            messagebox.showwarning("Error","All details are required")

    # Initialize main window
    root = tk.Toplevel()
    root.title("Responsive Login Form")
    center_window(root, 900, 550)  # Adjusted window size
    root.minsize(400, 300)
    root.configure(bg="white")  # Dark purple background for the window

    # Style configuration
    style = ttk.Style()
    style.configure("Custom.TFrame", background="#2B579A")
    style.configure("Custom.TLabel", background="#2B579A", foreground="white", font=("Times New Roman", 24))
    style.configure("Custom.TButton", font=("Times New Roman", 16, "bold"), padding=(10, 5))  # Style for the button

    # Center frame
    main_frame = ttk.Frame(root, padding="5 5 5 5", style="Custom.TFrame")
    main_frame.pack(expand=True)

    # Outer frame to act as a border with a different color, no border width
    border_color = "#FFFFFF"  # White border
    outer_frame = tk.Frame(main_frame, background=border_color, borderwidth=0, relief="flat")
    outer_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # Inner frame with the main background color, inside the outer border frame
    bordered_frame = ttk.Frame(outer_frame, padding="20", style="Custom.TFrame")
    bordered_frame.grid(row=0, column=0, sticky="nsew")

    # Login Heading inside the bordered frame
    label_heading = ttk.Label(bordered_frame, text="Admin Login", font=("Times New Roman", 35, "bold"), background="#2B579A", foreground="white", anchor='center')
    label_heading.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    # Username label
    label_username = ttk.Label(bordered_frame, text="Username:", font=("Times New Roman", 16), background="#2B579A", foreground="white")
    label_username.grid(row=1, column=0, sticky="w", pady=(10, 5))

    # Username entry with a white border
    username_frame = tk.Frame(bordered_frame, background="white")  # White border frame
    username_frame.grid(row=2, column=0, pady=(10, 5), sticky="ew")
    entry_username = tk.Entry(
        username_frame,
        insertbackground='white',
        width=25,
        font=("Times New Roman", 16),
        bg="#2B579A",
        fg="white",
        bd=0,  # No internal border
        highlightthickness=0  # No highlight border
    )
    entry_username.pack(fill="both", padx=2, pady=2)  # Padding inside the white border

    # Password label and entry
    label_password = ttk.Label(bordered_frame, text="Password:", font=("Times New Roman", 16), background="#2B579A", foreground="white")
    label_password.grid(row=3, column=0, sticky="w", pady=(10, 5))

    # Password entry with the same height as username entry
    password_frame = tk.Frame(bordered_frame, background="white")  # White border frame
    password_frame.grid(row=4, column=0, pady=(10, 5), sticky="ew")
    entry_password = tk.Entry(password_frame, show="*", insertbackground='white', width=25, font=("Arial", 16), bg="#2B579A", fg="white", bd=0, highlightthickness=0, highlightcolor='white', highlightbackground="white")
    entry_password.pack(fill="both", padx=2, pady=2)  # Padding inside the white border

    # Login button with increased width, height, and font style applied through "Custom.TButton" style
    button_login = ttk.Button(bordered_frame, text="Login", command=login, style="Custom.TButton", width=20)
    button_login.grid(row=5, column=0, pady=20, sticky="ew")

    # Make widgets responsive to resizing
    bordered_frame.grid_columnconfigure(0, weight=1)

    root.mainloop()

