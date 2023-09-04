import tkinter as tk
from tkinter import filedialog
import pandas as pd

def open_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files"," *.csv;*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path)
            data_text.delete(1.0, tk.END)  # Clear previous data
            data_text.insert(tk.END, df.to_string(index=False))
        except Exception as e:
            data_text.delete(1.0, tk.END)
            data_text.insert(tk.END, f"Error: {str(e)}")


root = tk.Tk()
root.title("Excel Viewer")

open_button = tk.Button(root, text="Open Excel File", command=open_excel_file)
open_button.pack()

data_text = tk.Text(root)
data_text.pack()

root.mainloop()
