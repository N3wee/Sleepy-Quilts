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
    Displays a welcome message, today's date, and navigation options.
    """
    today = datetime.date.today()
    print(f"Welcome to Sleepy Quilts Production System - {today.strftime('%A, %B %d, %Y')}")
    
    # Show basic overview and navigation
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