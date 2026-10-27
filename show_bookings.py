import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to retrieve data from the bookings table based on emp_id
def retrieve_bookings_by_emp_id():
    # Connect to the database
    conn = sqlite3.connect('car_details.db')
    cursor = conn.cursor()

    # Query to fetch bookings for the given emp_id
    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()
    
    return rows

# Function to display bookings
def display_bookings():
    # Fetch bookings for the given employee ID
    rows = retrieve_bookings_by_emp_id()

    if not rows:
        messagebox.showerror("No Data", f"No bookings found for Employee ID")
        return

    # Create the Tkinter window
    window = tk.Toplevel()
    window.title(f"Bookings")
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
    tree = ttk.Treeview(tree_frame, columns=("Booking ID", "Salesman ID", "Customer ID", "Customer Name", "Email", "Contact Number", 
                                              "Address", "Aadhar Number", "Car Make", "Car Model", "Price", "Booking Date"),
                        show="headings", style="Treeview")

    # Define headings
    tree.heading("Booking ID", text="Booking ID")
    tree.heading("Salesman ID", text="Salesman ID")
    tree.heading("Customer ID", text="Customer ID")
    tree.heading("Customer Name", text="Customer Name")
    tree.heading("Email", text="Email")
    tree.heading("Contact Number", text="Contact Number")
    tree.heading("Address", text="Address")
    tree.heading("Aadhar Number", text="Aadhar Number")
    tree.heading("Car Make", text="Car Make")
    tree.heading("Car Model", text="Car Model")
    tree.heading("Price", text="Price")
    tree.heading("Booking Date", text="Booking Date")

    # Define columns and set widths
    column_widths = {
        "Booking ID": 150,
        "Salesman ID": 160,
        "Customer ID": 160,
        "Customer Name": 250,
        "Email": 250,
        "Contact Number": 150,
        "Address": 300,
        "Aadhar Number": 180,
        "Car Make": 150,
        "Car Model": 150,
        "Price": 120,
        "Booking Date": 180
    }

    for col in tree["columns"]:
        tree.column(col, width=column_widths.get(col, 100), anchor="center")

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

