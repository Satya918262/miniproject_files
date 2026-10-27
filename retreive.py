import sqlite3
import tkinter as tk
from tkinter import ttk

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to retrieve data from the database
def retrieve_data():
    # Connect to the database
    conn = sqlite3.connect('car_details.db')
    cursor = conn.cursor()

    # Fetch all data from the employee table
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()
    
    return rows

# Function to display the data in a table
def display_data():
    # Create the Tkinter window
    window = tk.Toplevel()
    window.title("Employee Data")
    center_window(window, 1000, 550)

    # Create a frame to center the Treeview within the window
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True, fill=tk.BOTH, pady=50)  # Centered with padding

    # Create a Canvas widget to hold the Treeview
    canvas = tk.Canvas(main_frame)
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Create a frame to hold the Treeview widget inside the Canvas
    tree_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=tree_frame, anchor="nw")

    # Create a scrollbar container frame for the horizontal scrollbar (at the bottom)
    h_scrollbar_frame = tk.Frame(window)
    h_scrollbar_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    # Create the horizontal scrollbar and link it to the Canvas
    h_scrollbar = tk.Scrollbar(h_scrollbar_frame, orient="horizontal", command=canvas.xview, width=20)
    h_scrollbar.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Link the horizontal scrollbar to the canvas
    canvas.configure(xscrollcommand=h_scrollbar.set)

    # Style customization for the Treeview with column borders
    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=50,
                    background="white",
                    fieldbackground="white",
                    font=("times new roman", 13),
                    borderwidth=0,
                    relief="flat",
                    padding=(5, 2))  # Add padding for visual separation
    style.configure("Treeview.Heading",
                    background="lightgrey",
                    foreground="black",
                    font=('times new roman', 13, 'bold'),
                    borderwidth=1,
                    relief="raised")  # Raised effect for header border
    style.map("Treeview", background=[('selected', '#C0C0C0')])

    # Create a Treeview widget for the table
    tree = ttk.Treeview(tree_frame, columns=("ID", "First Name", "Last Name", "Username", "Password", "DOJ", "Email", "Phone", "Aadhar", "Designation", "Salary", "Address"),
                        show="headings", style="Treeview")

    # Define headings
    tree.heading("ID", text="Employee ID")
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.heading("DOJ", text="Date of Joining")
    tree.heading("Email", text="Email Address")
    tree.heading("Phone", text="Phone Number")
    tree.heading("Aadhar", text="Aadhar")
    tree.heading("Designation", text="Designation")
    tree.heading("Salary", text="Salary")
    tree.heading("Address", text="Employee Address")

    # Define different column widths for each column
    column_widths = {
        "ID": 150,
        "First Name": 160,
        "Last Name": 160,
        "Username": 140,
        "Password": 140,
        "DOJ": 140,
        "Email": 350,
        "Phone": 130,
        "Aadhar": 150,
        "Designation": 180,
        "Salary": 100,
        "Address": 400
    }

    # Define columns and set widths
    for col in tree["columns"]:
        tree.column(col, width=column_widths.get(col, 100), anchor="center")

    # Fetch data from the database
    rows = retrieve_data()

    # Insert data into the Treeview with alternating row colors
    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert("", tk.END, values=row, tags=(tag,))

    # Configure the tags for alternating row colors
    tree.tag_configure('evenrow', background='white')
    tree.tag_configure('oddrow', background='#f0f0f0')

    # Pack the Treeview widget within the frame
    tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # Update the scrollable region of the canvas to include the Treeview widget
    tree_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Enable mouse scrolling
    def on_mouse_wheel(event):
        # Scroll up/down based on the wheel direction
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Bind mouse scroll to canvas
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Run the Tkinter main loop
    window.mainloop()
