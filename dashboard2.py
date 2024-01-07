import tkinter as tk

def perform_action():
    url = url_entry.get()
    database_name = db_entry.get()
    # Call your function with the obtained inputs
    your_function(url, database_name)

def your_function(url, database_name):
    # Your function logic here
    print(f"URL: {url}")
    print(f"Database Name: {database_name}")

root = tk.Tk()

url_label = tk.Label(root, text="Enter URL:")
url_label.pack()

url_entry = tk.Entry(root)
url_entry.pack()

db_label = tk.Label(root, text="Enter Database Name:")
db_label.pack()

db_entry = tk.Entry(root)
db_entry.pack()

execute_button = tk.Button(root, text="Run Function", command=perform_action)
execute_button.pack()

root.mainloop()
