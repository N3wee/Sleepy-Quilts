# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('SleepyQuilts')

def main():
    """
    Main function to handle user navigation and display overview.
    Displays a welcome message, today's date, orders to produce today, and current stock.
    """
    today = datetime.date.today()
    print(f"Welcome to Sleepy Quilts Production System - {today.strftime('%A, %B %d, %Y')}")

    # Show overview
    show_overview(today)

    # Show basic navigation and options
    while True:
        print("\nWhat would you like to do?")
        print("1. Input Orders for Tomorrow")
        print("2. View Production Requirements for Tomorrow")
        print("3. Exit")

        choice = input("Enter your choice: ")
        
        if choice == "1":
            input_orders()  # Placeholder for input orders
        elif choice == "2":
            view_production_schedule()  # Placeholder for viewing production schedule
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

def show_overview(today):
    """
    Display today's orders and current stock overview.
    """
    print(f"\nOverview for {today.strftime('%A, %B %d, %Y')} (Today)")
    
    # Fetch today's orders
    orders_today = get_orders_for_today(today)
    if orders_today:
        print(f"\nOrders to Produce Today:")
        print(f"Single Duvets: {orders_today['single']}")
        print(f"Double Duvets: {orders_today['double']}")
        print(f"King Duvets: {orders_today['king']}")
    else:
        print("\nNo orders to produce today.")
    
    # Fetch current stock levels
    cotton_stock, fibre_stock = get_current_stock()
    print(f"\nCurrent Stock Levels:")
    print(f"Cotton: {cotton_stock} meters")
    print(f"Fibre: {fibre_stock} kg")

def get_orders_for_today(today):
    """
    Fetch today's orders from the Orders Sheet (Placeholder function).
    """
    # Placeholder logic to simulate fetching orders from the Orders sheet
    # Replace this with the actual Google Sheets fetching logic later
    return {'single': 50, 'double': 30, 'king': 20}  # Dummy data

def get_current_stock():
    """
    Fetch current stock levels from the Material Stock Sheet (Placeholder function).
    """
    # Placeholder logic to simulate fetching stock from the Material Stock sheet
    # Replace this with the actual Google Sheets fetching logic later
    return 1000, 500  # Dummy data (1000 meters of cotton, 500 kg of fibre)

def input_orders():
    """
    Placeholder function for inputting orders.
    """
    print("Inputting orders... (functionality to be implemented)")

def view_production_schedule():
    """
    Placeholder function for viewing production schedule.
    """
    print("Viewing production schedule... (functionality to be implemented)")

main()