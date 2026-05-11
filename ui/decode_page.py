import customtkinter as ctk
from tkinter import filedialog
from core.integration import run_decode


class DecodePage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.stego_path = ""

        ctk.CTkLabel(
            self,
            text="Decode Hidden Message",
            font=("Arial", 24)
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Upload Stego File",
            command=self.upload_stego
        ).pack(pady=10)

        self.file_label = ctk.CTkLabel(
            self,
            text="No file selected"
        )

        self.file_label.pack()

        self.hidden_type = ctk.StringVar(
            value="text"
        )

        ctk.CTkOptionMenu(
            self,
            values=["text", "image", "audio"],
            variable=self.hidden_type
        ).pack(pady=10)

        self.output_entry = ctk.CTkEntry(
            self,
            placeholder_text="Output Name"
        )

        self.output_entry.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        ctk.CTkButton(
            self,
            text="Start Decoding",
            command=self.start_decoding
        ).pack(pady=20)

        self.result_label = ctk.CTkLabel(
            self,
            text=""
        )

        self.result_label.pack(pady=10)

    def upload_stego(self):

        self.stego_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.wav *.mp3")
            ]
        )

        if self.stego_path:

            self.file_label.configure(
                text=self.stego_path
            )

    def start_decoding(self):

        if not self.stego_path:

            self.result_label.configure(
                text="Please upload a stego file."
            )

            return

        output_name = self.output_entry.get().strip()

        if not output_name:

            output_name = "recovered"

        result = run_decode(
            encoded_file=self.stego_path,
            hidden_type=self.hidden_type.get(),
            output_name=output_name
        )

        if result["success"]:

            self.result_label.configure(
                text=(
                    f"{result['message']}\n"
                    f"Saved to:\n"
                    f"{result['output_path']}"
                )
            )

        else:

            self.result_label.configure(
                text=f"Error: {result['message']}"
            )