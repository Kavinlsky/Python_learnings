import tkinter as tk
from tkinter import messagebox, filedialog

import pandas as pd


class SentimentAnalysis():
    def __init__(self,root):
        self.root=root
        self.window()
        self.window_buttons()

    def window(self):
        self.root.title("Sentiment Analysis")
        self.root.geometry('1080x720')

    def window_buttons(self):
        self.menubar=tk.Menu(root)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File',menu=self.file)
        self.file.add_cascade(label="Open Excel",command=self.load_excel)

        root.config(menu=self.menubar)


    def screen_(self):
        self.data_viewer=tk.Text(root)
        self.data_viewer.pack()

    def load_excel(self):
        self.excel_file_path=filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.csv")])
        if self.excel_file_path:
            print(self.excel_file_path)
            try:
                df = pd.read_excel(self.excel_file_path)
                self.data_viewer.delete(1.0, tk.END)  # Clear previous data
                self.data_viewer.insert(tk.END, df.to_string(index=False))
            except Exception as e:
                self.data_viewer.delete(1.0, tk.END)
                self.data_viewer.insert(tk.END, f"Error: {str(e)}")




if __name__=="__main__":
    root=tk.Tk()
    SentimentAnalysis(root)
    root.mainloop()