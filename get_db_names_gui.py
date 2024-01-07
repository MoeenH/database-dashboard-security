import tkinter as tk
from get_db_names import sqlmap_dbs
import re

root = tk.Tk()

def extract_database_names(output_text):
  """Extracts the database names listed under "Available databases" from the SQLMap output text and returns a list of those names.

  Args:
    output_text: The string containing the SQLMap output.

  Returns:
    A list of the extracted database names, or an empty list if none are found.
  """

  pattern = r"Available databases \[(\d+)\]:\s*\n((?:[*] \w+\n)+)"
  match = re.search(pattern, output_text, flags=re.DOTALL)
  if match:
    database_names = match.group(2).strip().split("\n")
    database_names = [name.strip("* ") for name in database_names]
    return database_names
  else:
    return []


def run_sequel():
    url = mainContainer.get()
    result = sqlmap_dbs(url)
    rslt = extract_database_names(result)
    result_label.config(text=f"Result: {rslt}")

root.geometry("800x800")
root.title("Database Dashboard Security")

label = tk.Label(root, text="Database Dashboard Security", font=('Helvetica', 20))
label.pack(pady=20)

urlFrame = tk.Frame(root)
urlFrame.columnconfigure(0, weight=1)
urlFrame.columnconfigure(1, weight=1)

urlText = tk.Label(urlFrame, text="Enter URL:", font=('Helvetica', 14))
urlText.grid(row=0, column=0)

mainContainer = tk.Entry(urlFrame, font=('Helvetica', 14))
mainContainer.grid(row=0, column=1)

urlFrame.pack(fill='x')

button = tk.Button(root, text="Get DB Names", font=('Helvetica', 14), command=run_sequel)
button.pack(pady=20, padx=20)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
