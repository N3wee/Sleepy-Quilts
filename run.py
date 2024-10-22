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

def add_quilt():
    print("Add a new quilt")

    # Collect quilt information from user
    quilt_name = input("Enter quilt name: ")
    quilt_material = input("Enter quilt material: ")
    quilt_fill = input("Enter quilt fill (e.g., down, synthetic, etc.): ")
    quilt_tog = input("Enter quilt tog rating: ")
    quilt_size = input("Enter quilt size: ")
    quilt_price = input("Enter quilt price: ")
    quilt_quantity = input("Enter quilt quantity: ")

    # Prepare the row to insert into Google Sheets
    quilt_data = [quilt_name, quilt_material, quilt_fill, quilt_tog, quilt_size, quilt_price, quilt_quantity]

    try:
        # Try to access the 'quilts' worksheet
        sheet = SHEET.worksheet('quilts')
    except gspread.exceptions.WorksheetNotFound:
        # If worksheet doesn't exist, create it and set headers
        sheet = SHEET.add_worksheet(title='quilts', rows=100, cols=7)
        sheet.append_row(["Name", "Material", "Fill", "Tog", "Size", "Price", "Quantity"])  # Add headers

    # Append the new quilt data
    sheet.append_row(quilt_data)

    print(f"Quilt '{quilt_name}' added successfully!")


# Existing main structure
def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_quilt()  # Now connected to the actual Google Sheets function
        elif choice == '2':
            view_quilts()
        elif choice == '3':
            update_quilt()
        elif choice == '4':
            delete_quilt()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")


main()




