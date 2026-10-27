import tkinter as tk
from tkinter import Label, Frame, Toplevel, Canvas
import sqlite3
from PIL import Image, ImageTk
from io import BytesIO

def run_car_showroom_app():
    # Function to center the window
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Colors for the design
    title_color = "#02013b"  # Dark blue for headings
    text_color = "#0d93c6"   # Light blue for brand names
    background_color = "#f2f2f2"  # Light grey background

    def show_car_models(brand_name, event):
        # Create Toplevel window to show car models
        top = Toplevel(root)
        top.title(f"{brand_name} - Models")
        top.resizable(False, False)
        center_window(top, 800, 600)
        top.configure(bg=background_color)

        # Label to show the selected brand's name at the top of the Toplevel window
        brand_label = Label(top, text=f"{brand_name} Models", font=("times new roman", 26, "bold"), fg=title_color, bg=background_color)
        brand_label.pack(pady=10)

        # Create a frame to center the canvas in the Toplevel window
        frame = Frame(top, bg=background_color)
        frame.pack(side="top", fill="both", expand=True)

        # Create a Canvas widget for scrolling
        canvas = Canvas(frame, bg=background_color)
        canvas.pack(side=tk.TOP, fill="both", expand=True)  # This will center the canvas in the frame

        # Create a frame inside the canvas to hold the car model details
        models_frame = Frame(canvas, bg=background_color, padx=20)
        canvas.create_window((0, 0), window=models_frame, anchor="nw")

        # Query the database to get models of the selected brand
        cursor.execute("""
            SELECT model_name, price, manufacture_year, fuel_type, seating_count, image_data 
            FROM cars 
            WHERE brand_name=?
        """, (brand_name,))

        # Display car models
        for car in cursor.fetchall():
            car_frame = Frame(models_frame, bg="white", padx=30, pady=10, width=350, height=350, 
                              highlightbackground="#000000", highlightthickness=1, relief="solid")
            car_frame.pack(fill="x", pady=10, anchor='center')  # Ensure the card frame is centered

            # Car image
            car_image_blob = car[5]
            if car_image_blob:
                car_image = Image.open(BytesIO(car_image_blob)).resize((400, 200), Image.LANCZOS)
                car_image = ImageTk.PhotoImage(car_image)
                car_image_label = Label(car_frame, image=car_image, bg="white")
                car_image_label.image = car_image  # Keep reference to avoid garbage collection
                car_image_label.grid(row=0, column=0, padx=10, pady=10)

            # Car details
            car_details_frame = Frame(car_frame, bg="white")
            car_details_frame.grid(row=0, column=1, sticky="w", padx=20, pady=10)

            Label(car_details_frame, text=f"Model: {car[0]}", font=("times new roman", 15, "bold"), fg=text_color, bg="white").grid(row=0, column=0, sticky="w", padx=10)
            Label(car_details_frame, text=f"Price: {car[1]}", font=("times new roman", 14), bg="white").grid(row=1, column=0, sticky="w", padx=10)
            Label(car_details_frame, text=f"Year: {car[2]}", font=("times new roman", 14), bg="white").grid(row=2, column=0, sticky="w", padx=10)
            Label(car_details_frame, text=f"Fuel: {car[3]}", font=("times new roman", 14), bg="white").grid(row=3, column=0, sticky="w", padx=10)
            Label(car_details_frame, text=f"Seats: {car[4]}", font=("times new roman", 14), bg="white").grid(row=4, column=0, sticky="w", padx=10)

            car_frame.grid_propagate(False)
            car_frame.config(height=250, width=750)

        # Update the scroll region
        models_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Bind mouse wheel scrolling to the canvas
        canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel(event, canvas))

    def on_mouse_wheel(event, canvas):
        # Detect mouse wheel movement and scroll the canvas
        if event.delta > 0:
            canvas.yview_scroll(-1, "units")  # Scroll up
        else:
            canvas.yview_scroll(1, "units")  # Scroll down

    def display_brand(frame, brand_name, image_path):
        def on_card_click(event):
            show_car_models(brand_name, event)

        # Load the brand image
        logo_image = Image.open(image_path).resize((150, 90), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Card frame with fixed width, height, and updated border style
        card_frame = Frame(frame, padx=10, pady=10, bg=background_color, width=200, height=250, 
                           highlightbackground="#000000", highlightthickness=2, relief="solid")
        card_frame.pack(side=tk.LEFT, padx=20, pady=10, anchor='center', expand=True)  # Ensure the card frame is centered

        # Bind the click event to the entire card frame, brand image, and brand text
        card_frame.bind("<Button-1>", on_card_click)

        # Brand logo
        logo_label = Label(card_frame, image=logo_photo, bg=background_color)
        logo_label.image = logo_photo  # Keep reference to avoid garbage collection
        logo_label.pack()

        # Brand name label
        name_label = Label(card_frame, text=brand_name, font=("Helvetica", 14), fg=text_color, bg=background_color)
        name_label.pack()

        # Bind brand text click event
        name_label.bind("<Button-1>", on_card_click)

        # Bind brand logo click event
        logo_label.bind("<Button-1>", on_card_click)

    # Initialize the main window
    root = tk.Toplevel()
    root.title("Car Showroom - Car Models")
    center_window(root, 900, 650)

    # Setting background color
    root.configure(bg=background_color)

    # Top heading for "Top Brands"
    top_heading = Label(root, text="Top Brands", font=("times new roman", 26, "bold"), fg=title_color, bg=background_color)
    top_heading.pack(pady=(20, 10))

    # Frame to hold top brand images and names
    top_brands_frame = Frame(root, bg=background_color)
    top_brands_frame.pack(pady=10)

    # Database setup
    conn = sqlite3.connect("car_details.db")
    cursor = conn.cursor()

    # Top brands data
    top_brands = {
        "Benz": "mercedes_logo.jpg",
        "Land Rover": "land_rover.png",
        "Suzuki": "suzuki.png",
        "Skoda": "skoda.png"
    }

    # Display top brands
    for brand, logo_path in top_brands.items():
        display_brand(top_brands_frame, brand, logo_path)

    # Heading for "Other Brands"
    other_heading = Label(root, text="Other Brands", font=("times new roman", 26, "bold"), fg=title_color, bg=background_color)
    other_heading.pack(pady=(30, 10))

    # Frame to hold other brand images and names
    other_brands_frame = Frame(root, bg=background_color)
    other_brands_frame.pack(pady=10)

    # Other brands data
    other_brands = {
        "Toyota": "toyota_logo.png",
        "Honda": "honda_logo.jpg",
        "Ford": "ford_logo.png",
        "BMW": "bmw_logo.jpg"
    }

    # Display other brands
    for brand, logo_path in other_brands.items():
        display_brand(other_brands_frame, brand, logo_path)

    # Run the Tkinter event loop
    root.mainloop()

    # Close the database connection
    conn.close()

