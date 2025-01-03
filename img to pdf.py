import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_folder = None
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        select_images_button.pack(pady=(0, 10))

        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)

        label = tk.Label(self.root, text="Enter output PDF name:")
        label.pack()

        pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify='center')
        pdf_name_entry.pack()

        select_output_dir_button = tk.Button(self.root, text="Select Destination Folder", command=self.select_output_folder)
        select_output_dir_button.pack(pady=(10, 10))

        convert_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_images_to_pdf)
        convert_button.pack(pady=(20, 40))

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_name)

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory(title="Select Destination Folder")
        if self.output_folder:
            messagebox.showinfo("Selected Folder", f"Output files will be saved in:\n{self.output_folder}")

    def convert_images_to_pdf(self):
        if not self.image_paths:
            messagebox.showerror("Error", "Please select at least one image.")
            return

        if not self.output_folder:
            messagebox.showerror("Error", "Please select a destination folder.")
            return

        output_pdf_name = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        output_pdf_path = os.path.join(self.output_folder, output_pdf_name)

        try:
            # Open the first image and convert it to RGB
            first_image = Image.open(self.image_paths[0]).convert("RGB")
            # Convert other images to RGB
            other_images = [
                Image.open(image_path).convert("RGB") for image_path in self.image_paths[1:]
            ]
            # Save all images as a single PDF
            first_image.save(output_pdf_path, save_all=True, append_images=other_images)
            messagebox.showinfo("Success", f"Images successfully converted to PDF:\n{output_pdf_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()


if __name__ == "__main__":
    main()
