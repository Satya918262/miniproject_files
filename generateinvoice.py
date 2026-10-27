import os
import sqlite3
from fpdf import FPDF
from datetime import datetime
from tkinter import messagebox

# Function to fetch booking details from the database
def fetch_booking_details(booking_id):
    """Fetch booking details from the SQLite database."""
    conn = sqlite3.connect('car_details.db')  # Adjust the database path if needed
    cursor = conn.cursor()

    try:
        # Query to fetch booking details based on booking_id
        cursor.execute("""
            SELECT customer_name, car_make, car_model, price, booking_date 
            FROM bookings 
            WHERE booking_id=?
        """, (booking_id,))
        booking_details = cursor.fetchone()

        if booking_details:
            return booking_details  # Returns a tuple with booking details
        else:
            print(f"No booking found with ID: {booking_id}")
            return None
    except Exception as e:
        print(f"Database Error: {e}")
        return None
    finally:
        conn.close()

# Function to generate the PDF invoice
def generate_invoice(booking_id):
    """Generate a PDF invoice using FPDF based on the fetched data."""
    booking_details = fetch_booking_details(booking_id)

    if booking_details:
        # Extract details
        customer_name, car_make, car_model, price, booking_date = booking_details

        pdf = FPDF(format='A4')
        pdf.add_page()

        margin = 7  # Adjust the margin if needed
        pdf.rect(margin, margin, pdf.w - 2 * margin, pdf.h - 2 * margin)

        # Header Section
        pdf.ln(5)
        pdf.set_font("Times", style="B", size=30)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="Invoice", ln=0, align="L")  # Top-left corner
        pdf.image("blss_logo.png", x=160, y=10, w=40)  # Top-right corner
        pdf.ln(20)
        pdf.line(10, 30, 200, 30)  # Horizontal line divider
        pdf.ln(10)

        # Showroom Details
        pdf.set_x(15)
        pdf.set_font("Times", style="B", size=16)
        pdf.cell(100, 10, txt="Bliss Car Showroom", ln=1)
        pdf.set_font("Times", size=14)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="Address: 123, Main Street, City", ln=1)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="Contact: 9876543210", ln=1)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="email: blsscars@gmail.com", ln=1)

        pdf.ln(5)

        # Customer Details
        pdf.set_font("Times", style="B", size=16)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="Customer Details", ln=1)
        pdf.set_font("Times", size=14)
        pdf.set_x(15)
        pdf.cell(100, 10, txt=f"Customer Name: {customer_name}", ln=1)
        pdf.set_x(15)
        pdf.cell(100, 10, txt=f"Booking Date: {booking_date}", ln=1)
        # Booking Details
        pdf.set_font("Times", size=14)
        pdf.set_x(15)
        pdf.cell(100, 10, txt=f"Booking ID: {booking_id}", ln=1)
        pdf.set_font("Times", style="B", size=16)
        pdf.ln(5)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="Booking Details:", ln=1)

        pdf.ln(5)

        # Table for Car Details
        pdf.set_fill_color(200, 220, 255)
        pdf.set_x(15)
        pdf.set_font("Times", style="B", size=14)
        pdf.cell(60, 10, "Brand", border=1, align="C", fill=True)
        pdf.cell(60, 10, "Model", border=1, align="C", fill=True)
        pdf.cell(60, 10, "Price", border=1, align="C", fill=True)
        pdf.ln()
        pdf.set_x(15)
        pdf.set_font("Times", size=14)
        pdf.cell(60, 10, car_make, border=1, align="C")
        pdf.cell(60, 10, car_model, border=1, align="C")
        pdf.cell(60, 10, price, border=1, align="C")  # Use price as text directly

        pdf.ln(20)

        # Payment Status
        pdf.set_font("Times", style="B", size=14)
        pdf.set_x(15)
        pdf.cell(100, 10, txt="Payment Status: Unpaid", ln=1)

        pdf.ln(10)

        # Footer
        pdf.set_font("Times", style="B", size=16)
        pdf.cell(0, 10, txt="Thanks for visiting............", ln=1, align="C")

        pdf.ln(20)
        pdf.set_font("Times", size=14)
        pdf.cell(0, 10, txt=f"Date: {datetime.today().strftime('%d-%m-%Y')}         ", ln=1, align="R")
        pdf.cell(0, 10, txt="Signature: ______________", ln=1, align="R")


        # Save PDF
        pdf.output(f"{customer_name} Invoice.pdf")
        message=f"Invoice has been generated successfully as {customer_name} Invoice.pdf!"
        messagebox.showinfo("Invoice Generated",message)
    else:
        print("No booking details found.")
