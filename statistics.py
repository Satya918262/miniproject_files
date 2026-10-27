import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def display_statistics():
    # Function to center the window on the screen
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')

    # Function to retrieve statistics from the bookings table
    def retrieve_booking_statistics():
        # Connect to the database
        conn = sqlite3.connect('car_details.db')
        cursor = conn.cursor()

        # Query to get total sales (sum of price)
        cursor.execute("SELECT SUM(price) FROM bookings")
        total_sales = cursor.fetchone()[0]

        # Query to get the total number of bookings
        cursor.execute("SELECT COUNT(*) FROM bookings")
        total_bookings = cursor.fetchone()[0]

        # Query to get bookings per day (grouped by booking_date)
        cursor.execute(""" 
            SELECT strftime('%Y-%m-%d', booking_date) AS day, COUNT(*) 
            FROM bookings 
            GROUP BY strftime('%Y-%m-%d', booking_date)
            ORDER BY day
        """)
        daily_bookings = cursor.fetchall()

        # Query to get car brand sales distribution
        cursor.execute(""" 
            SELECT car_make, SUM(price) 
            FROM bookings 
            GROUP BY car_make
            ORDER BY car_make
        """)
        car_brand_sales = cursor.fetchall()

        # Close the connection
        conn.close()

        return total_sales, total_bookings, daily_bookings, car_brand_sales

    # Function to display booking statistics and graphs
    total_sales, total_bookings, daily_bookings, car_brand_sales = retrieve_booking_statistics()

    # Ensure total_sales is valid (0 if None or negative)
    total_sales = max(0, total_sales if isinstance(total_sales, (int, float)) else 0)
    
    # Ensure total_bookings is valid (0 if None or negative)
    total_bookings = max(0, total_bookings if isinstance(total_bookings, int) else 0)

    # Create the Tkinter window for displaying statistics
    window = tk.Toplevel()
    window.title("Booking Statistics")
    center_window(window, 1100, 600)
    window.configure(bg="white")

    # Add a canvas for displaying graphs with increased width
    canvas_frame = tk.Frame(window, bg="white", bd=2, relief="solid")
    canvas_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    canvas = tk.Canvas(canvas_frame, bg="white", width=800)  # Increase canvas width
    canvas.grid(row=0, column=0, sticky="nsew")

    # Create a frame inside the canvas
    frame = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Title label
    title_label = tk.Label(frame, text="Booking Statistics", font=("times new roman", 20, "bold"), bg="white")
    title_label.grid(row=0, column=0, columnspan=2, pady=15)

    # Total sales label (centered) without a border
    total_sales_label = tk.Label(frame, text=f"Total Sales: ₹{total_sales:,.2f}", font=("times new roman", 18), bg="white", anchor="center")
    total_sales_label.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5, padx=10)

    # Total bookings label (centered) without a border
    total_bookings_label = tk.Label(frame, text=f"Total Bookings: {total_bookings}", font=("times new roman", 18), bg="white", anchor="center")
    total_bookings_label.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5, padx=10)

    # Prepare data for Daily Bookings Graph
    days = [item[0] for item in daily_bookings]
    daily_booking_counts = [item[1] for item in daily_bookings]

    # Prepare data for Car Brand Sales (Pie Chart)
    brands = [item[0] for item in car_brand_sales]
    brand_sales = [item[1] for item in car_brand_sales]

    # Create the figure for plotting graphs
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))

    # Set the figure background color to white
    fig.patch.set_facecolor('white')

    # Graph 1: Daily Bookings (Bar Chart)
    bar_width = 0.2  # Width of individual bars
    positions = range(len(days))
    ax[0].bar(positions, daily_booking_counts, color='skyblue', edgecolor='black', width=bar_width)
    ax[0].set_title('Daily Bookings', fontsize=14, fontweight='bold')
    ax[0].set_xlabel('Date', fontsize=12)
    ax[0].set_ylabel('Number of Bookings', fontsize=12)
    ax[0].set_xticks(positions)  # Set positions for x-ticks
    ax[0].set_xticklabels(days, rotation=0, ha="center", fontsize=10)  # Set dates to horizontal and center align

    # Reduce the overall width of the bar graph by setting x-limits
    ax[0].set_xlim(-0.5, len(days) - 0.5)  # Adjust x-axis limits to compress the graph width

    # Add border around the graph (bar chart)
    for spine in ax[0].spines.values():
        spine.set_edgecolor('black')  # Set color of the border
        spine.set_linewidth(2)        # Set thickness of the border

    # Graph 2: Car Brand Sales Distribution (Pie chart)
    if sum(brand_sales) == 0:
        ax[1].pie([1], labels=["No Sales"], autopct='%1.1f%%', colors=['lightgray'], startangle=90)
        ax[1].set_title('Car Brand Sales Distribution', fontsize=14, fontweight='bold', pad=20)  # Increased padding
    else:
        ax[1].pie(brand_sales, labels=brands, autopct='%1.1f%%', startangle=90)
        ax[1].set_title('Car Brand Sales Distribution', fontsize=14, fontweight='bold', pad=20)  # Increased padding

    # Resize the pie chart to make it larger
    ax[1].axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    # Add spacing between the title and the pie chart
    plt.subplots_adjust(hspace=0.8)

    # Embed the matplotlib figures into the Tkinter window
    canvas_agg = FigureCanvasTkAgg(fig, master=frame)
    canvas_agg.draw()
    canvas_agg.get_tk_widget().grid(row=3, column=0, padx=20, pady=(10, 20), sticky="nsew")

    # Update the scroll region of the canvas dynamically
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Enable mouse scroll zoom behavior
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Update window resizing behavior for both window and canvas
    window.grid_rowconfigure(0, weight=1, uniform="equal")
    window.grid_columnconfigure(0, weight=1, uniform="equal")

    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)

    # Run the Tkinter main loop
    window.mainloop()

