import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
import cv2

class Player:
    def __init__(self, name, max_hp, pos):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp/2
        self.pos = pos
        
    def set_current_hp(self, hp):
        self.hp = hp
        
    def create_image(self):
        img = np.zeros((151,201,3), np.uint8)
        cv2.putText(img, self.name, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.line(img, (10, 100), (190, 100), (200,200,200), 10)
        cv2.line(img, (10, 100), (10 + int(180*(self.hp/self.max_hp)), 100), (50,255,50), 10)
        
        return img
    
    def visualize(self, img):
        cv2.imshow(self.name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class GUI:
    def __init__(self, root, image_path, players):
        self.root = root
        self.players = players
        self.root.title("Image Zoom App")
        self.root.geometry("1280x720")

        # top buttons
        self.top_frame = tk.Frame(self.root)
        self.top_frame.rowconfigure(0, weight=1)
        
        self.btn1 = tk.Button(self.top_frame, text="zoom in")
        self.btn1.grid(row=0, column=0, sticky=tk.W+tk.E)
        self.btn2 = tk.Button(self.top_frame, text="zoom out")
        self.btn2.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.btn3 = tk.Button(self.top_frame, text="Change Image", command=self.change_image)
        self.btn3.grid(row=0, column=2, sticky=tk.W+tk.E)
        
        self.top_frame.pack(fill='x')
        
        # Load the image and set the initial zoom level
        self.image = Image.open(image_path)
        self.zoom_level = 1.0

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height, background='black')
        self.canvas.pack()

        # Display the image on the canvas
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_item = self.canvas.create_image(0, 0, image=self.image_tk)
        self.playerImgs = []
        for player in self.players:
            self.playerImgs.append(self.canvas.create_image(player.pos[0], player.pos[1], image=ImageTk.PhotoImage(Image.fromarray(player.create_image()))))

        # Bind mouse wheel and dragging events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_stop)
        
    def change_image(self):
        self.filename = askopenfilename()
        self.image = Image.open(self.filename)
        self.update_image()
        

    def on_drag_start(self, event):
        self.x = event.x
        self.y = event.y
    
    def on_drag_stop(self, event):
        self.x = 0
        self.y = 0

    def on_mouse_wheel(self, event):
        # Zoom the image in or out based on the mouse wheel direction
        if event.delta > 0:
            self.zoom_level *= 1.2
        else:
            self.zoom_level /= 1.2

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
        
        # Change Image here, add players
        player_Image = Image.fromarray(self.add_players(resized_image))
        #cv2.imshow("test", self.add_players(resized_image))
        #cv2.waitKey(0)
        # Update the canvas with the new image
        self.image_tk = ImageTk.PhotoImage(player_Image)
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
        

if __name__ == "__main__":
    p1 = Player("Dudueeee", 10, (200, 200))
    #p1.visualize(p1.create_image())
    image_path = "Roguemoor.jpg"
    root = tk.Tk()
    app = GUI(root, image_path, [p1])
    root.mainloop()
