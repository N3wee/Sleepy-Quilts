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

# Define the maximum stock levels
MAX_COTTON_STOCK = 3000  # Max cotton in meters
MAX_FIBRE_STOCK = 1000   # Max fibre in kg

def main():
    """
    Main function to handle user navigation and display overview.
    Displays a welcome message, today's date, orders to produce today, and current stock.
    """
    today = datetime.date.today()
    print(f"Welcome to Sleepy Quilts Production System")
    print(f"\nDate: {today.strftime('%A, %B %d, %Y')}")

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
    print(f"Cotton: {cotton_stock} / {MAX_COTTON_STOCK} meters")
    print(f"Fibre: {fibre_stock} / {MAX_FIBRE_STOCK} kg")

def get_orders_for_today(today):
    """
    Fetch today's orders from the Orders Sheet.
    """
    try:
        orders_sheet = SHEET.worksheet('Orders')
        orders_data = orders_sheet.get_all_values()
        
        # Iterate through rows and find today's orders
        for row in orders_data:
            if row[0] == today.strftime('%Y-%m-%d'):
                return {
                    'single': int(row[1]),
                    'double': int(row[2]),
                    'king': int(row[3])
                }
        return None  # No orders for today
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return None

def get_current_stock():
    """
    Fetch current stock levels from the Material Stock Sheet.
    """
    try:
        stock_sheet = SHEET.worksheet('Material Stock')
        stock_data = stock_sheet.get_all_values()

        # Get the last row (most recent stock values)
        last_stock = stock_data[-1]
        cotton_stock = float(last_stock[1])
        fibre_stock = float(last_stock[2])

        return cotton_stock, fibre_stock
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return 0, 0  # Return 0 if there's an error

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