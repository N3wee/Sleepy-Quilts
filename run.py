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
    show_overview()

    raw_materials_ordered_for = None  # Track if raw materials have been ordered and for which date

    while True:
        tomorrow = today + datetime.timedelta(days=1)
        
        # Fetch current stock levels and calculate stock percentage
        cotton_stock, fibre_stock = get_current_stock()
        cotton_percentage = (cotton_stock / MAX_COTTON_STOCK) * 100
        fibre_percentage = (fibre_stock / MAX_FIBRE_STOCK) * 100

        # Determine stock status
        if cotton_stock < MAX_COTTON_STOCK * 0.2 or fibre_stock < MAX_FIBRE_STOCK * 0.2:
            stock_status = f"(Low stock - Cotton: {round(cotton_percentage, 2)}%, Fibre: {round(fibre_percentage, 2)}%)"
        else:
            stock_status = f"(Adequate Stock - Cotton: {round(cotton_percentage, 2)}%, Fibre: {round(fibre_percentage, 2)}%)"

        # Navigation options
        if check_if_orders_exist(tomorrow):
            print("\nWhat would you like to do?")
            print("1. Received tomorrow’s orders. Would you like to rewrite them?")
        else:
            print("\nWhat would you like to do?")
            print("1. Input Orders for Tomorrow")
        
        print("2. View Production Requirements for Tomorrow")
        if raw_materials_ordered_for == tomorrow:
            print(f"3. Order Placed for {tomorrow.strftime('%A, %B %d, %Y')}")
        else:
            print(f"3. Order raw materials {stock_status}")
        print("4. Close the day and move to next day")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            input_orders(tomorrow)  # Input or rewrite orders for tomorrow
        elif choice == "2":
            view_production_schedule(tomorrow)  # View tomorrow's production requirements
        elif choice == "3" and raw_materials_ordered_for != tomorrow:
            if request_raw_materials(tomorrow):  # Pass 'tomorrow' as argument here
                raw_materials_ordered_for = tomorrow  # Mark that order is placed for tomorrow
        elif choice == "4":
            if can_fulfill_tomorrows_orders(tomorrow):  # Check if stock is sufficient for tomorrow's orders
                today = close_day(today)  # Close the day and move to next day
            else:
                print("Insufficient raw materials to fulfill tomorrow's orders. Please order raw materials first.")
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


def can_fulfill_tomorrows_orders(tomorrow):
    """
    Check if there is enough stock to fulfill tomorrow's orders.
    If there isn't enough stock, return False and inform the user.
    """
    orders_tomorrow = get_orders_for_today(tomorrow)
    if not orders_tomorrow:
        return True  # No orders, so stock isn't an issue
    
    cotton_stock, fibre_stock = get_current_stock()

    # Fetch material usage data
    material_usage_sheet = SHEET.worksheet('Material Usage')
    material_usage_data = material_usage_sheet.get_all_values()

    usage_single = {'cotton': float(material_usage_data[1][1]), 'fibre': float(material_usage_data[1][2])}
    usage_double = {'cotton': float(material_usage_data[2][1]), 'fibre': float(material_usage_data[2][2])}
    usage_king = {'cotton': float(material_usage_data[3][1]), 'fibre': float(material_usage_data[3][2])}

    # Calculate materials required for tomorrow's orders
    cotton_needed = (
        orders_tomorrow['single'] * usage_single['cotton'] +
        orders_tomorrow['double'] * usage_double['cotton'] +
        orders_tomorrow['king'] * usage_king['cotton']
    )
    fibre_needed = (
        orders_tomorrow['single'] * usage_single['fibre'] +
        orders_tomorrow['double'] * usage_double['fibre'] +
        orders_tomorrow['king'] * usage_king['fibre']
    )

    # Check if there's enough stock to fulfill tomorrow's orders
    if cotton_stock >= cotton_needed and fibre_stock >= fibre_needed:
        return True
    else:
        print(f"\nInsufficient stock to fulfill tomorrow's orders.")
        print(f"Cotton needed: {round(cotton_needed, 2)} meters, Available: {cotton_stock} meters")
        print(f"Fibre needed: {round(fibre_needed, 2)} kg, Available: {fibre_stock} kg")
        return False


def show_overview():
    """
    Display today's orders and current stock overview.
    """
    print(f"\nOverview:")

    # Fetch today's orders
    today = datetime.date.today()
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


def input_orders(tomorrow):
    """
    Input or rewrite sales orders for the next day.
    """
    try:
        print(f"\nPlease enter orders for {tomorrow.strftime('%A, %B %d, %Y')}:")

        single_orders = int(input("Enter the number of Single duvets ordered: "))
        double_orders = int(input("Enter the number of Double duvets ordered: "))
        king_orders = int(input("Enter the number of King duvets ordered: "))

        # Check if orders already exist for tomorrow
        orders_sheet = SHEET.worksheet('Orders')
        orders_data = orders_sheet.get_all_values()
        row_to_update = None

        for idx, row in enumerate(orders_data):
            if row[0] == tomorrow.strftime('%Y-%m-%d'):
                row_to_update = idx + 1  # Google Sheets uses 1-based index

        # If orders exist, overwrite them
        new_order_data = [tomorrow.strftime('%Y-%m-%d'), single_orders, double_orders, king_orders]
        if row_to_update:
            orders_sheet.update(range_name=f'A{row_to_update}:D{row_to_update}', values=[new_order_data])
            print(f"Orders for {tomorrow.strftime('%A, %B %d, %Y')} successfully overwritten.")
        else:
            orders_sheet.append_row(new_order_data)
            print(f"Orders for {tomorrow.strftime('%A, %B %d, %Y')} successfully recorded.")

    except Exception as e:
        print(f"Error recording orders: {e}")


def check_if_orders_exist(tomorrow):
    """
    Check if orders have already been entered for tomorrow.
    """
    try:
        orders_sheet = SHEET.worksheet('Orders')
        orders_data = orders_sheet.get_all_values()

        for row in orders_data:
            if row[0] == tomorrow.strftime('%Y-%m-%d'):
                return True
        return False
    except Exception as e:
        print(f"Error checking orders: {e}")
        return False


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


def request_raw_materials(tomorrow):
    """
    Order raw materials based on tomorrow's production needs plus a 10% buffer.
    """
    orders_tomorrow = get_orders_for_today(tomorrow)
    if not orders_tomorrow:
        print("No orders for tomorrow, raw materials request not needed.")
        return False

    cotton_stock, fibre_stock = get_current_stock()

    # Fetch material usage data
    material_usage_sheet = SHEET.worksheet('Material Usage')
    material_usage_data = material_usage_sheet.get_all_values()

    usage_single = {'cotton': float(material_usage_data[1][1]), 'fibre': float(material_usage_data[1][2])}
    usage_double = {'cotton': float(material_usage_data[2][1]), 'fibre': float(material_usage_data[2][2])}
    usage_king = {'cotton': float(material_usage_data[3][1]), 'fibre': float(material_usage_data[3][2])}

    # Calculate materials needed for tomorrow's orders + 10% buffer
    cotton_needed = (
        orders_tomorrow['single'] * usage_single['cotton'] +
        orders_tomorrow['double'] * usage_double['cotton'] +
        orders_tomorrow['king'] * usage_king['cotton']
    ) * 1.1
    fibre_needed = (
        orders_tomorrow['single'] * usage_single['fibre'] +
        orders_tomorrow['double'] * usage_double['fibre'] +
        orders_tomorrow['king'] * usage_king['fibre']
    ) * 1.1

    # Calculate how much to order to meet the production needs
    cotton_to_order = max(0, cotton_needed - cotton_stock)
    fibre_to_order = max(0, fibre_needed - fibre_stock)

    # Order raw materials with 1-day lead time
    print(f"\nOrdering raw materials to meet production for {tomorrow.strftime('%A, %B %d, %Y')}:")
    print(f"Cotton to Order: {round(cotton_to_order, 2)} meters")
    print(f"Fibre to Order: {round(fibre_to_order, 2)} kg")

    # Update stock in Google Sheets (simplified for demonstration)
    new_stock_row = [tomorrow.strftime('%Y-%m-%d'), cotton_stock + cotton_to_order, fibre_stock + fibre_to_order]
    stock_sheet = SHEET.worksheet('Material Stock')
    stock_sheet.append_row(new_stock_row)

    print(f"Raw materials will arrive tomorrow.")
    return True  # Indicate materials have been ordered


def view_production_schedule(tomorrow):
    """
    Calculate and display the production requirements for tomorrow based on orders.
    """
    try:
        print(f"\nProduction Schedule for {tomorrow.strftime('%A, %B %d, %Y')}:")

        # Fetch tomorrow's orders
        orders_tomorrow = get_orders_for_today(tomorrow)
        if not orders_tomorrow:
            print(f"No orders for tomorrow yet.")
            return

        # Fetch material usage data
        material_usage_sheet = SHEET.worksheet('Material Usage')
        material_usage_data = material_usage_sheet.get_all_values()

        # Extract material usage per duvet size
        usage_single = {'cotton': float(material_usage_data[1][1]), 'fibre': float(material_usage_data[1][2])}
        usage_double = {'cotton': float(material_usage_data[2][1]), 'fibre': float(material_usage_data[2][2])}
        usage_king = {'cotton': float(material_usage_data[3][1]), 'fibre': float(material_usage_data[3][2])}

        # Calculate raw material requirements
        cotton_required = (
            orders_tomorrow['single'] * usage_single['cotton'] +
            orders_tomorrow['double'] * usage_double['cotton'] +
            orders_tomorrow['king'] * usage_king['cotton']
        )
        fibre_required = (
            orders_tomorrow['single'] * usage_single['fibre'] +
            orders_tomorrow['double'] * usage_double['fibre'] +
            orders_tomorrow['king'] * usage_king['fibre']
        )

        # Display production and material requirements
        print(f"\nDuvets to Produce:")
        print(f"Single Duvets: {orders_tomorrow['single']}")
        print(f"Double Duvets: {orders_tomorrow['double']}")
        print(f"King Duvets: {orders_tomorrow['king']}")

        print(f"\nRaw Materials Needed for Production:")
        print(f"Cotton Required: {round(cotton_required, 2)} meters")
        print(f"Fibre Required: {round(fibre_required, 2)} kg")

    except Exception as e:
        print(f"Error calculating production requirements: {e}")


def close_day(current_day):
    """
    Simulate closing the day and moving to the next day.
    Deduct raw materials used for production from stock.
    After moving to the next day, show the updated overview.
    """
    tomorrow = current_day + datetime.timedelta(days=1)

    print(f"\nClosing the day. Moving to {tomorrow.strftime('%A, %B %d, %Y')}.")

    # Deduct raw materials based on today's production
    orders_today = get_orders_for_today(current_day)
    if orders_today:
        # Fetch material usage data
        material_usage_sheet = SHEET.worksheet('Material Usage')
        material_usage_data = material_usage_sheet.get_all_values()

        usage_single = {'cotton': float(material_usage_data[1][1]), 'fibre': float(material_usage_data[1][2])}
        usage_double = {'cotton': float(material_usage_data[2][1]), 'fibre': float(material_usage_data[2][2])}
        usage_king = {'cotton': float(material_usage_data[3][1]), 'fibre': float(material_usage_data[3][2])}

        # Calculate materials used today
        cotton_used = (
            orders_today['single'] * usage_single['cotton'] +
            orders_today['double'] * usage_double['cotton'] +
            orders_today['king'] * usage_king['cotton']
        )
        fibre_used = (
            orders_today['single'] * usage_single['fibre'] +
            orders_today['double'] * usage_double['fibre'] +
            orders_today['king'] * usage_king['fibre']
        )

        # Fetch current stock and update the sheet
        cotton_stock, fibre_stock = get_current_stock()
        updated_cotton_stock = max(0, cotton_stock - cotton_used)
        updated_fibre_stock = max(0, fibre_stock - fibre_used)

        # Update stock in Google Sheets
        new_stock_row = [tomorrow.strftime('%Y-%m-%d'), updated_cotton_stock, updated_fibre_stock]
        stock_sheet = SHEET.worksheet('Material Stock')
        stock_sheet.append_row(new_stock_row)

        print(f"\nRaw materials deducted. Updated stock for {tomorrow.strftime('%A, %B %d, %Y')} recorded.")
    else:
        print("\nNo orders to produce today, stock remains unchanged.")

    # Show the updated overview for the new day
    show_overview()

    return tomorrow


main()

