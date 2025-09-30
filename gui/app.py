import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os

# Import your model selector
from gui.model_selector import ModelSelector


class AIModelGUI:
    def __init__(self, root):
        self._root = root
        self._setup_window()
        self._model_selector = ModelSelector()
        self._current_model = None
        self._uploaded_file = None
        self._create_widgets()
        
    def _setup_window(self):
        self._root.title("HIT137 Assignment 3 - AI Model GUI")
        self._root.geometry("900x700")
        self._root.resizable(True, True)
        style = ttk.Style()
        style.theme_use('clam')
        
    def _create_widgets(self):
        self._create_menu()
        self._create_model_selection()
        self._create_input_section()
        self._create_output_section()
        self._create_info_section()
        
    def _create_menu(self):
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self._root.quit)
        
    def _create_model_selection(self):
        model_frame = ttk.LabelFrame(self._root, text="Model Selection", padding="10")
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(model_frame, text="Select Model:").pack(side=tk.LEFT, padx=5)
        self._model_var = tk.StringVar()
        self._models_list = ["Text-to-Image", "Sentiment Analysis"]
        self._model_combo = ttk.Combobox(
            model_frame,
            textvariable=self._model_var,
            values=self._models_list,
            state="readonly",
            width=30
        )
        self._model_combo.set(self._models_list[0])
        self._model_combo.pack(side=tk.LEFT, padx=5)
        self._model_combo.bind('<<ComboboxSelected>>', self._on_model_selected)
        
        ttk.Button(model_frame, text="Load Model", command=self._load_model).pack(side=tk.LEFT, padx=10)
        
    def _create_input_section(self):
        input_frame = ttk.LabelFrame(self._root, text="User Input", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        type_frame = ttk.Frame(input_frame)
        type_frame.pack(fill=tk.X, pady=5)
        self._input_type = tk.StringVar(value="text")
        ttk.Radiobutton(type_frame, text="Text", variable=self._input_type, value="text").pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="Image", variable=self._input_type, value="image").pack(side=tk.LEFT, padx=10)
        ttk.Button(type_frame, text="Browse", command=self._browse_file).pack(side=tk.LEFT, padx=10)
        
        self._input_text = scrolledtext.ScrolledText(input_frame, height=6, wrap=tk.WORD)
        self._input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Run", command=self._run_model).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self._clear_all).pack(side=tk.LEFT, padx=5)
        
    def _create_output_section(self):
        output_frame = ttk.LabelFrame(self._root, text="Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self._output_container = ttk.Frame(output_frame)
        self._output_container.pack(fill=tk.BOTH, expand=True)
        
        self._output_text = scrolledtext.ScrolledText(self._output_container, height=8, wrap=tk.WORD)
        self._output_text.pack(fill=tk.BOTH, expand=True)
        self._output_image_label = tk.Label(self._output_container)
        
    def _create_info_section(self):
        info_frame = ttk.LabelFrame(self._root, text="Model Information & OOP Explanation", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self._info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, font=("Arial", 9))
        self._info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self._update_info_display()
        
    def _on_model_selected(self, event=None):
        self._update_info_display()
        
    def _browse_file(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self._uploaded_file = filepath
            self._input_text.delete(1.0, tk.END)
            self._input_text.insert(tk.END, f"Selected: {filepath}")
            
    def _load_model(self):
        model_name = self._model_var.get()
        if not model_name:
            messagebox.showwarning("Warning", "Please select a model")
            return
            
        try:
            self._current_model = self._model_selector.get_model(model_name)
            if self._current_model is None:
                messagebox.showerror("Error", "Model not found")
                return
                
            self._output_text.insert(tk.END, f"Loading {model_name}...\n")
            self._root.update()
            
            if self._current_model.load_model():
                self._output_text.insert(tk.END, f"✅ {model_name} loaded successfully!\n\n")
            else:
                self._output_text.insert(tk.END, f"❌ Failed to load {model_name}\n\n")
                self._current_model = None
        except Exception as e:
            messagebox.showerror("Error", f"Error loading model: {str(e)}")
            self._current_model = None
            
    def _run_model(self):
        if not self._current_model:
            messagebox.showwarning("Warning", "Please load a model first")
            return
            
        input_data = self._get_input_data()
        if input_data is None:
            return
            
        try:
            self._output_text.insert(tk.END, "Running model...\n")
            self._root.update()
            result = self._current_model.predict(input_data)
            self._display_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error running model: {str(e)}")
            
    def _get_input_data(self):
        if self._input_type.get() == "text":
            text = self._input_text.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter text")
                return None
            return text
        else:
            if not self._uploaded_file:
                messagebox.showwarning("Warning", "Please select an image")
                return None
            return self._uploaded_file
            
    def _display_result(self, result):
        self._output_text.pack_forget()
        self._output_image_label.pack_forget()
        
        if isinstance(result, str) and result.endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(result)
                img.thumbnail((600, 400))
                photo = ImageTk.PhotoImage(img)
                self._output_image_label.config(image=photo)
                self._output_image_label.image = photo
                self._output_image_label.pack()
                self._output_text.pack(fill=tk.BOTH, expand=True)
                self._output_text.delete(1.0, tk.END)
                self._output_text.insert(tk.END, f"✅ Image generated!\nFile: {result}")
            except Exception as e:
                self._output_text.pack(fill=tk.BOTH, expand=True)
                self._output_text.delete(1.0, tk.END)
                self._output_text.insert(tk.END, f"❌ Image error: {str(e)}")
        else:
            self._output_text.pack(fill=tk.BOTH, expand=True)
            self._output_text.delete(1.0, tk.END)
            self._output_text.insert(tk.END, f"Result:\n{result}\n{'-'*40}\n")
        self._output_text.see(tk.END)
        
    def _update_info_display(self):
        model_name = self._model_var.get()
        if model_name == "Text-to-Image":
            info = """🔤 TEXT-TO-IMAGE MODEL

Model: nota-ai/bk-sdm-small
Category: Image Generation
Description: Generates images from text prompts.

Usage Example:
Enter a prompt like "a red apple on a white table"

OOP Concepts Used:
• Encapsulation: Model logic hidden in TextToImageModel class
• Polymorphism: Both models implement predict() with different behavior
• Method Overriding: get_usage_example() overridden per model
• Composition: GUI uses model objects via ModelSelector"""
        else:  # Sentiment Analysis
            info = """📊 SENTIMENT ANALYSIS MODEL

Model: cardiffnlp/twitter-roberta-base-sentiment-latest
Category: Text Classification
Description: Classifies text as Positive, Neutral, or Negative.

Usage Example:
Enter text like "I love this course!"

OOP Concepts Used:
• Encapsulation: Model logic hidden in SentimentModel class
• Polymorphism: Both models implement predict() with different behavior
• Method Overriding: get_usage_example() overridden per model
• Composition: GUI uses model objects via ModelSelector"""
        self._info_text.delete(1.0, tk.END)
        self._info_text.insert(tk.END, info)
        
    def _clear_all(self):
        self._input_text.delete(1.0, tk.END)
        self._output_text.delete(1.0, tk.END)
        self._output_image_label.pack_forget()
        self._output_text.pack(fill=tk.BOTH, expand=True)
        self._uploaded_file = None
        self._input_type.set("text")