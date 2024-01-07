import tkinter as tk
from main import run_sqlmap

root = tk.Tk()

def run_sequel():
    url = mainContainer.get()
    crawl = crawl_var.get()
    result = run_sqlmap(url, crawl)
    # result_label.config(text=f"Result: {result}")

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

# Dropdown for crawl
crawlFrame = tk.Frame(root)
crawlFrame.columnconfigure(0, weight=1)
crawlFrame.columnconfigure(1, weight=1)

crawlText = tk.Label(crawlFrame, text="Crawl:", font=('Helvetica', 14))
crawlText.grid(row=0, column=0)

crawl_var = tk.StringVar()
crawl_var.set("2")  # Default value
crawlDropdown = tk.OptionMenu(crawlFrame, crawl_var, "1", "2", "3")
crawlDropdown.grid(row=0, column=1)

crawlFrame.pack(fill='x')

button = tk.Button(root, text="Run scan", font=('Helvetica', 14), command=run_sequel)
button.pack(pady=20, padx=20)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()