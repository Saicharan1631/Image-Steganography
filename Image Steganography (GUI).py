import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import ttkbootstrap as tb

# Binary encoding & decoding functions
def generate_data(pixels, data):
    data += "##END"
    data_in_binary = [format(ord(i), '08b') for i in data]
    image_data = iter(pixels)

    for binary_char in data_in_binary:
        pixels = list(next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3])

        for bit_index in range(8):
            if (binary_char[bit_index] == '1' and pixels[bit_index] % 2 == 0) or \
               (binary_char[bit_index] == '0' and pixels[bit_index] % 2 != 0):
                pixels[bit_index] -= 1

        yield tuple(pixels[:3])
        yield tuple(pixels[3:6])
        yield tuple(pixels[6:9])

def encryption(img, message):
    width = img.size[0]
    x, y = 0, 0
    for pixel in generate_data(img.getdata(), message):
        img.putpixel((x, y), pixel)
        x = 0 if x == width - 1 else x + 1
        y += 1 if x == 0 else 0

def main_encryption(img_path, text, secret_key, output_filename):
    try:
        if not secret_key:
            messagebox.showerror("Error", "Secret key cannot be empty!")
            return

        text_with_key = secret_key + "||" + text
        image = Image.open(img_path)
        new_image = image.copy()
        encryption(new_image, text_with_key)

        output_filename += ".png"
        new_image.save(output_filename, "png")
        messagebox.showinfo("Success", f"Message encoded successfully!\nSaved as {output_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Encoding failed: {e}")

def main_decryption(img_path, secret_key):
    try:
        image = Image.open(img_path)
        data = ""
        image_data = iter(image.getdata())

        while True:
            pixels = list(next(image_data)[:3] + next(image_data)[:3] + next(image_data)[:3])
            binary_string = ''.join(['0' if i % 2 == 0 else '1' for i in pixels[:8]])
            char = chr(int(binary_string, 2))
            data += char

            if "##END" in data:
                data = data.replace("##END", "")
                break

        if "||" not in data:
            return "No secret key found!"

        saved_key, message = data.split("||", 1)
        if saved_key != secret_key:
            return "Incorrect secret key!"

        return message
    except Exception as e:
        messagebox.showerror("Error", f"Decoding failed: {e}")
        return None

# GUI Class
class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.style = tb.Style("superhero")
        
        self.img_path = ""
        self.notebook = tb.Notebook(root)
        self.encode_tab = tb.Frame(self.notebook)
        self.decode_tab = tb.Frame(self.notebook)
        self.notebook.add(self.encode_tab, text="Encode")
        self.notebook.add(self.decode_tab, text="Decode")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.create_encode_ui()
        self.create_decode_ui()

    def create_encode_ui(self):
        tb.Label(self.encode_tab, text="Select Image:").pack(pady=5)
        self.img_label = tb.Label(self.encode_tab)
        self.img_label.pack(pady=5)
        tb.Button(self.encode_tab, text="Choose Image", bootstyle="primary", command=self.select_image).pack(pady=5)

        # Secret message entry
        self.text_entry = tb.Entry(self.encode_tab, width=50)
        self.text_entry.insert(0, "Enter secret message")
        self.text_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "Enter secret message"))
        self.text_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event, "Enter secret message"))
        self.text_entry.pack(pady=5)

        # Secret Key Entry (Masked)
        self.secret_key_entry = tb.Entry(self.encode_tab, width=50)
        self.secret_key_entry.insert(0, "Enter secret key")
        self.secret_key_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "Enter secret key"))
        self.secret_key_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event, "Enter secret key"))
        self.secret_key_entry.pack(pady=5)

        # Output File Name Entry
        self.output_entry = tb.Entry(self.encode_tab, width=50)
        self.output_entry.insert(0, "Enter output file name")
        self.output_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "Enter output file name"))
        self.output_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event, "Enter output file name"))
        self.output_entry.pack(pady=5)

        tb.Button(self.encode_tab, text="Encode & Save", bootstyle="success", command=self.encode_image).pack(pady=10)

    def create_decode_ui(self):
        tb.Label(self.decode_tab, text="Select Encoded Image:").pack(pady=5)
        self.dec_img_label = tb.Label(self.decode_tab)
        self.dec_img_label.pack(pady=5)
        tb.Button(self.decode_tab, text="Choose Image", bootstyle="primary", command=self.select_encoded_image).pack(pady=5)

        # Secret Key Entry for Decoding (Masked)
        self.dec_secret_key_entry = tb.Entry(self.decode_tab, width=50)
        self.dec_secret_key_entry.insert(0, "Enter secret key")
        self.dec_secret_key_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "Enter secret key"))
        self.dec_secret_key_entry.bind("<FocusOut>", lambda event: self.restore_placeholder(event, "Enter secret key"))
        self.dec_secret_key_entry.pack(pady=5)

        tb.Button(self.decode_tab, text="Decode Message", bootstyle="danger", command=self.decode_image).pack(pady=10)
        self.decoded_text = tk.StringVar()
        self.decoded_label = tb.Label(self.decode_tab, textvariable=self.decoded_text, wraplength=500)
        self.decoded_label.pack(pady=10)

    def clear_placeholder(self, event, placeholder_text):
        entry = event.widget
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            if "secret key" in placeholder_text:
                entry.config(show="*")

    def restore_placeholder(self, event, placeholder_text):
        entry = event.widget
        if not entry.get().strip():
            entry.insert(0, placeholder_text)
            if "secret key" in placeholder_text:
                entry.config(show="")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.img_path = file_path
            img = Image.open(file_path)
            img.thumbnail((200, 200))  # Medium Size Image
            img = ImageTk.PhotoImage(img)
            self.img_ref = img  
            self.img_label.config(image=img)
            self.img_label.image = img  

    def select_encoded_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.img_path = file_path
            img = Image.open(file_path)
            img.thumbnail((200, 200))  # Medium Size Image
            img = ImageTk.PhotoImage(img)
            self.dec_img_ref = img  
            self.dec_img_label.config(image=img)
            self.dec_img_label.image = img  

    def encode_image(self):
        main_encryption(self.img_path, self.text_entry.get().strip(), self.secret_key_entry.get().strip(), self.output_entry.get().strip())

    def decode_image(self):
        self.decoded_text.set(f"Decoded Message: {main_decryption(self.img_path, self.dec_secret_key_entry.get().strip())}")

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = SteganographyApp(root)
    root.mainloop()
