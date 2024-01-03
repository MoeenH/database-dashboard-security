import subprocess

def run_sqlmap(url):
    # Replace with the path to SQLMap on your system
    sqlmap_path = '/usr/bin/sqlmap'  # Example: '/usr/bin/sqlmap/sqlmap.py'

    # Command to run SQLMap with default options
    command = [sqlmap_path, '-u', url, '--batch', '--risk=', '--level=5']

    try:
        # Run SQLMap command using subprocess
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Print SQLMap output
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Capture and print any errors
        print("Error occurred:", e)
        print("SQLMap output:", e.output)

if __name__ == "__main__":
    # Take URL input from the user
    url = input("Enter the URL to test with SQLMap: ")

    # Run SQLMap with the provided URL
    run_sqlmap(url)
