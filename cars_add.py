import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
from PIL import Image, ImageTk
import io
import requests
from io import BytesIO

# Function to create the database and table (with image as BLOB and seating count)
def create_db():
    conn = sqlite3.connect('car_details.db')
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist, with image as BLOB and seating_count column
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand_name TEXT,
            model_name TEXT,
            manufacture_year INTEGER,
            price REAL,
            fuel_type TEXT,
            seating_count INTEGER,
            image_data BLOB
        )
    ''')
    conn.commit()
    conn.close()
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_data = BytesIO(response.content)
        return image_data.read()
    else:
        raise Exception("Failed to download image")

# Function to insert car details into the database (with image as BLOB and seating count)
def submit_car_details(dropdown_brand, entry_model, entry_year, entry_price, entry_image, fuel_type_var, entry_seating):
    brand_name = dropdown_brand.get()
    model_name = entry_model.get()
    manufacture_year = entry_year.get()
    price = entry_price.get()
    image_path = entry_image.get()
    fuel_type = fuel_type_var.get()
    seating_count = entry_seating.get()

    if not all([brand_name, model_name, manufacture_year, price, image_path, fuel_type, seating_count]):
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        # Check if the image path is a URL or local file
        if image_path.startswith("http://") or image_path.startswith("https://"):
            image_data = download_image(image_path)  # Download and convert the image from URL
        else:
            with open(image_path, 'rb') as file:
                image_data = file.read()  # Read the local file into binary data

        # Connect to the database and insert the car details with the image as BLOB
        conn = sqlite3.connect('car_details.db')
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO cars (brand_name, model_name, manufacture_year, price, fuel_type, seating_count, image_data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (brand_name, model_name, manufacture_year, price, fuel_type, seating_count, image_data))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Car details submitted successfully!")

        # Reset the form fields after successful submission
        dropdown_brand.set("Select a brand")
        dropdown_brand.configure(background="white", foreground="black")
        entry_model.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_image.delete(0, tk.END)
        entry_seating.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {str(e)}")

# Function to browse and select an image file
def browse_image(entry_image):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        entry_image.delete(0, tk.END)
        entry_image.insert(0, file_path)

# Function to center window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Car details form function
def car_details_form():
    car_window = tk.Toplevel()
    car_window.title("Car Details Form")
    center_window(car_window, 700, 500)
    car_window.config(bg="white")

    heading = tk.Label(car_window, text="Car Details", font=("Times new roman", 26, "bold"), bg="#4A4E57", height=2, fg="white")
    heading.pack(fill=tk.X, pady=(0, 10))

    form_frame = tk.Frame(car_window, bg="white")
    form_frame.pack(pady=5, padx=50, expand=True)

    car_brands = ["Benz", "Land Rover", "Suzuki", "Skoda", "Toyota", "Honda", "Ford", "BMW"]

    # Style for combobox without forced border
    style = ttk.Style()
    style.configure("TCombobox",
                font=("Times New Roman", 14),    # Set a larger, readable font
                padding=5,                 # Add padding around the text
                foreground="black",        # Set text color to black
                background="white",
                fieldbackground="white",)       # Set background color to white

    style.map("TCombobox",
              fieldbackground=[('readonly', 'white')],
              background=[('readonly', 'white')])

    label_brand = tk.Label(form_frame, text="Brand Name", font=("Times new roman", 16), bg="white", fg='black')
    label_brand.grid(row=0, column=0, pady=(0, 10), sticky="e")

    # Frame to wrap the dropdown for the border effect
    dropdown_frame = tk.Frame(form_frame, bg="white", bd=0.05)  # White frame with no gray background
    dropdown_frame.grid(row=0, column=1, pady=(0, 10), padx=(10, 0), sticky="nsew")

    # Dropdown without extra forced border inside the frame
    dropdown_brand = ttk.Combobox(dropdown_frame, values=car_brands, font=("times new roman", 14), width=28, style="TCombobox", state="readonly")
    dropdown_brand.set("Select a brand")
    dropdown_brand.pack(fill=tk.BOTH, padx=1, pady=1)  # Padding to create space from the frame border

    # Function to create entry fields
    def create_entry(parent, label_text, row):
        label = tk.Label(parent, text=label_text, font=("Times new roman", 16), bg="white", fg='black')
        label.grid(row=row, column=0, pady=(0, 10), sticky="e")
        
        entry = tk.Entry(parent, font=("Arial", 12), width=30, bg="#FFFFFF", relief="solid", borderwidth=1)
        entry.grid(row=row, column=1, pady=(0, 10), padx=(10, 0), ipadx=10, ipady=4)
        return entry

    entry_model = create_entry(form_frame, "Model", 1)
    entry_price = create_entry(form_frame, "Price", 2)
    entry_year = create_entry(form_frame, "Manufacture Year", 3)

    # Fuel type section with radio buttons
    label_fuel_type = tk.Label(form_frame, text="Fuel Type", font=("Times new roman", 16), bg="white", fg='black')
    label_fuel_type.grid(row=4, column=0, pady=(0, 5), sticky="e")  # Reduced pady here

    # Create a variable to hold the selected fuel type
    fuel_type_var = tk.StringVar(value="Petrol")

    # Create a frame to hold radio buttons in one row
    fuel_frame = tk.Frame(form_frame, bg="white")
    fuel_frame.grid(row=4, column=1, columnspan=2, pady=(0, 12), sticky="w")

    style = ttk.Style()
    style.configure("TRadiobutton",
                background="white",  # Set the background to white
                foreground="black",  # Set the text color to black
                font=("Times new roman", 14),   # Set the font
                padding=3)   

    # Create radio buttons after defining styles
    radiobutton_petrol = ttk.Radiobutton(fuel_frame, text="Petrol", variable=fuel_type_var, value="Petrol",style="TRadiobutton")
    radiobutton_petrol.pack(side="left", padx=10)

    radiobutton_diesel = ttk.Radiobutton(fuel_frame, text="Diesel", variable=fuel_type_var, value="Diesel",style="TRadiobutton")
    radiobutton_diesel.pack(side="left", padx=10)

    radiobutton_petrol = ttk.Radiobutton(fuel_frame, text="Hybrid", variable=fuel_type_var, value="Hybrid",style="TRadiobutton")
    radiobutton_petrol.pack(side="left", padx=10)

    radiobutton_electric = ttk.Radiobutton(fuel_frame, text="Electric", variable=fuel_type_var, value="Electric",style="TRadiobutton")
    radiobutton_electric.pack(side="left", padx=10)

    entry_seating = create_entry(form_frame, "Seating Count", 5)

    label_image = tk.Label(form_frame, text="Image", font=("Times new roman", 16), bg="white", fg='black')
    label_image.grid(row=6, column=0, pady=(0, 10), sticky="e")
    
    entry_image = tk.Entry(form_frame, font=("Arial", 12), width=30, bg="#FFFFFF", relief="solid", borderwidth=1)
    entry_image.grid(row=6, column=1, pady=(0, 10), padx=(10, 0), ipadx=10, ipady=4)

    button_browse = tk.Button(form_frame, text="Browse", font=("Times new roman", 14), bg="#0d93c6", fg="white", command=lambda: browse_image(entry_image))
    button_browse.grid(row=6, column=2, pady=(0, 10), padx=(10, 0))

    submit_button = tk.Button(form_frame, text="Submit", font=("Times new roman", 16), bg="#4A4E57", fg="white", width=12,
                            command=lambda: submit_car_details(dropdown_brand, entry_model, entry_year, entry_price, entry_image, fuel_type_var, entry_seating))
    submit_button.grid(row=7, column=1, pady=0)

    car_window.mainloop()

