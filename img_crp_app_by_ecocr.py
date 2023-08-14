import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
# import pytesseract
import easyocr
reader=easyocr.Reader(['en'])


# pytesseract.pytesseract.tesseract_cmd = r"D:\KavinKumar-6204\Kavin-Python\Tesseract-OCR\tesseract.exe"


class ImageCropApp:

    def __init__(self, root):

        self.root = root
        self.rect_start = None
        self.image = None
        self.rect_id = None
        self.undo_rect_id = []
        self.rectangles = []

        self.canvas_left = tk.Canvas(root, bg='#DAE1D6', width=700, height=710)
        self.canvas_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_right = tk.Canvas(root, bg='#848C7F', width=760, height=710)
        self.canvas_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_left.bind('<Button-1>', self.on_click)
        self.canvas_left.bind('<B1-Motion>', self.on_drag)
        self.canvas_left.bind('<ButtonRelease-1>', self.on_release)

        self.menubar = tk.Menu(root)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.file)
        self.file.add_command(label="Open Image", command=self.open_image)
        # self.file.add_command(label="Crop and Save", command=self.crop_and_save)
        # self.file.add_command(label='Open New Window',command=self.open_new_window)
        self.file.add_command(label='Exit', command=self.on_closing)

        self.edit = tk.Menu(root)
        self.edit = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=self.edit)
        self.edit.add_command(label='Clear', command=self.clear_text)

        self.edit = tk.Menu(root)
        self.edit = tk.Menu(root, tearoff=0)
        self.menubar.add_cascade(label='Process', command=self.crop_and_process)

        self.undo = tk.Menu(root)
        self.undo = tk.Menu(root, tearoff=0)
        self.menubar.add_cascade(label='Undo', command=self.undo_del_rectangle)

        self.skip_rectangle = tk.Menu(root)
        self.skip_rectangle = tk.Menu(root, tearoff=0)
        self.menubar.add_cascade(label='Skip', command=self.skip_rect)

        root.config(menu=self.menubar)

        self.windows_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def skip_rect(self):
        # print(self.rectangles)
        self.skip_rect_list=()
        self.rectangles.append(self.skip_rect_list)
        # print("After append empty tuple")
        # print(self.rectangles)

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

        self.address_entry = tk.Text(self.canvas_right, height=1, width=25)
        self.address_entry.grid(row=5, column=3, padx=5, pady=5,sticky='nsw')

        self.phone_label = tk.Label(self.canvas_right, text="Phone:")
        self.phone_label.grid(row=7, column=0, padx=5, pady=5)

        self.phone_entry = tk.Text(self.canvas_right, height=1, width=25)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=10)

        self.medicine_label=tk.Label(self.canvas_right,text="Medicines")
        self.medicine_label.grid(row=7,column=2,padx=5,pady=5)

        self.medicine_entry=tk.Text(self.canvas_right,height=1,width=25)
        self.medicine_entry.grid(row=7,column=3,padx=5,pady=5)

    def clear_text(self):
        self.name_entry.delete('1.0', 'end')
        self.date_entry.delete('1.0', 'end')
        self.phone_entry.delete('1.0', 'end')
        self.address_entry.delete('1.0', 'end')
        self.org_entry.delete('1.0', 'end')
        self.medicine_entry.delete('1.0','end')
        # self.rectangles=[]

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            root.destroy()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas_left.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

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

    def crop_and_process(self):
        if self.image and self.rectangles:
            for i,rectangle in enumerate(self.rectangles, start=1):
                if len(rectangle)==4:
                    x0, y0, x1, y1=rectangle
                    cropped_image = self.image.crop((x0, y0, x1, y1))
                    self.text_extraction(i,cropped_image)

    def text_extraction(self,i,image):
        # text = pytesseract.image_to_string(image)
        result = reader.readtext(image)

        for detection in result:
            text=detection[1]
            if i==1:
                self.name_entry.insert(tk.END, text)
            elif i==2:
                self.date_entry.insert(tk.END,text)
            elif i==3:
                self.org_entry.insert(tk.END,text)
            elif i==4:
                self.address_entry.insert(tk.END,text)
            elif i ==5:
                self.phone_entry.insert(tk.END,text)
            elif i==6:
                self.medicine_entry.insert(tk.END,text)

    def undo_del_rectangle(self):
        # rectangle remove code in below
        last_rect_id=self.undo_rect_id[-1]
        self.undo_rect_id.remove(last_rect_id)
        self.canvas_left.delete(last_rect_id)

        # remove rectangles co-ordinates in the self.rectangles list
        # print(self.rectangles)
        last_rect_co_ordinates=self.rectangles[-1]
        self.rectangles.remove(last_rect_co_ordinates)
        # print("After removed")
        # print(self.rectangles)






if __name__ == "__main__":
    root = tk.Tk()
    root.title("Prescription App")
    app = ImageCropApp(root)
    root.mainloop()
