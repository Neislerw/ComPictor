import os
import random
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class PictureComparator:
    def __init__(self, root):
        self.root = root
        self.delete_folder = None
        self.picture_files = []
        self.selected_pictures = []
        
        self.photo_directory = tk.StringVar()
        self.photo_directory.set("")

        self.setup_ui()

    def setup_ui(self):
        self.root.title("Picture Comparator")

        self.photo_entry = tk.Entry(self.root, textvariable=self.photo_directory)
        self.photo_entry.pack(padx=10, pady=10)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_directory)
        self.browse_button.pack(padx=10, pady=10)

        self.load_button = tk.Button(self.root, text="Load Photos", command=self.load_photos)
        self.load_button.pack(padx=10, pady=10)

        self.rotate_button = tk.Button(self.root, text="Rotate Images", command=self.rotate_images)
        self.rotate_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.winner_label = None

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.photo_directory.set(directory)

    def load_photos(self):
        main_folder = self.photo_directory.get()

        if not main_folder:
            tk.messagebox.showerror("Error", "Please select a photo directory.")
            return
        
        self.delete_folder = os.path.join(main_folder, "delete")

        try:
            os.makedirs(self.delete_folder)
        except OSError:
            pass
        
        self.picture_files = [f for f in os.listdir(main_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.main_folder = main_folder  # Store the main folder path
        self.load_next_images()
    def load_next_images(self):
        if len(self.picture_files) > 0:
            if len(self.selected_pictures) > 0:
                self.picture_files.extend(self.selected_pictures)
                self.selected_pictures.clear()
            
            self.picture1 = random.choice(self.picture_files)
            self.picture_files.remove(self.picture1)
            self.picture2 = random.choice(self.picture_files)
            self.picture_files.remove(self.picture2)
            
            self.display_images()
        else:
            self.root.quit()
    
    def display_images(self):
        image1 = Image.open(os.path.join(self.main_folder, self.picture1))
        image2 = Image.open(os.path.join(self.main_folder, self.picture2))

        rotated_image1 = image1.rotate(-90, expand=True)
        rotated_image2 = image2.rotate(-90, expand=True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        max_width = min(rotated_image1.width, rotated_image2.width, screen_width // 2)
        max_height = min(rotated_image1.height, rotated_image2.height, screen_height)

        resized_image1 = rotated_image1.resize((max_width, max_height), Image.LANCZOS)
        resized_image2 = rotated_image2.resize((max_width, max_height), Image.LANCZOS)

        self.tk_image1 = ImageTk.PhotoImage(resized_image1)
        self.tk_image2 = ImageTk.PhotoImage(resized_image2)
        
        self.label1 = tk.Label(self.root, image=self.tk_image1)
        self.label2 = tk.Label(self.root, image=self.tk_image2)
        
        self.label1.pack(side=tk.LEFT, padx=10, pady=10)
        self.label2.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.label1.bind("<Button-1>", self.choose_picture1)
        self.label2.bind("<Button-1>", self.choose_picture2)
    
    def choose_picture1(self, event):
        shutil.move(os.path.join(self.main_folder, self.picture2), os.path.join(self.delete_folder, self.picture2))
        self.cleanup_ui()
        self.selected_pictures.append(self.picture1)
        self.load_next_images()
    
    def choose_picture2(self, event):
        shutil.move(os.path.join(self.main_folder, self.picture1), os.path.join(self.delete_folder, self.picture1))
        self.cleanup_ui()
        self.selected_pictures.append(self.picture2)
        self.load_next_images()

    def rotate_images(self):
        self.display_images()

    def cleanup_ui(self):
        if hasattr(self, 'label1'):
            self.label1.pack_forget()
        if hasattr(self, 'label2'):
            self.label2.pack_forget()

def main():
    root = tk.Tk()
    comparator = PictureComparator(root)
    root.mainloop()
    print("Process completed. One picture remains in the main folder.")

if __name__ == "__main__":
    main()