import tkinter as tk
from PIL import ImageTk, Image

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.zoom = 1
        # Set window properties
        self.window.geometry("1280x720")
        self.window.title("DnD GUI")
        
        # top buttons
        self.top_frame = tk.Frame(self.window)
        self.top_frame.rowconfigure(0, weight=1)
        
        self.btn1 = tk.Button(self.top_frame, text="zoom in", command=self.zoom_in)
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn2 = tk.Button(self.top_frame, text="zoom out")
        self.btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.btn3 = tk.Button(self.top_frame, text="move left")
        self.btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
        
        self.top_frame.pack(fill='x')
        
        # Image
        self.OGimage = Image.open('Roguemoor.jpg')
        self.image = ImageTk.PhotoImage(self.OGimage)
        
        self.image_label = tk.Label(self.window, image=self.image)
        self.image_label.pack()
        
        
        self.window.mainloop()
        
    def zoom_in(self):
        width, height = self.OGimage.size
        self.zoom += 0.1
        self.image = self.OGimage.resize((int(width*self.zoom), int(height*self.zoom)), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.image)
        print(self.zoom)
        
if __name__ == "__main__":
    gui = GUI()