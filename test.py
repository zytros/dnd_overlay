import tkinter as tk
from PIL import Image, ImageTk

class ImageZoomApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Zoom App")
        self.root.geometry("1280x720")

        # Load the image and set the initial zoom level
        self.image = Image.open(image_path)
        self.zoom_level = 1.0

        # Create a canvas to display the image
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()

        # Display the image on the canvas
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_item = self.canvas.create_image(0, 0, image=self.image_tk)

        # Bind mouse wheel and dragging events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_stop)

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
        
        # Change Image here

        # Update the canvas with the new image
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.image_item, image=self.image_tk)

if __name__ == "__main__":
    image_path = "Roguemoor.jpg"  # Replace with the actual path to the image
    root = tk.Tk()
    app = ImageZoomApp(root, image_path)
    root.mainloop()
