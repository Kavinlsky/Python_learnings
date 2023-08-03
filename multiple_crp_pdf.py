import re
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz
from PIL import ImageTk
import spacy
import pytesseract
from medicine_list import mt_medicine_master_list

nlp = spacy.load("en_core_web_lg")

# med_nlp=spacy.load('en_core_sci_sm')


class PDFViewer(tk.Tk):

    def __init__(self):
        super().__init__()

        self.page_number = tk.StringVar()
        self.rect_start = None
        self.image = None
        self.rect_id = None
        self.undo_rect_id = []
        self.rectangles = []

        self.title("Prescription")

        self.screen_properties()

        self.windows_widgets()

        self.extract_text_show_entry()

        self.current_page_number()

    def screen_properties(self):

        self.screen1_frame = tk.Frame(self)
        self.screen2_frame = tk.Frame(self)

        self.canvas_left = tk.Canvas(self, bg='gray', width=400, height=710)
        self.canvas_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_right = tk.Canvas(self, bg='#FAF0E0', width=760, height=710)
        self.canvas_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.canvas_left.bind('<Button-1>', self.on_click)
        self.canvas_left.bind('<B1-Motion>', self.on_drag)
        self.canvas_left.bind('<ButtonRelease-1>', self.on_release)

        self.menubar = Menu(self)
        self.file = Menu(self, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.file)
        self.file.add_command(label="Open PDF", command=self.load_pdf)
        # self.file.add_command(label='Open New Window',command=self.open_new_window)
        self.file.add_command(label='Exit', command=self.on_closing)

        self.edit = Menu(self)
        self.edit = Menu(self, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=self.edit)
        self.edit.add_command(label='Clear', command=self.clear_text)

        self.process_menu = Menu(self)
        self.process_menu = Menu(self, tearoff=0)
        self.menubar.add_cascade(label="Process", command=self.crop_and_process)

        self.go_to_page = Menu(self)
        self.go_to_page = Menu(self, tearoff=0)
        self.menubar.add_cascade(label="Go to", command=self.go_to_page_number)

        # self.store_to_db = Menu(self)
        # self.store_to_db = Menu(self, tearoff=0)
        # self.menubar.add_cascade(label="Store", command=self.store_to_database)


        self.config(menu=self.menubar)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_click(self, event):
        self.rect_start = (event.x, event.y)

    def on_drag(self, event):
        if self.rect_id:
            self.canvas_left.delete(self.rect_id)
        x0, y0 = self.rect_start
        x1, y1 = event.x, event.y
        self.rect_id = self.canvas_left.create_rectangle(x0, y0, x1, y1, outline='red')

    def on_release(self, event):
        if self.rect_id:
            self.undo_rect_id.append(self.rect_id)
            x0, y0 = self.rect_start
            x1, y1 = event.x, event.y
            self.rectangles.append((x0, y0, x1, y1))
            self.rect_start = None
            self.rect_id = None

    def open_new_window(self):
        PDFViewer()

    def go_to_page_number(self):
        page_num = self.page_number.get()
        self.current_page_ = int(page_num)
        self.current_page = self.current_page_ - 1
        self.show_current_page()

    def switch_screen(self):
        pass

    def clear_text(self):
        self.text_extract_entry.delete('1.0', 'end')
        self.name_entry.delete('1.0', 'end')
        self.date_entry.delete('1.0', 'end')
        self.phone_entry.delete('1.0', 'end')
        self.address_entry.delete('1.0', 'end')
        self.org_entry.delete('1.0', 'end')
        self.medicine_entry.delete('1.0','end')
        self.email_entry.delete('1.0','end')

    def extract_text_show_entry(self):
        self.text_extract_label = tk.Label(self.canvas_right, text="Extracted Text")
        self.text_extract_label.grid(row=10, column=0, padx=15, pady=45)

        self.text_extract_entry = tk.Text(self.canvas_right, height=8, width=30)
        self.scroll = tk.Scrollbar(self.canvas_right)

        self.text_extract_entry.configure(yscrollcommand=self.scroll.set)
        self.text_extract_entry.place(x=10, y=250, width=560, height=200)

    def process(self):
        document = self.pdf_document[self.current_page]
        self.text = document.get_text()
        # print(self.text)
        self.text_extract_entry.delete('1.0', 'end')
        self.text_extract_entry.insert(tk.END, self.text)
        self.entity_extraction()
        self.medicine_extraction()
        self.email_extraction()
        self.phone_no_extraction()

    def current_page_number(self):
        self.current_page_label = tk.Label(self.canvas_right, text="Current Page")
        self.current_page_label.grid(row=9, column=0, padx=5, pady=5)

        self.current_page_entry = tk.Entry(self.canvas_right, textvariable=self.page_number)
        self.current_page_entry.grid(row=9, column=1, padx=10, pady=10, sticky='nsw')

        self.prev_button = tk.Button(self.canvas_right, text="Previous Page", command=self.show_prev_page)
        self.prev_button.grid(row=9, column=2, padx=10, pady=5, sticky='nsw')

        self.next_button = tk.Button(self.canvas_right, text="Next Page", command=self.show_next_page)
        self.next_button.grid(row=9, column=3, padx=10, pady=5, sticky='nsw')

        # self.switch_screen_button = tk.Button(self.canvas_right, text="Switch Screen", command=self.show_next_page)
        # self.switch_screen_button.grid(row=8, column=4, padx=10, pady=5, sticky='nsw')

    def windows_widgets(self):
        self.name_label = tk.Label(self.canvas_right, text="Name:")
        self.name_label.grid(row=3, column=0, padx=5, pady=5)

        self.name_entry = tk.Text(self.canvas_right, height=1, width=25)
        self.name_entry.grid(row=3, column=1, padx=5, pady=5)

        self.date_label = tk.Label(self.canvas_right, text="Date:")
        self.date_label.grid(row=3, column=2, padx=5, pady=5)

        self.date_entry = tk.Text(self.canvas_right, height=1, width=15)
        self.date_entry.grid(row=3, column=3, padx=5, pady=5, sticky='nsw')

        self.org_label = tk.Label(self.canvas_right, text="Org:")
        self.org_label.grid(row=5, column=0, padx=5, pady=5)

        self.org_entry = tk.Text(self.canvas_right, height=1, width=25)
        self.org_entry.grid(row=5, column=1, padx=5, pady=5)

        self.address_label = tk.Label(self.canvas_right, text="Address:")
        self.address_label.grid(row=5, column=2, padx=5, pady=5)

        self.address_entry = tk.Text(self.canvas_right, height=1, width=15)
        self.address_entry.grid(row=5, column=3, padx=5, pady=5,sticky='nsw')

        self.phone_label = tk.Label(self.canvas_right, text="Phone:")
        self.phone_label.grid(row=7, column=0, padx=5, pady=5)

        self.phone_entry = tk.Text(self.canvas_right, height=1, width=25)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=10)

        self.medicine_label=tk.Label(self.canvas_right,text="Medicines")
        self.medicine_label.grid(row=7,column=2,padx=5,pady=5)

        self.medicine_entry=tk.Text(self.canvas_right,height=1,width=25)
        self.medicine_entry.grid(row=7,column=3,padx=5,pady=5)

        self.email_label=tk.Label(self.canvas_right,text="Email")
        self.email_label.grid(row=8,column=0,padx=5,pady=5)

        self.email_entry=tk.Text(self.canvas_right,height=1,width=25)
        self.email_entry.grid(row=8,column=1,padx=5,pady=5)

    def crop_and_process(self):
        print(self.rectangles)
        if self.image and self.rectangles:
            for i,rectangle in enumerate(self.rectangles, start=1):
                if len(rectangle)==4:
                    x0, y0, x1, y1=rectangle
                    cropped_image = self.image.crop((x0, y0, x1, y1))
                    self.text_extraction(i,cropped_image)

    def text_extraction(self,i,image):
        pytesseract.pytesseract.tesseract_cmd = r"D:\KavinKumar-6204\Kavin-Python\Tesseract-OCR\tesseract.exe"

        text = pytesseract.image_to_string(image)
        print(text)
        # if i==1:
        #     self.name_entry.insert(tk.END, text)
        # elif i==2:
        #     self.date_entry.insert(tk.END,text)
        # elif i==3:
        #     self.org_entry.insert(tk.END,text)
        # elif i==4:
        #     self.address_entry.insert(tk.END,text)
        # elif i ==5:
        #     self.phone_entry.insert(tk.END,text)
        # elif i==6:
        #     self.medicine_entry.insert(tk.END,text)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            self.destroy()

    def load_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file_path:
            self.open_pdf()

    def open_pdf(self):
        self.pdf_document = fitz.open(self.pdf_file_path)
        self.current_page = 0
        self.show_current_page()

    def show_current_page(self):
        if self.pdf_document is None:
            return
        pdf_page = self.pdf_document[self.current_page]
        # print(type(self.current_page))
        pix = pdf_page.get_pixmap()
        self.image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas_left.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas_left.image_tk = self.image_tk

    def show_prev_page(self):
        if self.pdf_document is None or self.current_page == 0:
            return

        self.current_page -= 1
        self.current_page_entry.delete(0, tk.END)
        self.current_page_entry.insert(1, str(self.current_page + 1))
        self.show_current_page()

    def show_next_page(self):
        if self.pdf_document is None or self.current_page == len(self.pdf_document) - 1:
            return

        self.current_page += 1
        self.current_page_entry.delete(0, tk.END)
        self.current_page_entry.insert(1, str(self.current_page + 1))
        self.show_current_page()

    def entity_extraction(self):
        doc = nlp(self.text)
        # print(self.text)
        name_=[]
        date_=[]
        org_=[]
        address_=[]
        phone_=[]
        for entity in doc.ents:
            # print(entity.text,"__________________", entity.label_)
            if entity.text is not None and entity.label_ == 'PERSON':
                if entity.text not in name_:
                    self.entity_name = entity.text
                    name_.append(self.entity_name)
                    self.name_entry.delete('1.0', 'end')
                self.entity_name=','.join(name_)
                self.name_entry.insert(tk.END, self.entity_name)
            if entity.text is not None and entity.label_ == 'DATE':
                if entity.text not in date_:
                    self.entity_date = entity.text
                    date_.append(self.entity_date)
                    self.date_entry.delete('1.0', 'end')
                self.entity_date=','.join(date_)
                self.date_entry.insert(tk.END, self.entity_date)
            if entity.text is not None and entity.label_ == 'GPE':
                if entity.text not in address_:
                    self.entity_address = entity.text
                    address_.append(self.entity_address)
                    self.address_entry.delete('1.0', 'end')
                self.entity_address=','.join(address_)
                self.address_entry.insert(tk.END, self.entity_address)
            if entity.text is not None and entity.label_ == 'ORG':
                if entity.text not in org_:
                    self.entity_org = entity.text
                    org_.append(self.entity_org)
                    self.org_entry.delete('1.0', 'end')
                self.entity_org=','.join(org_)
                self.org_entry.insert(tk.END, self.entity_org)

    def medicine_extraction(self):
        lists=mt_medicine_master_list
        medicine_=[]
        for i in lists:
            self.id = i[0]
            self.keyword = i[1]
            try:
                key = re.search(f'(?<![a-zA-Z]){self.keyword.lower()}(?![a-zA-Z])', self.text.lower())
            except Exception as e:
                key = self.keyword.lower() in self.text.lower()
            if key:
                medicines=key.group()
                medicine_.append(medicines)
        self.extracted_medicine=",".join(medicine_)
        self.medicine_entry.insert(tk.END,self.extracted_medicine)

    def email_extraction(self):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        self.emails=','.join(emails)
        self.email_entry.insert(tk.END,self.emails)

    def phone_no_extraction(self):
        phone_no_pattern=r'\b(?:\+?[1-9]\d{0,2})?[-.() ]?\d{1,3}[-.() ]?\d{1,3}[-.() ]?\d{2,4}\b'
        phone_numbers = re.findall(phone_no_pattern,self.text)
        self.phone_numbers=','.join(phone_numbers)
        self.phone_entry.insert(tk.END,self.phone_numbers)


if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
