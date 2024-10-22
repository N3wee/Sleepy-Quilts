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

def view_quilts():
    print("View all quilts")

    try:
        # Try to access the 'quilts' worksheet
        sheet = SHEET.worksheet('quilts')
        quilts = sheet.get_all_values()

        # Check if there is data beyond the headers
        if len(quilts) > 1:
            print("\nQuilt Inventory:")
            for row in quilts[1:]:  # Skip the header row
                print(f"Name: {row[0]}, Material: {row[1]}, Fill: {row[2]}, Tog: {row[3]}, "
                      f"Size: {row[4]}, Price: {row[5]}, Quantity: {row[6]}")
        else:
            print("No quilts found in inventory.")
    except gspread.exceptions.WorksheetNotFound:
        print("Worksheet 'quilts' not found.")


def update_quilt():
    print("Update quilt stock")

    try:
        # Try to access the 'quilts' worksheet
        sheet = SHEET.worksheet('quilts')
        quilts = sheet.get_all_values()

        # Check if there is any quilt data
        if len(quilts) > 1:
            # Display all quilts for the user to choose which one to update
            print("\nQuilt Inventory:")
            for index, row in enumerate(quilts[1:], start=1):  # Skip the header row
                print(f"{index}. Name: {row[0]}, Quantity: {row[6]}")
            
            # Prompt user to select a quilt by its number
            quilt_num = int(input("\nEnter the number of the quilt you want to update: "))
            if 1 <= quilt_num <= len(quilts) - 1:
                # Get the current quilt details
                selected_quilt = quilts[quilt_num]
                print(f"Selected Quilt: {selected_quilt[0]}")
                new_quantity = input(f"Enter the new quantity for '{selected_quilt[0]}': ")

                # Update the quantity in the sheet
                sheet.update_cell(quilt_num + 1, 7, new_quantity)  # quilt_num + 1 to account for header row
                print(f"Updated '{selected_quilt[0]}' stock to {new_quantity}.")
            else:
                print("Invalid quilt number.")
        else:
            print("No quilts found in inventory.")
    except gspread.exceptions.WorksheetNotFound:
        print("Worksheet 'quilts' not found.")


def delete_quilt():
    print("Delete a quilt")

    try:
        # Try to access the 'quilts' worksheet
        sheet = SHEET.worksheet('quilts')
        quilts = sheet.get_all_values()

        # Check if there is any quilt data
        if len(quilts) > 1:
            # Display all quilts for the user to choose which one to delete
            print("\nQuilt Inventory:")
            for index, row in enumerate(quilts[1:], start=1):  # Skip the header row
                print(f"{index}. Name: {row[0]}")
            
            # Prompt user to select a quilt by its number
            quilt_num = int(input("\nEnter the number of the quilt you want to delete: "))
            if 1 <= quilt_num <= len(quilts) - 1:
                # Get the current quilt details
                selected_quilt = quilts[quilt_num]
                print(f"Selected Quilt: {selected_quilt[0]}")

                # Confirm deletion
                confirm = input(f"Are you sure you want to delete '{selected_quilt[0]}'? (y/n): ")
                if confirm.lower() == 'y':
                    # Delete the row (quilt_num + 1 to account for header row)
                    sheet.delete_rows(quilt_num + 1)
                    print(f"Deleted '{selected_quilt[0]}' successfully.")
                else:
                    print("Delete operation canceled.")
            else:
                print("Invalid quilt number.")
        else:
            print("No quilts found in inventory.")
    except gspread.exceptions.WorksheetNotFound:
        print("Worksheet 'quilts' not found.")



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




