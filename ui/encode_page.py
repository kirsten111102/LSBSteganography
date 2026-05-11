import customtkinter as ctk
from tkinter import filedialog
from core.integration import run_encode

class EncodePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.carrier_path = ""
        self.hidden_path = ""

        ctk.CTkLabel(self, text="Encode Hidden Message", font=("Arial", 24)).pack(pady=20)

        ctk.CTkButton(self, text="Upload Carrier Audio", command=self.upload_carrier).pack(pady=10)
        self.carrier_label = ctk.CTkLabel(self, text="No carrier selected")
        self.carrier_label.pack()

        ctk.CTkButton(self, text="Upload Hidden File", command=self.upload_hidden).pack(pady=10)
        self.hidden_label = ctk.CTkLabel(self, text="No hidden file selected")
        self.hidden_label.pack()

        self.format_option = ctk.CTkOptionMenu(self, values=["wav", "mp3"])
        self.format_option.pack(pady=10)

        ctk.CTkButton(self, text="Start Encoding", command=self.start_encoding).pack(pady=20)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack()

    def upload_carrier(self):
        self.carrier_path = filedialog.askopenfilename()
        self.carrier_label.configure(text=self.carrier_path)

    def upload_hidden(self):
        self.hidden_path = filedialog.askopenfilename()
        self.hidden_label.configure(text=self.hidden_path)

    def start_encoding(self):
        result = run_encode(self.carrier_path, self.hidden_path, self.format_option.get())
        self.result_label.configure(text="Encoding completed successfully." if result["success"] else f"Encoding failed: {result['message']}")