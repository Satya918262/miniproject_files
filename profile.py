import tkinter as tk
from tkinter import messagebox
import sqlite3

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def fetch_employee_data(emp_id):
    conn = sqlite3.connect("car_details.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, contact FROM employees WHERE emp_id = ?", (emp_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def update_employee_data(emp_id, first_name, last_name, email, contact):
    conn = sqlite3.connect("car_details.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees 
        SET first_name = ?, last_name = ?, email = ?, contact = ?
        WHERE emp_id = ?""", 
        (first_name, last_name, email, contact, emp_id))
    conn.commit()
    conn.close()

def user_profile(emp_id):
    def toggle_edit_mode():
        nonlocal edit_mode
        edit_mode = not edit_mode
        state = "normal" if edit_mode else "readonly"
        entry_first_name.config(state=state)
        entry_last_name.config(state=state)
        entry_email.config(state=state)
        entry_mobile.config(state=state)
        if edit_mode:
            button_edit.config(text="Save", bg="green")
            messagebox.showwarning("Edit Mode", "Make Changes Carefully.")
        else:
            button_edit.config(text="Edit", bg="#2B579A")

        if not edit_mode:  # Save changes when switching back to non-edit mode
            updated_first_name = first_name_var.get()
            updated_last_name = last_name_var.get()
            updated_email = email_var.get()
            updated_mobile = mobile_var.get()
            update_employee_data(emp_id, updated_first_name, updated_last_name, updated_email, updated_mobile)
            messagebox.showinfo("Success", "Employee details updated successfully!")

    def close_window():
        dashboard.destroy()

    employee_data = fetch_employee_data(emp_id)

    if not employee_data:
        messagebox.showerror("Error", f"No data found for employee ID {emp_id}")
        return

    first_name, last_name, email, contact = employee_data

    dashboard = tk.Toplevel()
    dashboard.title("profile")
    center_window(dashboard, 600, 400)
    dashboard.configure(bg="white")

    heading = tk.Label(
        dashboard,
        text="Profile",
        font=("Times New Roman", 19, "bold"),
        bg="#2B579A",
        fg="white",
        height=2,
    )
    heading.pack(fill=tk.X, pady=(0, 10))

    center_frame = tk.Frame(dashboard, bg="white")
    center_frame.pack(expand=True)

    form_frame = tk.Frame(center_frame, bg="white")
    form_frame.pack(pady=5, padx=50)

    first_name_var = tk.StringVar(value=first_name)
    last_name_var = tk.StringVar(value=last_name)
    email_var = tk.StringVar(value=email)
    mobile_var = tk.StringVar(value=contact)

    edit_mode = False

    label_first_name = tk.Label(form_frame, text="First Name ", font=("Times New Roman", 16), bg="white", fg="black", anchor="w")
    label_first_name.grid(row=0, column=0, pady=(0, 10), sticky="e")
    entry_first_name = tk.Entry(form_frame, textvariable=first_name_var, font=("Times New Roman", 14), width=30, bg="#f0f0f0", relief="solid", borderwidth=1, state="readonly")
    entry_first_name.grid(row=0, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))

    label_last_name = tk.Label(form_frame, text="Last Name ", font=("Times New Roman", 16), bg="white", fg="black", anchor="w")
    label_last_name.grid(row=1, column=0, pady=(0, 10), sticky="e")
    entry_last_name = tk.Entry(form_frame, textvariable=last_name_var, font=("Times New Roman", 14), width=30, bg="#f0f0f0", relief="solid", borderwidth=1, state="readonly")
    entry_last_name.grid(row=1, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))

    label_email = tk.Label(form_frame, text="Email Address ", font=("Times New Roman", 16), bg="white", fg="black", anchor="w")
    label_email.grid(row=2, column=0, pady=(0, 10), sticky="e")
    entry_email = tk.Entry(form_frame, textvariable=email_var, font=("Times New Roman", 14), width=30, bg="#f0f0f0", relief="solid", borderwidth=1, state="readonly")
    entry_email.grid(row=2, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))

    label_mobile = tk.Label(form_frame, text="Mobile Number ", font=("Times New Roman", 16), bg="white", fg="black", anchor="w")
    label_mobile.grid(row=3, column=0, pady=(0, 10), sticky="e")
    entry_mobile = tk.Entry(form_frame, textvariable=mobile_var, font=("Times New Roman", 14), width=30, bg="#f0f0f0", relief="solid", borderwidth=1, state="readonly")
    entry_mobile.grid(row=3, column=1, pady=(0, 10), ipadx=20, ipady=4, padx=(10, 0))

    button_frame = tk.Frame(center_frame, bg="white")
    button_frame.pack(pady=10)

    button_edit = tk.Button(
        button_frame,
        text="Edit",
        font=("Times New Roman", 14, "bold"),
        bg="#2B579A",
        fg="white",
        width=12,
        command=toggle_edit_mode,
    )
    button_edit.grid(row=0, column=0, padx=5)

    button_close = tk.Button(
        button_frame,
        text="Close",
        font=("Times New Roman", 14, "bold"),
        bg="red",
        fg="white",
        width=12,
        command=close_window,
    )
    button_close.grid(row=0, column=1, padx=5)

    dashboard.mainloop()
