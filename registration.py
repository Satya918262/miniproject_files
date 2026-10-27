import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import datetime

def create_employee():
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    # Ensure the database and table are set up
    def setup_database():
        conn = sqlite3.connect("car_details.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                            emp_id TEXT PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            username TEXT,
                            password TEXT,
                            date_of_joining TEXT,
                            email TEXT,
                            contact TEXT,
                            aadhar TEXT UNIQUE,
                            designation TEXT,
                            salary TEXT,
                            address TEXT)''')
        conn.commit()
        conn.close()

    # Generate employee ID, username, and password
    def generate_credentials():
        conn = sqlite3.connect("car_details.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT MAX(emp_id) FROM employees")
        result = cursor.fetchone()

        if result[0] is None:
            emp_id = "EMP" + str(random.randint(1000, 9999))  # Random 4-digit number if no previous record
        else:
            max_id = int(result[0][3:])
            emp_id = "EMP" + str(max_id + 1).zfill(4)

        conn.close()
        
        special_char = random.choice("@#%^&*")

        username = first_name_entry.get().lower() + emp_id[-4:]
        password = first_name_entry.get().upper()[0]+first_name_entry.get()[1:3].lower() + special_char+ aadhar_entry.get()[-4:]

        return emp_id, username, password

    # Validation function
    def validate_fields():
        if not first_name_entry.get() or not last_name_entry.get() or not email_entry.get() or \
           not contact_entry.get() or not address_entry.get("1.0", "end").strip() or \
           not aadhar_entry.get() or not designation_entry.get() or not salary_entry.get():
            messagebox.showerror("Input Error", "All fields are required!")
            return False

        if len(aadhar_entry.get()) != 12 or not aadhar_entry.get().isdigit():
            messagebox.showerror("Input Error", "Aadhar number must contain 12 digits")
            return False

        if len(contact_entry.get()) != 10 or not contact_entry.get().isdigit():
            messagebox.showerror("Input Error", "Phone number must contain 10 digits")
            return False
        
        return True

    def save_to_database():
        if not validate_fields():
            return

        conn = sqlite3.connect("car_details.db")
        cursor = conn.cursor()

        aadhar_number = aadhar_entry.get()
        cursor.execute("SELECT * FROM employees WHERE aadhar = ?", (aadhar_number,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Duplicate Entry", "An employee with this Aadhaar card number already exists.")
            conn.close()
            return

        emp_id, username, password = generate_credentials()
        date_of_joining = datetime.date.today().strftime("%Y-%m-%d")

        cursor.execute('''INSERT INTO employees 
                        (emp_id, first_name, last_name, username, password, date_of_joining, email, contact,  aadhar, designation, salary, address)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',(emp_id, first_name_entry.get(), last_name_entry.get(),username, password, date_of_joining, email_entry.get(),
                         contact_entry.get(),aadhar_number,designation_entry.get(), salary_entry.get(),address_entry.get("1.0", "end").strip() ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Username: {username}\nPassword: {password}\nDate of Joining: {date_of_joining}")
        clear_form()
        root.destroy()

        
    def clear_form():
    # Clear all entry fields and text widgets
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        contact_entry.delete(0, tk.END)
        address_entry.delete("1.0", tk.END)
        aadhar_entry.delete(0, tk.END)
        designation_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)

  
    # Create main window
    root = tk.Toplevel()
    root.title("Employee Registration")
    center_window(root, 700, 550)
    root.config(bg="white")
    heading = tk.Label(root, text="Employee Registration", font=("times new roman", 19, "bold"), width=40, height=2, bg="#2B579A", fg="white")
    heading.pack(fill=tk.X, pady=(0, 10))
    
    center_frame = tk.Frame(root, bg="white")
    center_frame.pack(expand=True)
    form_frame = tk.Frame(center_frame, bg="white")
    form_frame.pack(pady=5, padx=50)

    def create_entry(parent, label_text, row):
        label = tk.Label(parent, text=label_text, font=("times new roman", 16), bg="white", fg='black', anchor="center")
        label.grid(row=row, column=0, pady=(0, 10), sticky="e")
        entry = tk.Entry(parent, font=("times new roman", 14), width=30, bg="#f0f0f0", relief="solid", borderwidth=1)
        entry.grid(row=row, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))
        entry.config(justify="center")
        return entry

    first_name_entry = create_entry(form_frame, "First Name *", 0)
    last_name_entry = create_entry(form_frame, "Last Name *", 1)
    email_entry = create_entry(form_frame, "Email *", 2)
    contact_entry = create_entry(form_frame, "Contact Number *", 3)
    
    address = tk.Label(form_frame, text="Full Address *", font=("times new roman", 16), bg="white", fg='black', anchor="center")
    address.grid(row=4, column=0, pady=(0, 10), sticky="e")
    address_entry = tk.Text(form_frame, font=("times new roman", 14), width=30, height=2, bg="#f0f0f0", relief="solid", borderwidth=1)
    address_entry.grid(row=4, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))
    address_entry.config(wrap="word")
    
    aadhar_entry = create_entry(form_frame, "Aadhar Card No *", 5)
    designation_entry = create_entry(form_frame, "Designation", 6)
    salary_entry = create_entry(form_frame, "Salary", 7)

    button_frame = tk.Frame(center_frame, bg="white")
    button_frame.pack(pady=10)
    save_button = tk.Button(button_frame, text="Save", font=("times new roman", 14, "bold"), bg="#2B579A", fg="white", width=12, command=save_to_database)
    save_button.grid(row=0, column=0, padx=5)

    close_button = tk.Button(button_frame, text="Close", font=("times new roman", 14, "bold"), bg="#2B579A", fg="white", width=12, command=root.destroy)
    close_button.grid(row=0, column=2, padx=5)

    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=1)
    
    setup_database()
    root.mainloop()

