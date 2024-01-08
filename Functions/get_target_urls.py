import subprocess
import os
import re

def run_sqlmap(url, crawl_level):

    sqlmap_path = '/usr/bin/sqlmap'  
    crawl_level = '--crawl=' + crawl_level
    command = [sqlmap_path, '-u', url, '--batch', crawl_level]

    try:
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_lines = result.stdout.split('\n')
        relevant_output = []  # Store relevant output lines

        # Look for specific lines in the output
        for line in output_lines:
            
            if 'SQL injection vulnerability has already been detected' in line or 'you can find results of scanning' in line:
                relevant_output.append(line)

        return '\n'.join(relevant_output)  

    except subprocess.CalledProcessError as e:
        
        print("Error occurred:", e)
        print("SQLMap output:", e.output)


def save_to_file(output):
    folder_name = 'output'
    file_name = 'target_url.txt'

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)

   
    with open(file_path, 'w') as file:
        file.write(output)

    print(f"SQLMap output saved to {file_path}")


def print_output_location(output):
    
    location_pattern = r"find results of scanning.*'(.+\.csv)'"
    match = re.search(location_pattern, output)

    if match:
        file_location = match.group(1)
        print(f"You can find results of scanning in multiple targets mode inside the CSV file: {file_location}")
    else:
        print("No file location found in the SQLMap output.")


if __name__ == "__main__":
    main_url = input("Enter the main url that you want to traverse")
    main_crawl_level = input("Enter the Crawl Level: ")
    #main_url = 'http://testphp.vulnweb.com/'

    
    target_url = run_sqlmap(main_url, main_crawl_level)

    if target_url:
        save_to_file(target_url)
        print_output_location(target_url)
    else:
        print("No SQLMap output generated.")
