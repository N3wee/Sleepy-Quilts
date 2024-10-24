**Comfy Quilts Inventory Manager**
==================================

Comfy Quilts is a Python terminal-based application that allows users to manage a quilt inventory. Users can add, view, update, and delete quilt entries, with the data being stored and managed through Google Sheets. The application is deployed on Heroku for easy access and testing.

Here is the [live version of my project](#).\
(*Add the Heroku live link here once deployed*)

* * * * *

**How to Use**
--------------

Comfy Quilts is a simple inventory management tool for quilts, designed to run in a terminal interface. Users can interact with the menu options to perform CRUD (Create, Read, Update, Delete) operations on a Google Sheets-based inventory.

### Steps to use:

1.  **Add a Quilt**: Enter quilt details like name, material, fill type, tog rating, size, price, and stock quantity. The new quilt will be saved in the inventory.
2.  **View All Quilts**: Displays all the quilts in the inventory, including details such as name, material, fill type, tog rating, size, price, and quantity.
3.  **Update Quilt Stock**: Select a quilt and modify its stock quantity.
4.  **Delete a Quilt**: Choose a quilt to remove from the inventory entirely.
5.  **Exit**: Terminates the program.

* * * * *

**Features**
------------

### **Existing Features**

-   **Add a Quilt**: Users can add new quilt details, which are then stored in a Google Sheet.
-   **View All Quilts**: Users can view the entire inventory in a tabular format.
-   **Update Quilt Stock**: Allows users to update the stock quantity for an existing quilt.
-   **Delete a Quilt**: Removes a selected quilt from the inventory.
-   **Input Validation**: Ensures that users enter valid data for material, fill type, size, and numerical values (like tog rating, price, and quantity).
-   **Google Sheets Integration**: Data is stored and managed via Google Sheets.

### **Screenshots**

*Insert screenshots of the terminal displaying the app's menu, adding a quilt, and viewing the inventory*

* * * * *

**Future Features**
-------------------

-   **Export Data**: Allow users to export the quilt inventory to a CSV or Excel file.
-   **Detailed Quilt Information**: Add more detailed information fields such as fabric care instructions or quilt origin.
-   **Search Feature**: Implement a search function to filter quilts by size, material, or price.

* * * * *

**Data Model**
--------------

The app stores quilt data in a Google Sheet, with the following fields:

-   **Name**: The name of the quilt.
-   **Material**: The type of fabric (cotton, polycotton, polyester, silk).
-   **Fill**: The filling material (fibre, feather, down).
-   **Tog**: The tog rating of the quilt (a numerical value).
-   **Size**: The size of the quilt (single, double, king, superking).
-   **Price**: The price of the quilt in GBP.
-   **Quantity**: The stock quantity available.

* * * * *

**Bugs**
--------

### **Solved Bugs**

-   **Input Validation**: Initially, invalid inputs for material, fill, and size were not handled properly. Validation checks were added to ensure only valid options are entered.
-   **Stock Update Bug**: Updating the stock for a quilt would sometimes fail due to incorrect indexing. This was resolved by ensuring the proper row number was updated in Google Sheets.

### **Remaining Bugs**

-   There are no known remaining bugs.

* * * * *

**Validator Testing**
---------------------

-   **PEP8**: The code was checked for PEP8 compliance using `pycodestyle`, and no major issues were found.

* * * * *

**Deployment**
--------------

This project was deployed using Code Institute's mock terminal for Heroku.

### **Steps for deployment**:

1.  Fork or clone this repository.
2.  Create a new Heroku app.
3.  Set the buildbacks to `Python` and `NodeJS` in that order.
4.  Link the Heroku app to the repository.
5.  Click on **Deploy**.

* * * * *

**Testing**
-----------

### **Manual Testing**:

-   **Adding a Quilt**: Verified that new quilts can be added successfully with valid inputs.
-   **Viewing Quilts**: Confirmed that all quilts are displayed correctly with headers and data aligned.
-   **Updating Quilt Stock**: Ensured that stock quantities could be updated, and invalid quantities were rejected.
-   **Deleting Quilts**: Verified that selected quilts were deleted from the inventory.
-   **Input Validation**: Tested invalid entries for quilt size, material, fill, and numeric values to ensure that appropriate error messages were displayed.

### **Screenshots**

*Insert screenshots demonstrating successful tests for adding, viewing, updating, and deleting quilts*

* * * * *

**Credits**
-----------

-   **gspread**: Used to interact with Google Sheets API.
-   **Google API**: For managing Google Sheets credentials and access.
-   **tabulate**: For formatting the inventory data in the terminal.
-   **Code Institute**: For providing the project template and guidance.