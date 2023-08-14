import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
# import pytesseract
import ast
import threading
import pyautogui


# pytesseract.pytesseract.tesseract_cmd =r"Tesseract-OCR/tesseract.exe"


class ImageCropApp:

    def __init__(self, root):
        self.root = root
        self.rect_start = None
        self.image = None
        self.rect_id = None
        self.undo_rect_id = []
        self.data=[]
        self.rectangles = []
        self.co_ordinates_txt_file=None
        self.image_width = 850
        self.image_height = 930
        self.index=0

        self.root.title("Attesta")

        self.root.geometry("1920x1080")

        # self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='logo.png'))      # self.root.iconbitmap("D:\KavinKumar-6204\Kavin-Python\pythonProject2\OCR_projects__\Pdf_processing/tkinter_app_\Application\logo.ico")

        # self.label = tk.Label(self.root, text="© 2024 CAP Digisoft Solution, Inc. All Rights Reserved.")
        # self.label.pack(side="bottom", anchor="se", padx=10, pady=10)

        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)
        self.frame3 = tk.Frame(root)

        self.frame1.pack(fill="both", expand=True)
        self.frame2.pack(fill="both", expand=True)
        self.frame3.pack(fill="both", expand=True)

        # self.root.bind("<Control-j>", self.temp_process())

        self.create_screen2()
        self.create_screen3()

        self.show_screen(self.frame1)

        self.screen_properties()

        self.windows_widgets()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def screen_properties(self):
        self.canvas_left = tk.Canvas(self.frame1, bg='#DAE1D6', width=700, height=710)
        self.canvas_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_right = tk.Canvas(self.frame1, bg='White', width=760, height=710)
        self.canvas_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_left.bind('<Button-1>', self.on_click)
        self.canvas_left.bind('<B1-Motion>', self.on_drag)
        self.canvas_left.bind('<ButtonRelease-1>', self.on_release)

        self.menubar = tk.Menu(root)
        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.file)
        self.file.add_command(label="Open Image", command=self.open_image)
        self.file.add_command(label="Open Folder", command=self.open_folder)
        self.file.add_command(label="Save Co-ordinates", command=self.save_co_ordinates)
        self.file.add_command(label='Load Co-ordinates', command=self.load_co_ordinates)
        self.file.add_command(label='Exit', command=self.on_closing)

        self.edit = tk.Menu(root)
        self.edit = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=self.edit)
        self.edit.add_command(label='Clear', command=self.clear_text)
        self.edit.add_command(label="Undo", command=self.undo_del_rectangle)
        self.edit.add_command(label="Next",command=self.show_next_image)
        self.edit.add_command(label="Previous",command=self.show_previous_image)
        # self.edit.add_command(label="Delete",command=self.delete_image_on_canvas)

        self.process = tk.Menu(root)
        self.process = tk.Menu(root, tearoff=0)
        self.menubar.add_cascade(label='Process', command=self.crop_and_process)

        self.skip_rectangle = tk.Menu(root)
        self.skip_rectangle = tk.Menu(root, tearoff=0)
        self.menubar.add_cascade(label='Skip', command=self.skip_rect)

        root.config(menu=self.menubar)

    def windows_widgets(self):
        # separator_line = self.canvas_right.create_line(100, 20, 500, 20, fill="gray")
        self.title_of_right_canvas=tk.Label(self.canvas_right,text="Processed Text", font=("Helvetica", 16),justify='right',anchor='e')
        self.title_of_right_canvas.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

        self.name_label = tk.Label(self.canvas_right, anchor='e',borderwidth=2, justify="right", text="Name:")
        self.name_label.grid(row=3, column=0, padx=10, pady=10,sticky="w")

        self.name_entry = tk.Text(self.canvas_right,relief='solid',height=1, width=85)
        self.name_entry.grid(row=3, column=1, padx=10, pady=10, sticky='nsw')

        self.date_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Date:")
        self.date_label.grid(row=4, column=0, padx=10, pady=10,sticky="w")

        self.date_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.date_entry.grid(row=4, column=1, padx=10, pady=10, sticky='nsw')

        self.org_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Org:")
        self.org_label.grid(row=5, column=0, padx=10, pady=10,sticky="w")

        self.org_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.org_entry.grid(row=5, column=1, padx=10, pady=10, sticky='nsw')

        self.address_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Address:")
        self.address_label.grid(row=6, column=0, padx=10, pady=10,sticky="w")

        self.address_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.address_entry.grid(row=6, column=1, padx=10, pady=10, sticky='nsw')

        self.phone_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Phone:")
        self.phone_label.grid(row=7, column=0, padx=10, pady=10,sticky="w")

        self.phone_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.phone_entry.grid(row=7, column=1, padx=10, pady=10, sticky='nsw')

        self.email_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Email")
        self.email_label.grid(row=8, column=0, padx=10, pady=10,sticky="w")

        self.email_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.email_entry.grid(row=8, column=1, padx=10, pady=10, sticky='nsw')

        self.dob_label = tk.Label(self.canvas_right, anchor='e',borderwidth=2, justify="right",text="Date of Birth")
        self.dob_label.grid(row=9, column=0, padx=10, pady=10,sticky="w")

        self.dob_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.dob_entry.grid(row=9, column=1, padx=10, pady=10, sticky='nsw')

        self.gender_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Gender")
        self.gender_label.grid(row=10, column=0, padx=10, pady=10,sticky="w")

        self.gender_entry = tk.Text(self.canvas_right,relief='solid', height=1, width=85)
        self.gender_entry.grid(row=10, column=1, padx=10, pady=10, sticky='nsw')

        self.medicine_label = tk.Label(self.canvas_right,anchor='e',borderwidth=2, justify="right", text="Medicines")
        self.medicine_label.grid(row=11, column=0, padx=10, pady=10,sticky="w")

        self.medicine_entry = tk.Text(self.canvas_right,relief='solid', height=6, width=85)
        self.medicine_entry.grid(row=11, column=1, padx=10, pady=10, sticky='nsw')

        self.submit_button=tk.Button(self.canvas_right,text="Submit",command=self.temp_process)
        self.submit_button.grid(row=13, column=1, padx=10, pady=10, sticky='nsw')

        self.root.bind("<Control-j>", self.temp_process)

    def create_screen2(self):
        self.canvas_left = tk.Canvas(self.frame2, bg='white', width=700, height=710)
        self.canvas_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_right = tk.Canvas(self.frame2, bg='#BFE357', width=760, height=710)
        self.canvas_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.windows_widgets()

        # label = tk.Label(self.frame2, text="Screen 2", justify="right")
        # label.pack(padx=20, pady=20)
        button = tk.Button(self.frame2, text="Next", command=lambda: self.show_screen(self.frame3))
        button.pack(padx=20, pady=20)

    def create_screen3(self):
        label = tk.Label(self.frame3, text="Screen 3")
        label.pack(padx=20, pady=20)
        button = tk.Button(self.frame3, text="Restart", command=lambda: self.show_screen(self.frame1))
        button.pack(padx=20, pady=20)

    def show_screen(self, frame):
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        frame.pack(fill="both", expand=True)

    def get_result_from_text_box(self):
        name=self.name_entry.get('1.0','end')
        date=self.date_entry.get('1.0','end')
        address=self.address_entry.get('1.0','end')
        medicine=self.medicine_entry.get('1.0','end')
        dob=self.dob_entry.get('1.0','end')
        email=self.email_entry.get('1.0','end')
        phone_number=self.phone_entry.get('1.0','end')
        org=self.org_entry.get('1.0','end')
        gender=self.gender_entry.get('1.0','end')

        print(name,"------",dob,"------",date,"------",address,"------",medicine,"------",email,"------",phone_number,"------",org,"------",gender)
        # self.data.append((self.file_name,name,org,date,gender,dob,phone_number,email,address,medicine))
        messagebox.showinfo("Success", "Data Collected Successfully")
        # self.clear_text()
        # self.show_next_image()
        # self.crop_and_process()

    def export_to_csv(self):
        if self.data:
            with open("data.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["File Name", "Name","Organization","Date","Gender","Date_of_Birth","Phone Number","Email","Address","Medicines"])
                writer.writerows(self.data)
            messagebox.showinfo("Success", "Data exported to 'data.csv'!")
        else:
            messagebox.showerror("Error", "No data to export.")

    def save_co_ordinates(self):
        file_name = self.file_path.split("/")[-1]
        self.text_file_name = file_name.split(".")[0]
        self.save_text_file_path=filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text Files","*.txt")],initialfile=f'{self.text_file_name}_co-ordinates.txt')
        if self.save_text_file_path:
            with open(self.save_text_file_path, "w") as co_ordinates_file:
                co_ordinates_file.write(str(self.rectangles))

    def load_co_ordinates(self):
        self.co_or_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt;")])
        if self.co_or_path:
            with open(self.co_or_path, "r") as co_file:
                self.co_ordinates_txt_file = (co_file.readlines()[0])
                self.draw_rectangle()

    def draw_rectangle(self):
        if self.co_ordinates_txt_file:
            rectangles = self.co_ordinates_txt_file
            rectangles = ast.literal_eval(rectangles)
            draw = ImageDraw.Draw(self.image)
            for rect in rectangles:
                self.rectangles.append(rect)
                if len(rect) == 4:
                    x0, y0, x1, y1 = rect
                    draw.rectangle((x0, y0, x1, y1), outline='red', width=2)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas_left.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def skip_rect(self):
        # print(self.rectangles)
        self.skip_rect_list = ()
        self.rectangles.append(self.skip_rect_list)
        # print("After append empty tuple")
        # print(self.rectangles)

    def clear_text(self):
        self.name_entry.delete('1.0', 'end')
        self.date_entry.delete('1.0', 'end')
        self.phone_entry.delete('1.0', 'end')
        self.address_entry.delete('1.0', 'end')
        self.org_entry.delete('1.0', 'end')
        self.medicine_entry.delete('1.0', 'end')
        self.gender_entry.delete('1.0','end')
        self.dob_entry.delete('1.0','end')
        self.email_entry.delete('1.0','end')
        # self.rectangles=[]

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit ?"):
            root.destroy()

    def open_folder(self):
        self.folder_path=filedialog.askdirectory()
        if self.folder_path:
            self.image_files=[os.path.join(self.folder_path,file) for file in os.listdir(self.folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            self.current_image_index=0
            self.show_current_image()

    def show_current_image(self):
        if self.image_files and len(self.image_files)>self.current_image_index:
            self.clear_text()
            self.file_path = self.image_files[self.current_image_index]
            print(self.file_path)
            self.image = Image.open(self.file_path)
            self.file_name = self.file_path.split("/")[-1]
            self.image = self.image.resize((self.image_width, self.image_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            root.title(f"Attesta - {self.file_name}")
            self.draw_rectangle()
            self.image_id=self.canvas_left.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

            threading.Thread(target=self.crop_and_process())
        else:
             messagebox.showinfo("Completed","No more images to process")

    def show_previous_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.clear_text()
            self.show_current_image()

    def show_next_image(self):
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1)
            self.delete_image_on_canvas()
            self.show_current_image()

    def delete_image_on_canvas(self):
        if self.image_id:
            print(self.image_id,"Image    ID")
            self.canvas_left.delete(self.image_id)

    def open_image(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.file_path:
            self.file_name = self.file_path.split("/")[-1]
            self.image = Image.open(self.file_path)
            self.image=self.image.resize((self.image_width,self.image_height),Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.image)
            root.title(f"Attesta - {self.file_name}")
            self.image_id=self.canvas_left.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

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
        if self.image:
            if self.image and self.rectangles or self.co_ordinates_txt_file:
                for i, rectangle in enumerate(self.rectangles, start=1):
                    if len(rectangle) == 4:
                        x0, y0, x1, y1 = rectangle
                        cropped_image = self.image.crop((x0, y0, x1, y1))
                        self.text_extraction(i,cropped_image)
            else:
                messagebox.showerror("Error","Kindly draw the co-ordinates or Load the co-ordinates")
        else:
            messagebox.showerror("Error","Kindly Upload the Image you want to Process")

    def temp_process(self,event):
        self.show_next_image()
        self.root.after(15000, self.execute_hotkey)

    def execute_hotkey(self):
        pyautogui.hotkey('ctrl', 'j')

    def text_extraction(self, i, image):
        text = pytesseract.image_to_string(image)
        text=text.strip()
        if i == 1:
            if text:
                self.name_entry.insert(tk.END, text)
            else:
                self.name_entry.insert(tk.END,"Not Found !")
        elif i == 2:
            if text:
                self.date_entry.insert(tk.END, text)
            else:
                self.dob_entry.insert(tk.END,"Not Found !")
        elif i == 3:
            if text:
                self.org_entry.insert(tk.END, text)
            else:
                self.org_entry.insert(tk.END,"Not Found !")
        elif i == 4:
            if text:
                 self.address_entry.insert(tk.END, text)
            else:
                self.address_entry.insert(tk.END,"Not Found !")
        elif i == 5:
            if text:
                self.phone_entry.insert(tk.END, text)
            else:
                self.phone_entry.insert(tk.END,"Not Found !")
        elif i == 6:
            if text:
                self.email_entry.insert(tk.END, text)
            else:
                self.email_entry.insert(tk.END, "Not Found !")
        elif i == 7:
            if text:
                self.dob_entry.insert(tk.END, text)
            else:
                self.dob_entry.insert(tk.END, "Not Found !")
        elif i == 8:
            if text:
                self.gender_entry.insert(tk.END, text)
            else:
                self.gender_entry.insert(tk.END, "Not Found !")
        elif i == 9:
            if text:
                self.medicine_entry.insert(tk.END, text)
            else:
                self.medicine_entry.insert(tk.END,"Not Found !")

    def undo_del_rectangle(self):
        # rectangle remove code in below
        last_rect_id = self.undo_rect_id[-1]
        self.undo_rect_id.remove(last_rect_id)
        self.canvas_left.delete(last_rect_id)

        # remove rectangles co-ordinates in the self.rectangles list
        last_rect_co_ordinates = self.rectangles[-1]
        self.rectangles.remove(last_rect_co_ordinates)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropApp(root)
    root.mainloop()
