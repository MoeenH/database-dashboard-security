import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from main import m_run_sqlmap
from get_db_tableinfo import sqlmap_functionality
import subprocess
import shutil
import os
import re

class FirstTab:
    def __init__(self, master):
        self.master = master

        # UI Elements
        self.label = tk.Label(master, text="Database Dashboard Security", font=('Helvetica', 20))
        self.label.pack(pady=20)

        self.url_frame = tk.Frame(master)
        self.url_frame.columnconfigure(0, weight=1)
        self.url_frame.columnconfigure(1, weight=1)

        self.url_text = tk.Label(self.url_frame, text="Enter URL:", font=('Helvetica', 14))
        self.url_text.grid(row=0, column=0)

        self.main_container = tk.Entry(self.url_frame, font=('Helvetica', 14))
        self.main_container.grid(row=0, column=1)

        self.crawl_text = tk.Label(self.url_frame, text="Enter Crawl Level:", font=('Helvetica', 14))
        self.crawl_text.grid(row=1, column=0)

        self.crawl_level = tk.Entry(self.url_frame, font=('Helvetica', 14))
        self.crawl_level.grid(row=1, column=1)

        self.url_frame.pack(fill='x')

        self.button = tk.Button(master, text="Run scan", font=('Helvetica', 14), command=self.run_sequel)
        self.button.pack(pady=20, padx=20)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack()

    def run_sequel(self):
        try:
            url = self.main_container.get()
            crawl_level = self.crawl_level.get()
            output_lines = m_run_sqlmap(url, crawl_level)

            # Display the output in the Tkinter window
            self.result_text.delete(1.0, tk.END)  # Clear previous output
            for line in output_lines:
                self.result_text.insert(tk.END, line)
        except Exception as e:
            self.result_text.delete(1.0, tk.END)  # Clear previous output
            self.result_text.insert(tk.END, f"Error: {e}")

    # def run_sqlmap(self, url, crawl_level):
    #     try:
    #         clean_database_name = "information_schema"  # Replace this with the desired database name
    #         command = ["sqlmap", '-u', url, '-D', clean_database_name, '--tables', '--level', '3', '--risk', '3']

    #         result = subprocess.run(command, capture_output=True, text=True, check=True, input="")
    #         table_names_match = re.search(rf'Database: {re.escape(clean_database_name)}\s*\n\[\d+ tables\](.+?)\n\n', result.stdout, re.DOTALL)

    #         if table_names_match:
    #             table_names_section = table_names_match.group(1)
    #             table_names = re.findall(r'\|\s+(\w+)\s+\|', table_names_section)

    #             output_lines = [f"Tables for database '{clean_database_name}':"]
    #             for index, table_name in enumerate(sorted(table_names), start=1):
    #                 output_lines.append(f"{index}. {table_name}")

    #             output_lines.append(f"Output written to 'output.txt'")

    #             with open("output.txt", 'w') as output_file:
    #                 for line in output_lines:
    #                     output_file.write(line + '\n')

    #             return output_lines
    #         else:
    #             return [f"No tables found for database '{clean_database_name}'."]
    #     except subprocess.CalledProcessError as e:
    #         raise Exception(f"Error running SQLMap: {e}")


class SecondTab:
    def __init__(self, master):
        self.master = master
        # self.master.title("SQLMap GUI")  # Comment this line

        # UI Elements
        self.url_label = tk.Label(master, text="Enter URL:")
        self.url_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.insert(0, "http://testphp.vulnweb.com/listproducts.php?cat=1")
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

        self.db_label = tk.Label(master, text="Enter Database Name:")
        self.db_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.db_entry = ttk.Entry(master, width=30)
        self.db_entry.insert(0, "database_name")  # Initial value, change as needed
        self.db_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        self.execute_button = tk.Button(master, text="Run SQLMap", command=self.run_sqlmap)
        self.execute_button.grid(row=2, column=0, columnspan=3, pady=10)

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def run_sqlmap(self):
        try:
            url = self.url_entry.get()
            database_name = self.db_entry.get()
            output_file_path = "output.txt"  # Change this to the desired output file path

            sqlmap_output = self.sqlmap_tables(url, database_name, output_file_path)

            # Display the output in the Tkinter window
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, sqlmap_output)
        except Exception as e:
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, f"Error: {e}")

    def sqlmap_tables(self, url, database_name, output_file_path):
        sqlmap_path = self.find_sqlmap()

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

                output_lines.append(f"Output written to '{output_file_path}'")

                return '\n'.join(output_lines)
            else:
                return f"No tables found for database '{clean_database_name}'."
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running SQLMap: {e}")

    def find_sqlmap(self):
        sqlmap_path = shutil.which("sqlmap")
        if sqlmap_path is None:
            raise Exception("SQLMap not found. Make sure it's installed and available in the system PATH.")
        return sqlmap_path


class ThirdTab:
    def __init__(self, master):
        self.master = master
        # self.master.title("SQLMap GUI - Get Tables Names")  # Comment this line

        # UI Elements
        self.url_label = tk.Label(master, text="Enter URL:")
        self.url_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.url_entry = ttk.Entry(master, width=50)
        self.url_entry.insert(0, "http://testphp.vulnweb.com/listproducts.php?cat=1")
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

        self.execute_button = tk.Button(master, text="Run SQLMap", command=self.run_sqlmap)
        self.execute_button.grid(row=1, column=0, columnspan=3, pady=10)

        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def run_sqlmap(self):
        try:
            url = self.url_entry.get()
            output_file_path = "tables_output.txt"  # Change this to the desired output file path

            table_names_output = self.sqlmap_tables(url, output_file_path)

            # Display the output in the Tkinter window
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, table_names_output)
        except Exception as e:
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, f"Error: {e}")

    def sqlmap_tables(self, url, output_file_path):
        sqlmap_path = self.find_sqlmap()
        command = [sqlmap_path, '-u', url, '--tables']

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            table_names = result.stdout.strip().split('\n')[1:]

            output_lines = [f"Tables found at '{url}':"]
            for index, table_name in enumerate(table_names, start=1):
                output_lines.append(f"{index}. {table_name}")

            with open(output_file_path, 'w') as output_file:
                for line in output_lines:
                    output_file.write(line + '\n')

            output_lines.append(f"Output written to '{output_file_path}'")

            return '\n'.join(output_lines)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running SQLMap: {e}")

    def find_sqlmap(self):
        sqlmap_path = shutil.which("sqlmap")
        if sqlmap_path is None:
            raise Exception("SQLMap not found. Make sure it's installed and available in the system PATH.")
        return sqlmap_path
    
class FourthTab:
    def __init__(self, master):
        self.master = master

        # UI Elements
        self.label = tk.Label(master, text="Database Dashboard Security", font=('Helvetica', 20))
        self.label.pack(pady=20)

        self.url_frame = tk.Frame(master)
        self.url_frame.columnconfigure(0, weight=1)
        self.url_frame.columnconfigure(1, weight=1)

        self.url_text = tk.Label(self.url_frame, text="Enter URL:", font=('Helvetica', 14))
        self.url_text.grid(row=0, column=0)

        self.url_entry = tk.Entry(self.url_frame, font=('Helvetica', 14))
        self.url_entry.grid(row=0, column=1)
        
        self.db_text = tk.Label(self.url_frame, text="Enter database names filepath:", font=('Helvetica', 14))
        self.db_text.grid(row=1, column=0)
        
        self.database_filename = tk.Entry(self.url_frame, font=('Helvetica', 14))
        self.database_filename.grid(row=1, column=1)
        
        self.tb_text = tk.Label(self.url_frame, text="Enter tablenames filepath:", font=('Helvetica', 14))
        self.tb_text.grid(row=2, column=0)
        
        self.tables_filename = tk.Entry(self.url_frame, font=('Helvetica', 14))
        self.tables_filename.grid(row=2, column=1)

        self.url_frame.pack(fill='x')

        self.button = tk.Button(master, text="Get table info", font=('Helvetica', 14), command=self.run_funct)
        self.button.pack(pady=20, padx=20)

        self.result_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.result_text.pack()

    def run_funct(self):
        try:
            url = self.url_entry.get()
            database_filename = self.database_filename.get()
            tables_filename = self.tables_filename.get()

            # Call the appropriate function here using url and crawl_level
            # For example, you can replace the following line with your function call
            result_output = sqlmap_functionality(url, database_filename, tables_filename)

            self.result_text.delete(1.0, tk.END)  # Clear previous output
            for line in result_output:
                self.result_text.insert(tk.END, line)
        except Exception as e:
            self.result_text.delete(1.0, tk.END)  # Clear previous output
            self.result_text.insert(tk.END, f"Error: {e}")



class DashboardGUI:
    def __init__(self, master):
        self.master = master
        master.geometry("800x800")
        master.title("Database Dashboard Security")

        # Top bar with tabs
        self.top_bar = ttk.Notebook(master)
        self.dashboard_tab = tk.Frame(self.top_bar)
        self.database_tab = tk.Frame(self.top_bar)
        self.tables_tab = tk.Frame(self.top_bar)
        self.tables_info_tab = tk.Frame(self.top_bar)

        self.top_bar.add(self.dashboard_tab, text="URL Scan")
        self.top_bar.add(self.database_tab, text="Get Table Names")
        self.top_bar.add(self.tables_tab, text="Get Database Names")
        self.top_bar.add(self.tables_info_tab, text="Get Table Info")

        self.top_bar.pack(fill='x')

        # Content for the first tab (Dashboard)
        self.dashboard_content = FirstTab(self.dashboard_tab)

        # Content for the second tab (Get Database Names)
        self.get_database_name_content = SecondTab(self.database_tab)

        # Content for the third tab (Get Table Names)
        self.get_tables_name_content = ThirdTab(self.tables_tab)
        
        #Fourth Tab
        self.get_tables_info_content = FourthTab(self.tables_info_tab)
        


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardGUI(root)
    root.mainloop()

