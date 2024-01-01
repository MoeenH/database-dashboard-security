import subprocess
import os
import re

def run_sqlmap(url,crawl_level):
    # Replace with the path to SQLMap on your system
    sqlmap_path = '/usr/bin/sqlmap'  # Example: '/usr/bin/sqlmap/sqlmap.py'
    crawl_level = '--crawl='+crawl_level
    # Command to run SQLMap with output redirection
    command = [sqlmap_path, '-u', url, '--batch', crawl_level ]

    try:
        # Run SQLMap command using subprocess and capture output
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        return result.stdout

    except subprocess.CalledProcessError as e:
        # Capture and print any errors
        print("Error occurred:", e)
        print("SQLMap output:", e.output)

def save_to_file(output):
    folder_name = 'output'
    file_name = 'sqlmap_output.txt'

    # Create the output directory if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)

    # Write SQLMap output to the file
    with open(file_path, 'w') as file:
        file.write(output)

    print(f"SQLMap output saved to {file_path}")

def print_output_location(output):
    # Extract the file location using regex
    location_pattern = r"find results of scanning.*'(.+\.csv)'"
    match = re.search(location_pattern, output)

    if match:
        file_location = match.group(1)
        print(f"You can find results of scanning in multiple targets mode inside the CSV file: {file_location}")
    else:
        print("No file location found in the SQLMap output.")

if __name__ == "__main__":
    # Take URL input from the user
    main_url = input("Enter the main URL to crawl with SQLMap: ")
    main_crawl_level = input("Enter the Crawl Level: ")
    #main_url = 'http://testphp.vulnweb.com/'
    # Run SQLMap with the provided URL
    target_url = run_sqlmap(main_url,main_crawl_level)

    if target_url:
        save_to_file(target_url)
        print_output_location(target_url)
    else:
        print("No SQLMap output generated.")
