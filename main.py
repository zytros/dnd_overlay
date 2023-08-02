import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import cv2
import threading
from time import sleep

class Player:
    def __init__(self, name, max_hp, pos):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp/2
        self.pos = pos
        
    def set_current_hp(self, hp):
        self.hp = hp
        
    def create_image(self):
        img = np.zeros((151,201,4), np.uint8)
        cv2.putText(img, self.name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.line(img, (10, 100), (190, 100), (200,200,200), 10)
        cv2.line(img, (10, 100), (10 + int(180*(self.hp/self.max_hp)), 100), (50,255,50), 10)
        
        # set alpha channel to 0 iff pixel is black
        for y in range(151):
            for x in range(201):
                if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 0:
                    img[y][x][3] = 50
                else:
                    img[y][x][3] = 255
        
        return img


class GUI:
    def __init__(self, root:tk.Tk, image_path, players):
        self.root = root
        self.players = players
        self.root.title("DnD GUI")
        self.root.geometry("1280x720")
        self.pos = (0,0)
        self.p1 = players[0]
        self.p2 = players[1]
        self.p3 = players[2]
        self.p4 = players[3]
        self.p5 = players[4]

        # top buttons
        self.top_frame = tk.Frame(self.root)
        self.top_frame.rowconfigure(0, weight=1)
        
        self.btn1 = tk.Button(self.top_frame, text="zoom in", command=self.man_zoom_in)
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn2 = tk.Button(self.top_frame, text="zoom out", command=self.man_zoom_out)
        self.btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.btn3 = tk.Button(self.top_frame, text="Change Image", command=self.change_image)
        self.btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
        
        self.top_frame.pack(fill='x')
        
        # Load the image and set the initial zoom level
        self.original_image = Image.open(image_path)
        self.zoom_level = 1.0
        self.image = self.original_image.copy()

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height, background='black')
        self.canvas.pack()

        # Display the image on the canvas
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_item = self.canvas.create_image(self.pos[0], self.pos[1], anchor='nw' ,image=self.image_tk)
        
        # add player overlays
        self.player_overlays = []
        for player in players:
            self.pil_img = Image.fromarray(player.create_image())
            self.tk_img = ImageTk.PhotoImage(self.pil_img)
            self.canv_player_img = self.canvas.create_image(player.pos[0], player.pos[1], anchor='nw' ,image=self.tk_img)
            self.player_overlays.append((self.pil_img, self.tk_img, self.canv_player_img))


        # Bind mouse wheel and dragging events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        
        
    def change_image(self):
        self.filename = askopenfilename()
        self.image = Image.open(self.filename)
        self.update_image()
        

    def on_drag_start(self, event):
        self.x = event.x
        self.y = event.y


    def on_mouse_wheel(self, event):
        # Zoom the image in or out based on the mouse wheel direction
        if event.delta > 0:
            self.zoom_level += 0.2
        else:
            self.zoom_level -= 0.2

        self.update_image()

    def man_zoom_in(self):
        self.zoom_level += 0.2
        self.update_image()

    def man_zoom_out(self):
        self.zoom_level -= 0.2
        self.update_image()

    def on_drag(self, event):
        # Move the image based on the dragging distance
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.image_item, dx, dy)
        self.x = event.x
        self.y = event.y

    def update_image(self):
        # Calculate the new size of the image based on the zoom level
        new_width = int(self.image.width * self.zoom_level)
        new_height = int(self.image.height * self.zoom_level)

        # Resize the image
        resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
        
        # Change Image here

        # Update the canvas with the new image
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_item, image=self.image_tk)
        
    def add_players(self, image):
        pixels = np.array(image)
        for player in self.players:
            pos = player.pos
            player_pixels = player.create_image()
            for i in range(150):
                for j in range(200):
                    pixels[pos[0]+i][pos[1]+j] = player_pixels[i][j]
        return pixels
        
def openGUI(p1, p2, p3, p4, p5):
    image_path = "Roguemoor.jpg"
    root = tk.Tk()
    app = GUI(root, image_path, [p1, p2, p3, p4, p5])
    root.mainloop()

if __name__ == "__main__":
    p1 = Player("Dudueeee1", 10, (0, 200))
    p2 = Player("Dudueeee2", 10, (0, 400))
    p3 = Player("Dudueeee3", 10, (300, 200))
    p4 = Player("Dudueeee4", 10, (300, 400))
    p5 = Player("Dudueeee5", 10, (600, 200))
    threading.Thread(target=openGUI, args=(p1,p2,p3,p4,p5)).start()
    while(True):
        hp = (p1.hp-1)%10
        p1.set_current_hp(hp)
        print(p1.hp)
        sleep(1)
