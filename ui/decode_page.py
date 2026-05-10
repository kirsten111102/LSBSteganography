import customtkinter as ctk
from tkinter import filedialog
from core.integration import run_decode

class DecodePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.stego_path = ""

        ctk.CTkLabel(self, text="Decode Hidden Message", font=("Arial", 24)).pack(pady=20)

        ctk.CTkButton(self, text="Upload Stego File", command=self.upload_stego).pack(pady=10)
        self.file_label = ctk.CTkLabel(self, text="No file selected")
        self.file_label.pack()

        ctk.CTkButton(self, text="Start Decoding", command=self.start_decoding).pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

    def upload_stego(self):
        self.stego_path = filedialog.askopenfilename()
        self.file_label.configure(text=self.stego_path)

    def start_decoding(self):
        result = run_decode(self.stego_path)
        self.result_label.configure(text=result)