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

input_stock_data()