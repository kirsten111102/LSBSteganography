import customtkinter as ctk
from ui.dashboard import DashboardPage
from ui.encode_page import EncodePage
from ui.decode_page import DecodePage
from ui.compare_page import ComparePage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StegoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LSB Audio Steganography Studio")
        self.geometry("1200x800")

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", expand=True, fill="both")

        ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Encode", command=self.show_encode).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Decode", command=self.show_decode).pack(pady=10, padx=10)
        ctk.CTkButton(self.sidebar, text="Compare", command=self.show_compare).pack(pady=10, padx=10)

        self.current_page = None
        self.show_dashboard()

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main()
        DashboardPage(self.main_frame).pack(expand=True, fill="both")

    def show_encode(self):
        self.clear_main()
        EncodePage(self.main_frame).pack(expand=True, fill="both")

    def show_decode(self):
        self.clear_main()
        DecodePage(self.main_frame).pack(expand=True, fill="both")

    def show_compare(self):
        self.clear_main()
        ComparePage(self.main_frame).pack(expand=True, fill="both")

if __name__ == "__main__":
    app = StegoApp()
    app.mainloop()