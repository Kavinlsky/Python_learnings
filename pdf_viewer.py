import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz

class PDFViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Prescription")

        self.canvas_left=tk.Canvas(self,bg='gray',width=440,height=710)
        self.canvas_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_right=tk.Canvas(self,bg='white',width=760,height=710)
        self.canvas_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.open_button=tk.Button(self,text="Open PDF",command=self.load_pdf)
        self.open_button.pack()

        self.prev_button = tk.Button(self, text="Previous Page", command=self.show_prev_page)
        self.prev_button.pack()

        self.next_button = tk.Button(self, text="Next Page", command=self.show_next_page)
        self.next_button.pack()

        self.next_button = tk.Button(self, text="Process", command=self.process)
        self.next_button.pack()

        self.name_label = tk.Label(self.canvas_right, text="Patient Name:")
        self.name_label.grid(row=3, column=0, padx=5, pady=5)

        self.name_entry = tk.Entry(self.canvas_right)
        self.name_entry.grid(row=3, column=1, padx=5, pady=5)

        self.age_label = tk.Label(self.canvas_right, text="Patient Age:")
        self.age_label.grid(row=4, column=0, padx=5, pady=5)

        self.age_entry = tk.Entry(self.canvas_right)
        self.age_entry.grid(row=4, column=1, padx=5, pady=5)

    def process(self):
        print(self.current_page)

    def load_pdf(self):
        self.pdf_file_path=filedialog.askopenfilename(filetypes=[("PDF Files","*.pdf")])
        if self.pdf_file_path:
            self.open_pdf()

    def open_pdf(self):
        self.pdf_document=fitz.open(self.pdf_file_path)
        self.current_page=0
        self.show_current_page()


    def show_current_page(self):
        if self.pdf_document is None:
            return
        pdf_page=self.pdf_document[self.current_page]
        pix=pdf_page.get_pixmap()
        image=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
        image_tk=ImageTk.PhotoImage(image)
        self.canvas_left.create_image(0, 0, anchor=tk.NW, image=image_tk)
        self.canvas_left.image_tk = image_tk

    def show_prev_page(self):
        if self.pdf_document is None or self.current_page == 0:
            return

        self.current_page -= 1
        print(self.current_page)
        self.show_current_page()

    def show_next_page(self):
        if self.pdf_document is None or self.current_page == len(self.pdf_document) - 1:
            return

        self.current_page += 1
        print(self.current_page)
        self.show_current_page()


if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
