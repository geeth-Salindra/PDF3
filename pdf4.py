import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyttsx3
import fitz  # PyMuPDF

class PDFToVoiceConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF4")

        self.pdf_label = tk.Label(master, text="Select PDF File:")
        self.pdf_label.pack()

        self.pdf_path_entry = tk.Entry(master, width=50)
        self.pdf_path_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_pdf)
        self.browse_button.pack()

        self.progress_label = tk.Label(master, text="")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(master, mode="indeterminate")
        self.progress_bar.pack()

        self.convert_button = tk.Button(master, text="Convert to Voice", command=self.convert_pdf_to_voice)
        self.convert_button.pack()

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.pdf_path_entry.delete(0, tk.END)
        self.pdf_path_entry.insert(0, file_path)

    def convert_pdf_to_voice(self):
        pdf_path = self.pdf_path_entry.get()
        output_file_path = "output.mp3"

        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        try:
            self.progress_label.config(text="Converting...")
            self.progress_bar.start()

            self.convert_pdf(pdf_path, output_file_path)

        except Exception as e:
            self.progress_label.config(text="")
            self.progress_bar.stop()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def convert_pdf(self, pdf_path, output_file_path):
        try:
            text = pdf_to_text(pdf_path)
            text_to_speech_local(text, output_file_path)

            self.progress_label.config(text="Conversion Complete")
            self.progress_bar.stop()

            messagebox.showinfo("Conversion Complete", f"Audio file saved at: {os.path.abspath(output_file_path)}")
        except Exception as e:
            self.progress_label.config(text="")
            self.progress_bar.stop()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def pdf_to_text(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        return text

def text_to_speech_local(text, output_path):
    engine = pyttsx3.init()

    # Set voice to Microsoft Zira
    voices = engine.getProperty('voices')
    for voice in voices:
        if "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.save_to_file(text, output_path)
    engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToVoiceConverterApp(root)
    root.mainloop()
