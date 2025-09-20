import tkinter as tk
from PIL import Image, ImageTk
import os

class OutputDisplay:
    def __init__(self, parent_frame):
        self.frame = tk.Frame(parent_frame)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.result_label = tk.Label(self.frame, text="Results will appear here", wraplength=500)
        self.result_label.pack(pady=10)

        self.image_label = tk.Label(self.frame)
        self.image_label.pack(pady=10)

    def display_text(self, text):
        self.result_label.config(text=text)
        self.image_label.config(image="")

    def display_image(self, image_path):
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep reference
            self.result_label.config(text="Image generated successfully!")