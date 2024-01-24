import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyttsx3
import fitz
from gtts import gTTS
import threading

class PDFToVoiceConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF3 V5")

        # Make the GUI non-resizable
        master.resizable(False, False)

        # Set the default tkinter icon
        master.iconbitmap(default='info')

        # Place the GUI in the center of the screen
        window_width = 312
        window_height = 312
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        master.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Title Label
        self.title_label = tk.Label(master, text="PDF3 V5", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=10)

        self.pdf_label = tk.Label(master, text="Select PDF File:")
        self.pdf_label.pack()

        self.pdf_path_entry = tk.Entry(master, width=50)
        self.pdf_path_entry.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_pdf)
        self.browse_button.pack()

        self.voice_label = tk.Label(master, text="Select Voice:")
        self.voice_label.pack()

        self.voice_options = ["Microsoft Zira", "Microsoft David", "Microsoft Mark", "SL Anjali"]
        self.selected_voice = tk.StringVar(value=self.voice_options[0])

        self.voice_dropdown = ttk.Combobox(master, textvariable=self.selected_voice, values=self.voice_options)
        self.voice_dropdown.pack()

        self.output_label = tk.Label(master, text="Select Output Directory:")
        self.output_label.pack()

        self.output_directory_entry = tk.Entry(master, width=50)
        self.output_directory_entry.pack()

        self.browse_output_button = tk.Button(master, text="Browse", command=self.browse_output_directory)
        self.browse_output_button.pack()

        self.progress_label = tk.Label(master, text="")
        self.progress_label.pack()

        self.progress_bar = ttk.Progressbar(master, mode="indeterminate")
        self.progress_bar.pack()

        self.convert_button = tk.Button(master, text="Convert to Voice", command=self.convert_pdf_to_voice)
        self.convert_button.pack()

    def browse_pdf(self):
        # Reset status messages when browsing for a new PDF
        self.progress_label.config(text="", fg="black")

        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        self.pdf_path_entry.delete(0, tk.END)
        self.pdf_path_entry.insert(0, file_path)

    def browse_output_directory(self):
        # Browse for the output directory
        output_directory = filedialog.askdirectory()
        self.output_directory_entry.delete(0, tk.END)
        self.output_directory_entry.insert(0, output_directory)

    def convert_pdf_to_voice(self):
        pdf_path = self.pdf_path_entry.get()
        selected_voice = self.selected_voice.get()
        output_directory = self.output_directory_entry.get()

        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        if not output_directory:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        # Generate output file name based on the PDF file's name
        output_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(pdf_path))[0] + "_output.mp3")

        # Disable the Convert to Voice button during conversion
        self.convert_button.config(state=tk.DISABLED)

        # Start PDF conversion in a separate thread
        threading.Thread(target=self.convert_pdf, args=(pdf_path, output_file_path, selected_voice)).start()

    def convert_pdf(self, pdf_path, output_file_path, selected_voice):
        try:
            text = pdf_to_text(pdf_path)

            # Check if the selected voice is "SL Anjali"
            if selected_voice == "SL Anjali" and not contains_sinhala(text):
                self.update_status("Error: Cannot use 'SL Anjali' for non-Sinhala text.", "red")
                return

            # Continue with conversion
            if contains_sinhala(text):
                text_to_speech_sinhala(text, output_file_path)
            else:
                text_to_speech_local(text, output_file_path, selected_voice)

            self.update_status("Conversion Complete", "green")

            messagebox.showinfo("Conversion Complete", f"Audio file saved at: {os.path.abspath(output_file_path)}")
        except Exception as e:
            self.update_status(f"Error: {str(e)}", "red")
        finally:
            # Enable the Convert to Voice button after conversion
            self.convert_button.config(state=tk.NORMAL)

    def update_status(self, message, color):
        self.progress_label.config(text=message, fg=color)
        self.progress_bar.stop()

def contains_sinhala(text):
    # Check if the text contains Sinhala characters
    sinhala_characters = set("අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖකඛගඝඞඟචඡජඣඤඥඦටඨඩඪණඬතථදධනඳපඵබභමඹයරලවශෂසහළෆ්ාැෑිීුූෘෙේෛොෝෞෟ෠෡෢෣෤෥෦෧෨෩෪෫෬෭෮෯෰෱ෲෳ෴෵෶෷ූ෗ෘෙේෛොෝෞෟ෠෡෢෣෤෥෦෧෨෩෪")

    return any(char in sinhala_characters for char in text)

def pdf_to_text(pdf_path):
    with fitz.open(pdf_path) as pdf_document:
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()
        return text

def text_to_speech_sinhala(text, output_path):
    # Use gTTS for Sinhala text-to-speech
    tts = gTTS(text, lang='si')
    tts.save(output_path)

def text_to_speech_local(text, output_path, selected_voice):
    engine = pyttsx3.init()

    # Set voice based on user selection
    voices = engine.getProperty('voices')
    for voice in voices:
        if selected_voice.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.save_to_file(text, output_path)
    engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToVoiceConverterApp(root)
    root.mainloop()
