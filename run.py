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


def display_menu():
    print("Welcome to Comfy Quilts Inventory Manager")
    print("Please choose an option:")
    print("1. Add a new quilt")
    print("2. View all quilts")
    print("3. Update quilt stock")
    print("4. Delete a quilt")
    print("5. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            print("You chose to add a new quilt.")
        elif choice == '2':
            print("You chose to view all quilts.")
        elif choice == '3':
            print("You chose to update quilt stock.")
        elif choice == '4':
            print("You chose to delete a quilt.")
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

    main()




