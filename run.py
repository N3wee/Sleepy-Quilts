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


# Run the input sales function
input_sales_data()        