import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import re
import threading
from typing import Dict, List
from googletrans import Translator, LANGUAGES

class LanguageData:
    def __init__(self):
        self.languages = LANGUAGES
        self.translations = self.load_translations()

    def load_translations(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        def default_translations() -> Dict[str, Dict[str, Dict[str, str]]]:
            return {
                "en": {
                    "hello": {"es": "hola", "fr": "bonjour", "de": "hallo", "ur": "ہیلو"},
                    "world": {"es": "mundo", "fr": "monde", "de": "welt", "ur": "دنیا"}
                },
                "es": {
                    "hola": {"en": "hello", "fr": "bonjour", "de": "hallo", "ur": "ہیلو"},
                    "mundo": {"en": "world", "fr": "monde", "de": "welt", "ur": "دنیا"}
                }
            }

        try:
            with open("translations.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading translations: {e}. Using default translations.")
            return default_translations()

    def get_language_codes(self) -> List[str]:
        return list(self.languages.keys())

    def get_language_names(self) -> List[str]:
        return [name.capitalize() for name in self.languages.values()]

    def get_language_name(self, code: str) -> str:
        return self.languages.get(code, "Unknown").capitalize()

    def get_language_code(self, name: str) -> str:
        return next((code for code, lang in self.languages.items() if lang.capitalize() == name), "en")

class TranslationEngine:
    def __init__(self, language_data: LanguageData):
        self.language_data = language_data
        self.translator = Translator()

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        try:
            translation = self.translator.translate(text, src=source_lang, dest=target_lang)
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

class ProfessionalTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Translator")
        self.root.geometry("800x300")
        self.root.configure(bg="#2E2E2E")
        
        self.language_data = LanguageData()
        self.translation_engine = TranslationEngine(self.language_data)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.source_lang = tk.StringVar(value="English")
        self.target_lang = tk.StringVar(value="Urdu")
        self.auto_translate_var = tk.BooleanVar(value=True)
        self.auto_translate_thread = None

        self.create_widgets()
        self.create_menu()

    def configure_styles(self):
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure("TLabel", background="#2E2E2E", foreground="#D3D3D3")
        self.style.configure("TButton", background="#555555", foreground="#D3D3D3")
        self.style.configure("TCheckbutton", background="#2E2E2E", foreground="#D3D3D3")
        self.style.configure("TCombobox", background="#555555", foreground="#D3D3D3")
        self.style.map("TButton",
                       background=[('active', '#555555')],
                       foreground=[('active', '#D3D3D3')])

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Language selection frame
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(lang_frame, text="From:").grid(row=0, column=0, padx=(0, 5))
        self.source_lang_combo = ttk.Combobox(lang_frame, textvariable=self.source_lang, 
                                              values=self.language_data.get_language_names(), state="readonly")
        self.source_lang_combo.grid(row=0, column=1, padx=5)

        ttk.Button(lang_frame, text="⇄", command=self.swap_languages, width=3).grid(row=0, column=2, padx=5)

        ttk.Label(lang_frame, text="To:").grid(row=0, column=3, padx=(5, 5))
        self.target_lang_combo = ttk.Combobox(lang_frame, textvariable=self.target_lang, 
                                              values=self.language_data.get_language_names(), state="readonly")
        self.target_lang_combo.grid(row=0, column=4, padx=(0, 5))

        # Text areas
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(1, weight=1)

        source_frame = ttk.LabelFrame(text_frame, text="Original Text", padding="5")
        source_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.source_text = tk.Text(source_frame, wrap=tk.WORD, height=10, bg="#1E1E1E", fg="#D3D3D3", insertbackground="#D3D3D3")
        self.source_text.pack(fill=tk.BOTH, expand=True)

        target_frame = ttk.LabelFrame(text_frame, text="Translated Text", padding="5")
        target_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.translated_text = tk.Text(target_frame, wrap=tk.WORD, height=10, bg="#1E1E1E", fg="#D3D3D3", insertbackground="#D3D3D3")
        self.translated_text.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="Translate", command=self.translate_text).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear", command=self.clear_text).pack(side=tk.LEFT)
        ttk.Checkbutton(button_frame, text="Auto Translate", variable=self.auto_translate_var, 
                        command=self.toggle_auto_translate).pack(side=tk.RIGHT)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Text", command=self.import_text)
        file_menu.add_command(label="Export Translation", command=self.export_translation)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy Original", command=lambda: self.copy_text(self.source_text))
        edit_menu.add_command(label="Copy Translation", command=lambda: self.copy_text(self.translated_text))
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All", command=self.clear_text)

    def translate_text(self):
        text = self.source_text.get("1.0", tk.END).strip()
        if not text:
            return
        source_lang_code = self.language_data.get_language_code(self.source_lang.get())
        target_lang_code = self.language_data.get_language_code(self.target_lang.get())
        translated_text = self.translation_engine.translate(text, source_lang_code, target_lang_code)
        self.translated_text.delete("1.0", tk.END)
        self.translated_text.insert(tk.END, translated_text)

    def clear_text(self):
        self.source_text.delete("1.0", tk.END)
        self.translated_text.delete("1.0", tk.END)

    def swap_languages(self):
        source = self.source_lang.get()
        target = self.target_lang.get()
        self.source_lang.set(target)
        self.target_lang.set(source)
        self.translate_text()

    def import_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.source_text.delete("1.0", tk.END)
            self.source_text.insert(tk.END, content)
            self.translate_text()

    def export_translation(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.translated_text.get("1.0",

 tk.END))

    def copy_text(self, text_widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(text_widget.get("1.0", tk.END))

    def paste_text(self):
        try:
            text = self.root.clipboard_get()
            self.source_text.insert(tk.END, text)
            if self.auto_translate_var.get():
                self.translate_text()
        except tk.TclError as e:
            messagebox.showerror("Paste Error", str(e))

    def toggle_auto_translate(self):
        if self.auto_translate_var.get():
            self.start_auto_translate()
        else:
            self.stop_auto_translate()

    def start_auto_translate(self):
        if self.auto_translate_thread is None:
            self.auto_translate_thread = threading.Thread(target=self.auto_translate)
            self.auto_translate_thread.daemon = True
            self.auto_translate_thread.start()

    def stop_auto_translate(self):
        if self.auto_translate_thread is not None:
            self.auto_translate_thread = None

    def auto_translate(self):
        while self.auto_translate_var.get():
            self.translate_text()
            self.root.after(1000, self.auto_translate)

def main():
    root = tk.Tk()
    app = ProfessionalTranslator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
