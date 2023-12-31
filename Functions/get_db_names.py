import subprocess

def sqlmap_dbs(url, output_file_path):
    
    sqlmap_path = '/usr/bin/sqlmap'  

    command = [sqlmap_path, '-u', url, '--batch', '--dbs']

    try:
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_lines = result.stdout.splitlines()
        filtered_lines = [line for line in output_lines if "available databases" in line.lower()]

        if not filtered_lines:
            print("No databases found.")
            return []
        start_index = output_lines.index(filtered_lines[0])

        
        database_names = [line.strip(' *') for line in output_lines[start_index + 1:]]

        with open(output_file_path, 'w') as output_file:
            for db_name in database_names:
                output_file.write(db_name + '\n')

        
        print("Available Databases:")
        for db_name in database_names:
            print(db_name)

        return database_names
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running SQLMap: {e}")

    # try:
    #     # Run the SQLMap command
    #     result = subprocess.run(command, capture_output=True, text=True, check=True)

    #     # Extract the database names from the SQLMap output
    #     output_lines = result.stdout.splitlines()

    #     # Filter out unwanted lines
    #     filtered_lines = [line for line in output_lines if "available databases" in line.lower()]

    #     if not filtered_lines:
    #         print("No databases found.")
    #         return []

    #     # Find the line containing "available databases"
    #     start_index = output_lines.index(filtered_lines[0])

    #     # Extract database names from the subsequent lines
    #     database_names = [line.strip(' *') for line in output_lines[start_index + 1:]]

    #     # Write the database names to the specified output file
    #     with open(output_file_path, 'w') as output_file:
    #         for db_name in database_names:
    #             output_file.write(db_name + '\n')

    #     # Print the desired part
    #     print("Available Databases:")
    #     for db_name in database_names:
    #         print(db_name)

    #     return database_names
    # except subprocess.CalledProcessError as e:
    #     raise Exception(f"Error running SQLMap: {e}")

if __name__ == "__main__":
    target_url = input("Enter the URL you found after crawl:")
    output_file_path = "database_names.txt"  
    try:
        database_names = sqlmap_dbs(target_url, output_file_path)

        if not database_names:
            print("No databases found.")
    except Exception as e:
        print(f"Error: {e}")
