from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz
from PIL import ImageTk
import spacy

nlp = spacy.load("en_core_web_lg")


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

        self.buttons()

        self.windows_widgets()

        self.extract_text_show_entry()

        self.current_page_number()

    def buttons(self):
        self.open_button=tk.Button(self,text="Open PDF",command=self.load_pdf)
        self.open_button.pack()

        self.prev_button = tk.Button(self, text="Previous Page", command=self.show_prev_page)
        self.prev_button.pack()

        self.next_button = tk.Button(self, text="Next Page", command=self.show_next_page)
        self.next_button.pack()

        self.process_button = tk.Button(self, text="Process", command=self.process)
        self.process_button.pack()

        self.text_clear_button = tk.Button(self, text="Clear", command=self.clear_text)
        self.text_clear_button.pack()

        self.exit_button=tk.Button(self, text="Exit",command=self.destroy)
        self.exit_button.pack()


    def clear_text(self):
        self.text_extract_entry.delete('1.0','end')

    def extract_text_show_entry(self):
        self.text_extract_label=tk.Label(self.canvas_right, text="Extracted Text")
        self.text_extract_label.grid(row=9,column=0,padx=5,pady=5)

        self.text_extract_entry=tk.Text(self.canvas_right,height=8,width=30)
        self.scroll = tk.Scrollbar(self.canvas_right)

        self.text_extract_entry.configure(yscrollcommand=self.scroll.set)
        self.text_extract_entry.place(x=10, y=250, width=560, height=200)

    def process(self):
        document=self.pdf_document[self.current_page]
        self.text=document.get_text()
        # print(self.text)
        self.text_extract_entry.delete('1.0','end')
        self.text_extract_entry.insert(tk.END,self.text)
        self.entity_extraction()

    def current_page_number(self):
        self.current_page_label = tk.Label(self.canvas_right, text="Current Page")
        self.current_page_label.grid(row=8, column=0, padx=5, pady=5)

        self.current_page_entry = tk.Entry(self.canvas_right)
        self.current_page_entry.grid(row=8, column=1, padx=10, pady=10)

    def windows_widgets(self):
        self.name_label = tk.Label(self.canvas_right, text="Name:")
        self.name_label.grid(row=3, column=0, padx=5, pady=5)

        self.name_entry = tk.Text(self.canvas_right,height=1,width=25)
        self.name_entry.grid(row=3, column=1, padx=5, pady=5)

        self.date_label = tk.Label(self.canvas_right, text="Date:")
        self.date_label.grid(row=4, column=0, padx=5, pady=5)

        self.date_entry = tk.Text(self.canvas_right,height=1,width=25)
        self.date_entry.grid(row=4, column=1, padx=5, pady=5)

        self.org_label = tk.Label(self.canvas_right, text="Org:")
        self.org_label.grid(row=5, column=0, padx=5, pady=5)

        self.org_entry = tk.Text(self.canvas_right,height=1,width=25)
        self.org_entry.grid(row=5, column=1, padx=5, pady=5)

        self.address_label = tk.Label(self.canvas_right, text="Address:")
        self.address_label.grid(row=6, column=0, padx=5, pady=5)

        self.address_entry = tk.Text(self.canvas_right,height=1,width=25)
        self.address_entry.grid(row=6, column=1, padx=5, pady=5)

        self.phone_label = tk.Label(self.canvas_right, text="Phone:")
        self.phone_label.grid(row=7, column=0, padx=5, pady=5)

        self.phone_entry = tk.Text(self.canvas_right,height=1,width=25)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=10)

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
        self.current_page_entry.delete(0,tk.END)
        self.current_page_entry.insert(1,str(self.current_page+1))
        self.show_current_page()

    def show_next_page(self):
        if self.pdf_document is None or self.current_page == len(self.pdf_document) - 1:
            return

        self.current_page += 1
        self.current_page_entry.delete(0, tk.END)
        self.current_page_entry.insert(1,str(self.current_page+1))
        self.show_current_page()

    def entity_extraction(self):
        doc=nlp(self.text)
        for entity in doc.ents:
            print(entity.text,"__________________", entity.label_)
            if entity.text is not None and entity.label_=='PERSON':
                self.entity_name=entity.text
                self.name_entry.delete('1.0', 'end')
                self.name_entry.insert(tk.END, self.entity_name)
            if entity.text is not None and entity.label_=='DATE':
                self.entity_date=entity.text
                self.date_entry.delete('1.0', 'end')
                self.date_entry.insert(tk.END, self.entity_date)
            if entity.text is not None and entity.label_=='CARDINAL':
                self.entity_phone=entity.text
                self.phone_entry.delete('1.0', 'end')
                self.phone_entry.insert(tk.END, self.entity_phone)
            if entity.text is not None and entity.label_ == 'GPE':
                self.entity_address = entity.text
                self.address_entry.delete('1.0', 'end')
                self.address_entry.insert(tk.END, self.entity_address)
            if entity.text is not None and entity.label_ == 'ORG':
                self.entity_org = entity.text
                self.org_entry.delete('1.0', 'end')
                self.org_entry.insert(tk.END, self.entity_org)


if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()