import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from open_employee import open_new_window
from statistics import display_statistics
from show_bookings import display_bookings
from admin_cars_list import admin_car_showroom

def show_admin_dashboard():
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Define functions for card actions
    def create_emp():
        open_new_window()

    def car_list():
        admin_car_showroom()

    def booked_details():
        display_bookings()

    def statistics():
        display_statistics()

    # Initialize main window
    root = tk.Toplevel()
    root.title("Admin Dashboard")
    center_window(root, 900, 600)
    root.configure(bg="white")  # Background color

    # Define styles
    style = ttk.Style()
    style.theme_use("clam")

    # Card style for individual cards
    card_width, card_height = 190, 190
    style.configure("Card.TFrame", background="#2B579A", relief="flat")
    style.configure("CardText.TLabel", font=("Times New Roman", 16, "bold"), foreground="white", background="white")

    # Title label
    label_welcome = ttk.Label(root, text="Welcome Admin", font=("times new roman", 30, "bold"), foreground="black", background="white")
    label_welcome.pack(pady=(40, 20))

    # Helper function to create a card that acts as a button
    def create_card(parent, text, image_path, command):
        # Canvas to enforce uniform card size with no highlight or border
        canvas = tk.Canvas(parent, width=card_width, height=card_height, bg="#2B579A", highlightthickness=0, borderwidth=0)
        canvas.pack_propagate(False)  # Prevent resizing

        # Frame to hold card content, with same styling as Canvas
        card = ttk.Frame(canvas, style="Card.TFrame")
        card.place(relx=0.5, rely=0.5, anchor="center")  # Center content in Canvas

        # Load and add image, resizing it to cover the top portion of the card
        try:
            icon = Image.open(image_path).resize((130, 120), Image.LANCZOS)  # Resize image to cover the top
            icon_img = ImageTk.PhotoImage(icon)
            label_icon = tk.Label(card, image=icon_img, background="#2B579A", borderwidth=0, highlightthickness=0, relief="flat")
            label_icon.image = icon_img
            label_icon.pack(pady=(5, 0))  # Adjust padding to add top margin
        except FileNotFoundError:
            print(f"Image '{image_path}' not found")

        # Add text label at the bottom of the card with top margin
        label_text = ttk.Label(card, text=text, style="CardText.TLabel", background="#2B579A")
        label_text.pack(side="bottom", pady=(10, 5))  # Position text at the bottom with top margin

        # Bind the Canvas and its contents to the command
        canvas.bind("<Button-1>", lambda e: command())
        card.bind("<Button-1>", lambda e: command())
        label_icon.bind("<Button-1>", lambda e: command())
        label_text.bind("<Button-1>", lambda e: command())

        return canvas

    # Card details with corresponding actions and images
    card_data = [
        ("Employee details", "employee_icon.png", create_emp),
        ("Cars List", "car_list_icon.png", car_list),
        ("Booked Details", "booked_icon.png", booked_details),
        ("Statistics", "statistics_icon.png", statistics),
    ]

    # Arrange cards in a 2x2 grid layout without styling the frame_cards itself
    frame_cards = tk.Frame(root, bg="white")  # Avoid ttk.Frame to prevent default styling
    frame_cards.pack()

    for i, (text, image, cmd) in enumerate(card_data):
        row, col = divmod(i, 2)
        card = create_card(frame_cards, text, image, cmd)
        card.grid(row=row, column=col, padx=10, pady=10)

    # Logout button at the end of the window
    def logout():
        root.destroy()
        # Close the admin dashboard window
        from main_first import main_screen
        main_screen()  # Reopen the main screen after logout

    # Define a custom style for the logout button
    style.configure("LogoutButton.TButton", 
                    font=("times new roman", 18, "bold"),  # Set a bold font
                    foreground="white",  # Text color
                    background="red",  # Light red background color
                    padding=(10, 5),  # Padding inside the button
                    relief="flat",  # Flat button, no borders
                    width=20)  # Set width to 20 for consistent button size

    # Create the logout button with the custom style
    logout_button = ttk.Button(root, text="Logout", command=logout, style="LogoutButton.TButton")
    logout_button.pack(pady=(15, 10))  # Add padding for spacing before and after the button

    root.mainloop()
