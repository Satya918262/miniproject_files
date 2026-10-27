import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from main_first import main_screen

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def open_main_screen():
    splash.withdraw()  # Close the splash screen
    main_screen()      # Open the main screen from ms.py

# Create the splash screen
splash = tk.Tk()
splash.title('Splash Screen')
center_window(splash, 650, 500)
splash.overrideredirect(True)  # Remove window borders

# Load and display the image on the splash screen
image = Image.open("logo.jpeg")
resized_image = image.resize((650, 500), Image.LANCZOS)
photo_image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(splash, image=photo_image, bd=0)  # bd=0 removes any border/padding
image_label.place(x=0, y=0)  # Position the image at the top-left corner

# Add a progress bar directly on top of the image
progress = ttk.Progressbar(splash, orient="horizontal", mode="determinate", length=650)
progress.place(x=0, y=480)  # Place the progress bar directly on top of the image (at the bottom)

# Function to fill the progress bar over time
def load_progress():
    for i in range(101):  # Fills the bar from 0% to 100%
        progress['value'] = i
        splash.update_idletasks()  # Update the splash screen to show progress
        splash.after(15)  # Adjust the delay for a smooth loading animation

    # Once loading is done, open the main window
    open_main_screen()

# Start the progress bar animation and open the main window after loading completes
splash.after(100, load_progress)  # Delay the loading process to allow splash screen to render

# Run the splash screen
splash.mainloop()
