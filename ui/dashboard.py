import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(self, text="LSB Audio Steganography Studio", font=("Arial", 28))
        title.pack(pady=30)

        desc = ctk.CTkLabel(
            self,
            text="Hide and extract text, image, or audio inside WAV/MP3 using LSB steganography.",
            font=("Arial", 16)
        )
        desc.pack(pady=10)