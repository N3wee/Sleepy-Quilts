# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('SleepyQuilts')

def fetch_sales_data():
    """
    Fetch sales data from the 'Sales' sheet.
    Returns a tuple of sales data and the next available week number.
    """
    try:
        sales_sheet = SHEET.worksheet('Sales')
        sales_data = sales_sheet.get_all_values()

        if len(sales_data) > 1:  # Ensure there's data beyond the header
            # Get the last week's number from the last row's first column
            last_week = int(sales_data[-1][0])
            current_week = last_week + 1
        else:
            # If no previous data or just the header, set current week as 1
            current_week = 1

        print("Sales data successfully fetched!")
        return sales_data, current_week
    except Exception as e:
        print(f"Error fetching sales data: {e}")
        return None, None


def input_sales_data():
    """
    Get user input for sales data and append it to the 'Sales' sheet along with the week number.
    """
    try:
        # Fetch sales data to determine the week number
        sales_data, current_week = fetch_sales_data()

        # Inform the user of the current week they are entering data for
        print(f"Please enter sales figures for Week {current_week}:")
        single_sales = int(input("Enter the number of Single duvets sold: "))
        double_sales = int(input("Enter the number of Double duvets sold: "))
        king_sales = int(input("Enter the number of King duvets sold: "))

        # Include the week number in the data to be appended
        new_sales_data = [current_week, single_sales, double_sales, king_sales]

        # Append the sales data with the week number to the sheet
        sales_sheet = SHEET.worksheet('Sales')
        sales_sheet.append_row(new_sales_data)
        print(f"Sales data for Week {current_week} successfully added to the sheet!")
    except Exception as e:
        print(f"Error appending sales data: {e}")


def fetch_stock_data():
    """
    Fetch stock data from the 'Raw Stock' sheet.
    Returns a tuple of stock data and the next available week number.
    """
    try:
        stock_sheet = SHEET.worksheet('Raw Stock')
        stock_data = stock_sheet.get_all_values()

        if len(stock_data) > 1:  # Ensure there's data beyond the header
            last_week = int(stock_data[-1][0])
            current_week = last_week + 1
        else:
            current_week = 1

        print("Stock data successfully fetched!")
        return stock_data, current_week
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return None, None


def input_stock_data():
    """
    Get user input for stock data (Cotton and Fibre) and append it to the 'Raw Stock' sheet.
    """
    try:
        # Fetch stock data to determine the week number
        stock_data, current_week = fetch_stock_data()

        # Inform the user of the current week they are entering data for
        print(f"Please enter stock figures for Week {current_week}:")
        cotton_stock = float(input("Enter the current stock of Cotton (in meters): "))
        fibre_stock = float(input("Enter the current stock of Fibre (in kilograms): "))

        # Validate that stock levels are non-negative
        if cotton_stock < 0 or fibre_stock < 0:
            print("Stock levels must be non-negative. Please try again.")
            return

        # Include the week number in the data to be appended
        new_stock_data = [current_week, cotton_stock, fibre_stock]

        # Append the stock data with the week number to the sheet
        stock_sheet = SHEET.worksheet('Raw Stock')
        stock_sheet.append_row(new_stock_data)
        print(f"Stock data for Week {current_week} successfully added to the sheet!")
    except ValueError:
        print("Invalid input. Please enter numeric values for stock levels.")
    except Exception as e:
        print(f"Error appending stock data: {e}")   

stock_data = fetch_stock_data()

def fetch_duvet_stock():
    """
    Fetch duvet stock data from the 'Duvet Stock' sheet.
    Returns the current stock levels for Single, Double, and King duvets.
    """
    try:
        duvet_stock_sheet = SHEET.worksheet('Duvet Stock')
        duvet_stock_data = duvet_stock_sheet.get_all_values()

        # Get the last recorded stock (most recent row)
        if len(duvet_stock_data) > 1:
            last_stock = duvet_stock_data[-1]
            current_stock_single = int(last_stock[1])  # Single duvet stock
            current_stock_double = int(last_stock[2])  # Double duvet stock
            current_stock_king = int(last_stock[3])    # King duvet stock
        else:
            # If no stock data is present, assume stock is zero
            current_stock_single = 0
            current_stock_double = 0
            current_stock_king = 0

        print("Duvet stock successfully fetched!")
        return current_stock_single, current_stock_double, current_stock_king
    except Exception as e:
        print(f"Error fetching duvet stock: {e}")
        return None, None, None


def update_duvet_stock():
    """
    Update the 'Duvet Stock' sheet by subtracting the current week's sales
    from the current duvet stock levels.
    """
    try:
        # Fetch the current week's sales data
        sales_data, current_week = fetch_sales_data()
        current_week_sales = sales_data[-1]  # Get the most recent sales data

        # Fetch the current duvet stock levels
        current_stock_single, current_stock_double, current_stock_king = fetch_duvet_stock()

        # Subtract sales figures from stock levels
        new_stock_single = max(0, current_stock_single - int(current_week_sales[1]))  # Single duvet stock
        new_stock_double = max(0, current_stock_double - int(current_week_sales[2]))  # Double duvet stock
        new_stock_king = max(0, current_stock_king - int(current_week_sales[3]))  # King duvet stock

        # Prepare new duvet stock data with the current week
        new_duvet_stock_data = [current_week, new_stock_single, new_stock_double, new_stock_king]

        # Append the updated stock levels to the Duvet Stock sheet
        duvet_stock_sheet = SHEET.worksheet('Duvet Stock')
        duvet_stock_sheet.append_row(new_duvet_stock_data)
        print(f"Duvet stock for Week {current_week} successfully updated!")
    except Exception as e:
        print(f"Error updating duvet stock: {e}")

def calculate_production():
    """
    Calculate the production requirements for the current week based on the last 4 weeks
    of sales data and updated duvet stock levels, including a 10% reserve.
    """
    try:
        # Fetch sales data
        sales_data, current_week = fetch_sales_data()

        # Fetch the updated duvet stock levels (after updating stock)
        current_stock_single, current_stock_double, current_stock_king = fetch_duvet_stock()

        # Ensure there are at least 4 weeks of data
        if len(sales_data) < 5:  # Account for possible header row
            print("Not enough data to calculate the production requirements (requires 4 weeks).")
            return

        # Get sales data for the last 4 weeks
        last_4_weeks = sales_data[-4:]  # Last 4 rows excluding the header

        # Initialize totals for Single, Double, King
        total_single = 0
        total_double = 0
        total_king = 0

        # Sum up sales for the last 4 weeks
        for week in last_4_weeks:
            total_single += int(week[1])  # Single duvet sales
            total_double += int(week[2])  # Double duvet sales
            total_king += int(week[3])    # King duvet sales

        # Calculate the average sales per duvet type over the last 4 weeks
        avg_single = total_single / 4
        avg_double = total_double / 4
        avg_king = total_king / 4

        # Add 10% reserve to the production requirements
        production_single = round(avg_single * 1.1)
        production_double = round(avg_double * 1.1)
        production_king = round(avg_king * 1.1)

        # Adjust production based on updated duvet stock
        adjusted_single = max(0, production_single - current_stock_single)
        adjusted_double = max(0, production_double - current_stock_double)
        adjusted_king = max(0, production_king - current_stock_king)

        # Output the production requirements
        print(f"Production requirements for Week {current_week}:")
        print(f"Single Duvets: {adjusted_single}")
        print(f"Double Duvets: {adjusted_double}")
        print(f"King Duvets: {adjusted_king}")

        return adjusted_single, adjusted_double, adjusted_king

    except Exception as e:
        print(f"Error calculating production requirements: {e}")
