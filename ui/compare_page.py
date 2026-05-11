import customtkinter as ctk
from tkinter import filedialog
from core.integration import run_compare

class ComparePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.original_path = ""
        self.stego_path = ""

        ctk.CTkLabel(self, text="Compare Audio Quality", font=("Arial", 24)).pack(pady=20)

        ctk.CTkButton(self, text="Upload Original Audio", command=self.upload_original).pack(pady=10)
        self.original_label = ctk.CTkLabel(self, text="No original file")
        self.original_label.pack()

        ctk.CTkButton(self, text="Upload Stego Audio", command=self.upload_stego).pack(pady=10)
        self.stego_label = ctk.CTkLabel(self, text="No stego file")
        self.stego_label.pack()

        ctk.CTkButton(self, text="Compare", command=self.compare_files).pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

    def upload_original(self):
        self.original_path = filedialog.askopenfilename()
        self.original_label.configure(text=self.original_path)

    def upload_stego(self):
        self.stego_path = filedialog.askopenfilename()
        self.stego_label.configure(text=self.stego_path)

    def compare_files(self):
        result = run_compare(self.original_path, self.stego_path)
        self.result_label.configure(text=result["message"])