import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pdfminer.high_level import extract_text
import pyttsx3
from tempfile import NamedTemporaryFile
import platform
import subprocess

class PDFToVoiceConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF to Voice Converter")

        self.pdf_label = tk.Label(master, text="Select PDF File:")
        self.pdf_label.pack()

        self.pdf_path_entry = tk.Entry(master, width=50)
        self.pdf_path_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_pdf)
        self.browse_button.pack()

        self.language_label = tk.Label(master, text="Enter Language Code (default is 'en'):")
        self.language_label.pack()

        self.language_entry = tk.Entry(master, width=50)
        self.language_entry.pack()

        self.convert_button = tk.Button(master, text="Convert to Voice", command=self.convert_pdf_to_voice)
        self.convert_button.pack()

        self.play_button = tk.Button(master, text="Play Audio", command=self.play_generated_audio)
        self.play_button.pack()

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.pdf_path_entry.delete(0, tk.END)
        self.pdf_path_entry.insert(0, file_path)

    def convert_pdf_to_voice(self):
        pdf_path = self.pdf_path_entry.get()
        language_code = self.language_entry.get() or 'en'

        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        try:
            text = pdf_to_text(pdf_path)
            output_file_path = convert_to_voice(text, pdf_path, language_code)
            messagebox.showinfo("Conversion Complete", f"Audio file saved at: {output_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def play_generated_audio(self):
        pdf_path = self.pdf_path_entry.get()
        audio_path = os.path.splitext(pdf_path)[0] + "_output.mp3"

        if os.path.exists(audio_path):
            self.play_audio_file(audio_path)
        else:
            messagebox.showerror("Error", "Audio file not found. Please convert the PDF to voice first.")

    def play_audio_file(self, audio_path):
        system_platform = platform.system().lower()
        if system_platform == "darwin":
            subprocess.run(["open", audio_path])
        elif system_platform == "linux":
            subprocess.run(["xdg-open", audio_path])
        elif system_platform == "windows":
            os.startfile(audio_path)
        else:
            messagebox.showerror("Error", "Unsupported platform for audio playback.")

def pdf_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        return extract_text(file)

def convert_to_voice(text, pdf_path, language='en'):
    engine = pyttsx3.init()
    engine.setProperty('gender', 'female')  # Set gender to female

    output_audio_path = os.path.splitext(pdf_path)[0] + "_output.mp3"
    engine.save_to_file(text, output_audio_path)
    engine.runAndWait()

    return output_audio_path

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToVoiceConverterApp(root)
    root.mainloop()
