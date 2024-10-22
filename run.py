import gspread
from google.oauth2.service_account import Credentials
import datetime

# Authentication and setup for Google Sheets API
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
    """
    Display the main menu options for the quilt inventory manager.
    """
    print("Welcome to Comfy Quilts Inventory Manager")
    print("Please choose an option:")
    print("1. Add a new quilt")
    print("2. View all quilts")
    print("3. Update quilt stock")
    print("4. Delete a quilt")
    print("5. Exit")

# Helper function for material validation
def get_valid_material():
    """
    Validate the material input from the user.
    Returns:
        material (str): A valid material (cotton, polycotton, polyester, silk).
    """
    valid_materials = ['cotton', 'polycotton', 'polyester', 'silk']
    while True:
        material = input("Enter quilt material (cotton, polycotton, polyester, silk): ").lower()
        if material in valid_materials:
            return material
        else:
            print("Invalid material. Please enter a valid option.")

# Helper function for fill validation
def get_valid_fill():
    """
    Validate the fill input from the user.
    Returns:
        fill (str): A valid fill (fibre, feather, down).
    """
    valid_fills = ['fibre', 'feather', 'down']
    while True:
        fill = input("Enter quilt fill (fibre, feather, down): ").lower()
        if fill in valid_fills:
            return fill
        else:
            print("Invalid fill. Please enter a valid option.")

# Helper function for size validation
def get_valid_size():
    """
    Validate the size input from the user.
    Returns:
        size (str): A valid size (single, double, king, superking).
    """
    valid_sizes = ['single', 'double', 'king', 'superking']
    while True:
        size = input("Enter quilt size (single, double, king, superking): ").lower()
        if size in valid_sizes:
            return size
        else:
            print("Invalid size. Please enter a valid option.")

# Helper function for valid number input
def get_valid_number(prompt):
    """
    Ensure the user inputs a valid number for price, tog rating, or stock quantity.
    
    Args:
        prompt (str): The prompt message to show the user.
    
    Returns:
        value (float): A valid numeric input from the user.
    """
    while True:
        try:
            value = float(input(prompt))  # Accept float to cover decimal numbers if needed
            return value
        except ValueError:
            print("Please enter a valid number.")

def add_quilt():
    """
    Collects quilt data from the user, validates input, and adds the quilt to the Google Sheet.
    """
    print("Add a new quilt")
    
    quilt_name = input("Enter quilt name: ")
    quilt_material = get_valid_material()
    quilt_fill = get_valid_fill()
    quilt_tog = get_valid_number("Enter quilt tog rating (as a number): ")  # Validate tog rating
    quilt_size = get_valid_size()
    quilt_price = get_valid_number("Enter quilt price in GBP: ")  # Validate price
    quilt_quantity = get_valid_number("Enter quilt quantity: ")  # Validate quantity

    quilt_data = [quilt_name, quilt_material, quilt_fill, quilt_tog, quilt_size, quilt_price, quilt_quantity]

    try:
        sheet = SHEET.worksheet('quilts')
    except gspread.exceptions.WorksheetNotFound:
        sheet = SHEET.add_worksheet(title='quilts', rows=100, cols=7)
        sheet.append_row(["Name", "Material", "Fill", "Tog", "Size", "Price", "Quantity"])  # Add headers

    sheet.append_row(quilt_data)
    print(f"Quilt '{quilt_name}' added successfully!")

def view_quilts():
    """
    Retrieves and displays all quilt entries from the Google Sheet.
    """
    print("View all quilts")

    try:
        sheet = SHEET.worksheet('quilts')
        quilts = sheet.get_all_values()

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
    """
    Allows the user to update the stock quantity of a selected quilt in the Google Sheet.
    """
    print("Update quilt stock")

    try:
        sheet = SHEET.worksheet('quilts')
        quilts = sheet.get_all_values()

        if len(quilts) > 1:
            print("\nQuilt Inventory:")
            for index, row in enumerate(quilts[1:], start=1):
                print(f"{index}. Name: {row[0]}, Quantity: {row[6]}")
            
            quilt_num = int(get_valid_number("\nEnter the number of the quilt you want to update: "))

            if 1 <= quilt_num <= len(quilts) - 1:
                selected_quilt = quilts[quilt_num]
                print(f"Selected Quilt: {selected_quilt[0]}")
                new_quantity = get_valid_number(f"Enter the new quantity for '{selected_quilt[0]}': ")
                sheet.update_cell(quilt_num + 1, 7, new_quantity)
                print(f"Updated '{selected_quilt[0]}' stock to {new_quantity}.")
            else:
                print("Invalid quilt number.")
        else:
            print("No quilts found in inventory.")
    except gspread.exceptions.WorksheetNotFound:
        print("Worksheet 'quilts' not found.")

def delete_quilt():
    """
    Allows the user to delete a selected quilt from the Google Sheet.
    """
    print("Delete a quilt")

    try:
        sheet = SHEET.worksheet('quilts')
        quilts = sheet.get_all_values()

        if len(quilts) > 1:
            print("\nQuilt Inventory:")
            for index, row in enumerate(quilts[1:], start=1):  # Skip the header row
                print(f"{index}. Name: {row[0]}")
            
            quilt_num = int(input("\nEnter the number of the quilt you want to delete: "))
            if 1 <= quilt_num <= len(quilts) - 1:
                selected_quilt = quilts[quilt_num]
                print(f"Selected Quilt: {selected_quilt[0]}")

                confirm = input(f"Are you sure you want to delete '{selected_quilt[0]}'? (y/n): ")
                if confirm.lower() == 'y':
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
    """
    Main function that handles the menu system and calls the appropriate functions based on user input.
    """
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_quilt()
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





