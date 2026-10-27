import tkinter as tk
from registration import create_employee
from retreive import display_data

# Function to center the window
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Function to change button color on hover
def on_enter(button):
    button.config(bg="#4CAF50")  

def on_leave(button):
    button.config(bg="#0d93c6")

def addemployee():
    create_employee()

def viewemployee():
    display_data()

# Function to open a new window with two buttons
def open_new_window():
    new_window = tk.Toplevel()
    new_window.title("Employee Details")
    new_window.config(bg="white")
    center_window(new_window, 500, 400)
    new_window.resizable(False, False)

    # Create a frame to center the buttons
    button_frame = tk.Frame(new_window, bg="white")
    button_frame.pack(expand=True)

    # Create the first button
    button1 = tk.Button(button_frame, text="View Employee Details", font=("Times New Roman", 16), fg="white", bg="#0d93c6", width=20,command=viewemployee)
    button1.pack(pady=10)

    # Add hover effect to Button 1
    button1.bind("<Enter>", lambda event: on_enter(button1))
    button1.bind("<Leave>", lambda event: on_leave(button1))

    # Create the second button
    button2 = tk.Button(button_frame, text="Add New Employee", font=("Times New Roman", 16), fg="white", bg="#0d93c6", width=20,command=addemployee)
    button2.pack(pady=10)

    # Add hover effect to Button 2
    button2.bind("<Enter>", lambda event: on_enter(button2))
    button2.bind("<Leave>", lambda event: on_leave(button2))

    new_window.mainloop()

