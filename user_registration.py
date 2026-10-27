import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import random
import sqlite3
from generateinvoice import generate_invoice
def userregistration(empid,fname):
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    def generate_customer_id():
        return f"CUST{random.randint(1000, 9999)}"

    def generate_booking_id():
        # Randomly generate a booking ID
        return random.randint(100000, 999999)

    def validate_fields():
        if not fullname_entry.get() or not email_entry.get() or \
           not contact_entry.get() or not address_entry.get("1.0", "end").strip() or not aadhar_entry.get():
            messagebox.showerror("Input Error", "All fields are required!")
            return False

        if len(aadhar_entry.get()) != 12 or not aadhar_entry.get().isdigit():
            messagebox.showerror("Input Error", "Aadhar number must contain 12 digits")
            return False
        if len(contact_entry.get()) != 10 or not contact_entry.get().isdigit():
            messagebox.showerror("Input Error", "Phone number must contain 10 digits")
            return False

        current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect("car_details.db")
        cursor = conn.cursor()

    # Create a table for storing bookings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY,
            salesman_id TEXT,
            customer_id TEXT,
            customer_name TEXT,
            email TEXT,
            contact_number TEXT,
            address TEXT,
            aadhar_number TEXT,
            car_make TEXT,
            car_model TEXT,
            price REAL,
            booking_date TIMESTAMP
        )
        """)
        conn.commit()
        booking_id = generate_booking_id()
        cursor.execute("""
            INSERT INTO bookings (booking_id,salesman_id, customer_id, customer_name, email, contact_number, address, aadhar_number, car_make, car_model, price,booking_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
            """, (
            booking_id,
            empid, 
            customer_id_entry.get(), 
            fullname_entry.get(), 
            email_entry.get(), 
            contact_entry.get(), 
            address_entry.get("1.0", "end").strip(), 
            aadhar_entry.get(), 
            make_var.get(), 
            model_var.get(), 
            price_entry.get(),
            current_timestamp
        ))
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        show_booking_success_screen(booking_id)
        return True

    def show_user_details_screen():
        next_frame.pack_forget()
        success_frame.pack_forget()
        form_frame.pack(expand=True, fill=tk.BOTH)

    def show_car_details_screen():
        form_frame.pack_forget()
        success_frame.pack_forget()
        next_frame.pack(expand=True, fill=tk.BOTH)

    def show_booking_success_screen(booking_id):
        next_frame.pack_forget()
        form_frame.pack_forget()
        success_frame.pack(expand=True, fill=tk.BOTH)
        success_button.config(command=lambda: generate_invoice(booking_id))

    # Fetch car makes and models from database
    def fetch_car_details():
        conn = sqlite3.connect("car_details.db")
        cursor = conn.cursor()
       
        cursor.execute("SELECT DISTINCT brand_name FROM cars")
        makes = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT model_name, brand_name, fuel_type, manufacture_year, price, seating_count FROM cars")
        car_details = cursor.fetchall()
       
        conn.close()

        # Organize car details by brand
        car_details_by_brand = {}
        for model, brand, fuel, year, price, seats in car_details:
            if brand not in car_details_by_brand:
                car_details_by_brand[brand] = []
            car_details_by_brand[brand].append({
                "model_name": model,
                "fuel_type": fuel,
                "manufacture_year": year,
                "price": price,
                "seating_count": seats
            })

        return makes, car_details_by_brand

    # Initialize the main window
    root = tk.Toplevel()
    root.title("Car Booking")
    center_window(root, 700, 550)
    root.config(bg="white")

    heading = tk.Label(root, text="Car Booking", font=("times new roman", 19, "bold"), width=40, height=2, bg="#2B579A", fg="white")
    heading.pack(fill=tk.X, pady=(0, 10))

    center_frame = tk.Frame(root, bg="white")
    center_frame.pack(expand=True)

    # Create the form_frame (user details form)
    form_frame = tk.Frame(center_frame, bg="white")

    def create_entry(parent, label_text, row, readonly=False):
        label = tk.Label(parent, text=label_text, font=("times new roman", 16), bg="white", fg='black', anchor="center")
        label.grid(row=row, column=0, pady=(0, 10), sticky="e")
       
        entry = tk.Entry(parent, font=("times new roman", 14), width=30, bg="#f0f0f0", relief="solid", borderwidth=1, justify="center")
        if readonly:
            entry.config(state="readonly")
        entry.grid(row=row, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))
        return entry

    # Generate customer ID and set it to readonly
    customer_id = generate_customer_id()
    customer_id_entry = create_entry(form_frame, "Customer ID", 0, readonly=True)
    customer_id_entry.config(state="normal")  # Temporarily enable entry to set value
    customer_id_entry.insert(0, customer_id)
    customer_id_entry.config(state="readonly")  # Make it readonly again

    fullname_entry = create_entry(form_frame, "Customer Name", 1)
    email_entry = create_entry(form_frame, "Email", 2)
    contact_entry = create_entry(form_frame, "Contact Number", 3)
   
    address_label = tk.Label(form_frame, text="Full Address *", font=("times new roman", 16), bg="white", fg='black', anchor="center")
    address_label.grid(row=4, column=0, pady=(0, 10), sticky="e")
    address_entry = tk.Text(form_frame, font=("times new roman", 14), width=34, height=2, bg="#f0f0f0", relief="solid", borderwidth=1, wrap="word")
    address_entry.grid(row=4, column=1, pady=(0, 10), ipadx=3, ipady=4, padx=(10, 0))

    aadhar_entry = create_entry(form_frame, "Aadhar Card No *", 5)

    back_button = tk.Button(form_frame, text="Back to Registration", font=("times new roman", 14, "bold"), bg="#2B579A", fg="white", command=lambda: [form_frame.pack_forget(), next_frame.pack(expand=True, fill=tk.BOTH)])
    back_button.grid(row=7, column=0, pady=10,padx=10, sticky="ew")

    submit_button = tk.Button(form_frame, text="Submit", font=("times new roman", 14, "bold"), bg="#2B579A", fg="white", width=20,command=validate_fields)
    submit_button.grid(row=7, column=1, pady=10, sticky="ew")

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)

    # Create the next_frame (car details form)
    next_frame = tk.Frame(center_frame, bg="white")

    # Car Details Screen
    next_label = tk.Label(next_frame, text="Car Details", font=("times new roman", 18, "bold"), bg="white", fg="black")
    next_label.grid(row=0, column=0, columnspan=2, pady=5)

    # Fetch car details and populate dropdowns
    car_makes, car_details_by_brand = fetch_car_details()
    style = ttk.Style()
    style.configure("TCombobox",
                font=("Times New Roman", 14),    # Set a larger, readable font
                padding=5,                 # Add padding around the text
                foreground="black",        # Set text color to black
                background="white",
                fieldbackground="white",
                relief="solid",           # gives a border to the combobox
                borderwidth=1)       # Set background color to white

    style.map("TCombobox",
              fieldbackground=[('readonly', 'white')],
              background=[('readonly', 'white')])
    
    salesman_entry = create_entry(next_frame, "Salesperson Id", 1)
    salesman_entry.insert(0, f"{empid}")
    # Car Make Dropdown
    make_label = tk.Label(next_frame, text="Car Make", font=("times new roman", 16), bg="white")
    make_label.grid(row=2, column=0, pady=10, sticky="e")
    make_var = tk.StringVar(next_frame)
    make_dropdown = ttk.Combobox(next_frame, textvariable=make_var, values=car_makes, font=("times new roman", 14), width=32,state="readonly",style="TCombobox")
    make_dropdown.grid(row=2, column=1, padx=15, pady=10)

    # Car Model Dropdown
    model_label = tk.Label(next_frame, text="Car Model", font=("times new roman", 16), bg="white")
    model_label.grid(row=3, column=0, pady=10, sticky="e")
    model_var = tk.StringVar(next_frame)
    model_dropdown = ttk.Combobox(next_frame, textvariable=model_var, values=[], font=("times new roman", 14), width=32,state="readonly",style="TCombobox")
    model_dropdown.grid(row=3, column=1, padx=10, pady=10)

    # Auto-fill car details based on selected model
    def on_brand_select(event):
        selected_brand = make_var.get()
        if selected_brand:
            # Update model dropdown with models based on selected brand
            model_dropdown['values'] = [car["model_name"] for car in car_details_by_brand.get(selected_brand, [])]
            model_dropdown.set('')  # Clear any previously selected model

            # Reset the car details fields
            fuel_type_entry.config(state="normal")
            fuel_type_entry.delete(0, tk.END)
            year_entry.config(state="normal")
            year_entry.delete(0, tk.END)
            price_entry.config(state="normal")
            price_entry.delete(0, tk.END)
            seats_entry.config(state="normal")
            seats_entry.delete(0, tk.END)

    def on_model_select(event):
        selected_brand = make_var.get()
        selected_model = model_var.get()
       
        if selected_brand and selected_model:
            car_details = next((car for car in car_details_by_brand[selected_brand] if car["model_name"] == selected_model), None)
           
            if car_details:
                # Clear previous values
                fuel_type_entry.config(state="normal")
                year_entry.config(state="normal")
                price_entry.config(state="normal")
                seats_entry.config(state="normal")

                # Fill the fields with new data
                fuel_type_entry.delete(0, tk.END)
                fuel_type_entry.insert(0, car_details["fuel_type"])
                fuel_type_entry.config(state="readonly")
               
                year_entry.delete(0, tk.END)
                year_entry.insert(0, car_details["manufacture_year"])
                year_entry.config(state="readonly")
               
                price_entry.delete(0, tk.END)
                price_entry.insert(0, car_details["price"])
                price_entry.config(state="readonly")
               
                seats_entry.delete(0, tk.END)
                seats_entry.insert(0, car_details["seating_count"])
                seats_entry.config(state="readonly")

    make_dropdown.bind("<<ComboboxSelected>>", on_brand_select)
    model_dropdown.bind("<<ComboboxSelected>>", on_model_select)

    # Car Details Entry Fields (non-editable)
    fuel_type_entry = create_entry(next_frame, "Fuel Type", 4, readonly=True)
    year_entry = create_entry(next_frame, "Manufacture Year", 5, readonly=True)
    price_entry = create_entry(next_frame, "Price", 6, readonly=True)
    seats_entry = create_entry(next_frame, "Seating Capacity", 7, readonly=True)

    next_button = tk.Button(next_frame, text="Next", font=("times new roman", 14, "bold"), bg="#2B579A", fg="white", width=20,command=show_user_details_screen)
    next_button.grid(row=8, column=0, columnspan=2, pady=10,sticky='ew')

    # Create success_frame (Booking Successful)
    success_frame = tk.Frame(center_frame, bg="white")
    success_label = tk.Label(success_frame, text="Booking Successful!", font=("times new roman", 20, "bold"), bg="white", fg="green")
    success_label.pack(pady=20)

    success_button = tk.Button(success_frame, text="Generate Invoice", font=("times new roman", 14, "bold"), bg="#2B579A", fg="white", width=20)
    success_button.pack(pady=10)# Show the registration form first
    
    next_frame.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
