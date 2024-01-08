import subprocess

class ScanOption:
    def __init__(self):
        self.scan_options = {
            "Banner Information": ["--banner"],
            "Identify Database Management System (DBMS)": ["--dbms", "MySQL"],
            "Enumerate Databases": ["--dbs"],
            "Enumerate Users": ["--users"],
            "Retrieve Current Database": ["--current-db"],
            "Enumerate Tables": ["--tables", "-D"],
            "Enumerate Columns": ["--columns", "-D", "-T"],
            "Dump Table Data": ["--dump", "-D", "-T"],
            # Add more options as needed...
        }

def run_sqlmap(url, args):
    try:
        command = ["sqlmap", "-u", url] + args
        
        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)
        
        return result.stdout  # Returning the output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"  # Returning an error message if any

def main():
    
    options = ScanOption()

    print("\nAvailable SQLMap Scans:")
    for idx, option in enumerate(options.scan_options.keys(), start=1):
        print(f"{idx}. {option}")
    
    try:
        choice = int(input("\nEnter the number corresponding to the scan option: "))
        selected_scan = list(options.scan_options.keys())[choice - 1]
        
        if selected_scan in options.scan_options:
            arguments = options.scan_options[selected_scan]
           
            url = input("Enter URL: ")
            if "-D" in arguments:
                database_name = input("Enter database name: ")
                arguments[arguments.index("-D") + 1] = database_name
            
            if "-T" in arguments:
                table_name = input("Enter table name: ")
                arguments[arguments.index("-T") + 1] = table_name
           
            if "--dbms" in arguments:
                dbms_type = input("Enter DBMS type name, e.g., MySQL, PostgreSQL: ")
                arguments[arguments.index("--dbms") + 1] = dbms_type
            
            output = run_sqlmap(url, arguments)

            print(f"\n{selected_scan}:")
            print(output)
        else:
            print("Invalid choice!")
    except (ValueError, IndexError):
        print("Invalid input! Please enter a valid number.")

if __name__ == "__main__":
    main()
