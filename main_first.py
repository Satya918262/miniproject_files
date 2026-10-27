import tkinter as tk
from PIL import Image, ImageTk
from admin_login import show_login_form  # Import the show_login_form function from login.py
from employee_login import employee_login_form

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def open_main(root):  # Pass the root window to close it
    root.destroy()  # Destroy the root window before opening the new one
    show_login_form()

def second_main(root):  # Pass the root window to close it
    root.destroy()  # Destroy the root window before opening the new one
    employee_login_form()

# Function for admin button click
def admin_click(root):
    open_main(root)

# Function for salesperson button click
def salesperson_click(root):
    second_main(root)

# Function to change the background color on hover
def on_enter(button):
    button.config(bg="#0d93c6")  # Lighter green on hover

def on_leave(button):
    button.config(bg="#4CAF50")  # Original dark green when mouse leaves

# Create the main window
def main_screen():
    # Use Toplevel instead of Tk
    root = tk.Toplevel()
    root.title("Welcome Window")
    root.config(bg="#03023c")  # Set the background color
    center_window(root, 900, 550)
    root.resizable(False, False)

    # Create a frame to hold all the content and center everything
    content_frame = tk.Frame(root, bg="#03023c")
    content_frame.pack(expand=True)  # This ensures the content is centered vertically and horizontally

    # Create a label for the text 'Welcome to' with stylish font
    welcome_label = tk.Label(content_frame, text="Welcome to", font=("Times New Roman", 50, "bold"), fg="white", bg="#03023c")
    welcome_label.pack(pady=0)  # Adds some space below the "Welcome to" text

    # Load and display the image below the 'Welcome to' label
    image = Image.open("logo1.jpeg")  # Replace with the correct image path
    resized_image = image.resize((300, 125), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(content_frame, image=photo_image, bg="#03023c")  # Ensure the background is same as window
    image_label.image = photo_image  # Keep a reference to avoid garbage collection
    image_label.pack(pady=10)  # Adds space below the image

    # Create the 'Admin' and 'Salesperson' buttons below the image
    admin_button = tk.Button(content_frame, text="Admin", font=("Times New Roman", 16), fg="white", bg="#4CAF50", 
                             command=lambda: admin_click(root), width=25, height=1)
    admin_button.pack(pady=10)  # Stack buttons vertically with some padding

    # Add hover effect to the Admin button
    admin_button.bind("<Enter>", lambda event, button=admin_button: on_enter(button))
    admin_button.bind("<Leave>", lambda event, button=admin_button: on_leave(button))

    salesperson_button = tk.Button(content_frame, text="Salesperson", font=("Times New Roman", 16), fg="white", bg="#4CAF50", 
                                   command=lambda: salesperson_click(root), width=25, height=1)
    salesperson_button.pack(pady=10)  # Stack buttons vertically with some padding

    # Add hover effect to the Salesperson button
    salesperson_button.bind("<Enter>", lambda event, button=salesperson_button: on_enter(button))
    salesperson_button.bind("<Leave>", lambda event, button=salesperson_button: on_leave(button))

    # Run the Tkinter event loop for this Toplevel window
    root.mainloop()
