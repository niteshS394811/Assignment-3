import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gui.model_selector import ModelSelector
from gui.output_display import OutputDisplay
from models.text_to_image_model import TextToImageModel
from models.sentiment_model import SentimentModel

# =======================
# DECORATOR: Logs user actions
# =======================
def log_action(func):
    """Decorator to log user-triggered actions"""
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] {func.__name__} called")
        return func(self, *args, **kwargs)
    return wrapper


# =======================
# MIXIN CLASS: For logging (demonstrates Multiple Inheritance)
# =======================
class LoggingMixin:
    def log(self, message):
        """Log a message to console"""
        print(f"[MIXIN] {message}")


# =======================
# MAIN GUI CLASS: Inherits from LoggingMixin + tk.Tk → MULTIPLE INHERITANCE
# =======================
class AIAppGUI(LoggingMixin, tk.Tk):
    def __init__(self):
        super().__init__()
        self.log("Initializing GUI...")
        self.title("Tkinter AI GUI")
        self.geometry("800x700")

        # Create menu bar
        self.create_menu()

        # Initialize model selector
        self.model_selector = ModelSelector()
        self.current_model = None

        # Create widgets
        self.create_widgets()

        self.log("GUI initialized successfully.")

    def create_menu(self):
        """Create menu bar with File, Models, Help"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_project)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Models menu
        models_menu = tk.Menu(menubar, tearoff=0)
        models_menu.add_command(label="Text-to-Image", command=lambda: self.select_model("Text-to-Image"))
        models_menu.add_command(label="Sentiment Analysis", command=lambda: self.select_model("Sentiment Analysis"))
        menubar.add_cascade(label="Models", menu=models_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def new_project(self):
        messagebox.showinfo("New Project", "Starting a new project...")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            messagebox.showinfo("File Open", f"Opened: {file_path}")

    def show_about(self):
        about_text = """
        HIT137 Assignment 3 - AI Model GUI
        Created by: Group X
        Uses Hugging Face models via transformers/diffusers
        """
        messagebox.showinfo("About", about_text)

    def select_model(self, model_name):
        self.current_model = self.model_selector.get_model(model_name)
        if self.current_model:
            self.model_dropdown.set(model_name)
            self.log(f"Model selected: {model_name}")
        else:
            messagebox.showerror("Error", f"Model '{model_name}' not found.")

    def create_widgets(self):
        # === TOP FRAME: Model Selection ===
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(top_frame, text="Model Selection:").pack(side="left")

        self.model_var = tk.StringVar(value="Text-to-Image")
        self.model_dropdown = ttk.Combobox(
            top_frame,
            textvariable=self.model_var,
            values=["Text-to-Image", "Sentiment Analysis"],
            state="readonly",
            width=20
        )
        self.model_dropdown.pack(side="left", padx=5)

        load_button = tk.Button(
            top_frame,
            text="Load Model",
            command=self.load_model,
            bg="#4CAF50",
            fg="white"
        )
        load_button.pack(side="right")

        # === USER INPUT SECTION ===
        input_frame = tk.Frame(self, relief="solid", bd=1)
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Radio Buttons
        input_type_frame = tk.Frame(input_frame)
        input_type_frame.pack(pady=5)

        self.input_type = tk.StringVar(value="Text")
        tk.Radiobutton(input_type_frame, text="Text", variable=self.input_type, value="Text").pack(side="left")
        tk.Radiobutton(input_type_frame, text="Image", variable=self.input_type, value="Image").pack(side="left")

        browse_button = tk.Button(input_type_frame, text="Browse", command=self.browse_file)
        browse_button.pack(side="right")

        # Text input box
        self.text_input = tk.Text(input_frame, height=6, width=50, wrap="word")
        self.text_input.pack(padx=10, pady=5)

        # Run buttons
        run_frame = tk.Frame(input_frame)
        run_frame.pack(pady=5)

        tk.Button(run_frame, text="Run Model 1", command=self.run_model_1).pack(side="left", padx=5)
        tk.Button(run_frame, text="Run Model 2", command=self.run_model_2).pack(side="left", padx=5)

        # === MODEL OUTPUT SECTION ===
        output_frame = tk.Frame(self, relief="solid", bd=1)
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(output_frame, text="Output Display:").pack(pady=5)

        self.output_display = OutputDisplay(output_frame)
        self.output_display.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # === MODEL INFO & EXPLANATION ===
        info_frame = tk.Frame(self)
        info_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(info_frame, text="Model Information & Explanation", font=("Arial", 12, "bold")).pack()

        # Left Column: Model Info
        left_col = tk.Frame(info_frame)
        left_col.pack(side="left", padx=10, pady=5)

        tk.Label(left_col, text="Selected Model Info:", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(left_col, text="• Model Name").pack(anchor="w", pady=2)
        tk.Label(left_col, text="• Category (Text, Vision, Audio)").pack(anchor="w", pady=2)
        tk.Label(left_col, text="• Short Description").pack(anchor="w", pady=2)

        # Right Column: OOP Concepts
        right_col = tk.Frame(info_frame)
        right_col.pack(side="right", padx=10, pady=5)

        tk.Label(right_col, text="OOP Concepts Explanation:", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(right_col, text="• Where Multiple Inheritance was applied").pack(anchor="w", pady=2)
        tk.Label(right_col, text="• Why Encapsulation was applied").pack(anchor="w", pady=2)
        tk.Label(right_col, text="• How Polymorphism and Method Overriding are shown").pack(anchor="w", pady=2)
        tk.Label(right_col, text="• Where Multiple Decorators are applied").pack(anchor="w", pady=2)

        # === NOTES SECTION ===
        notes_frame = tk.Frame(self)
        notes_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(notes_frame, text="Notes: Extra notes, instructions, or references.").pack()

    @log_action
    def load_model(self):
        if not self.current_model:
            self.current_model = self.model_selector.get_model(self.model_var.get())
        if self.current_model:
            self.log(f"Model loaded: {self.model_var.get()}")
            messagebox.showinfo("Success", f"Model '{self.model_var.get()}' loaded.")
        else:
            messagebox.showerror("Error", "Failed to load model.")

    @log_action
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file_path:
            self.text_input.delete(1.0, tk.END)
            self.text_input.insert(tk.END, f"Image loaded: {file_path}")

    @log_action
    def run_model_1(self):
        if not self.current_model:
            messagebox.showwarning("Warning", "Please load a model first.")
            return

        input_data = self.text_input.get(1.0, tk.END).strip()
        if not input_data:
            messagebox.showwarning("Warning", "Please enter input data.")
            return

        try:
            if isinstance(self.current_model, TextToImageModel):
                output_path = self.current_model.generate(input_data)
                self.output_display.display_image(output_path)
            elif isinstance(self.current_model, SentimentModel):
                result = self.current_model.analyze(input_data)
                display_text = f"Sentiment: {result['label']} (Confidence: {result['score']:.4f})"
                self.output_display.display_text(display_text)
        except Exception as e:
            messagebox.showerror("Error", f"Model failed: {str(e)}")

    @log_action
    def run_model_2(self):
        messagebox.showinfo("Info", "Model 2 is not implemented in this version. Use Run Model 1.")


# =============================================
# Main Entry Point
# =============================================
if __name__ == "__main__":
    app = AIAppGUI()
    app.mainloop()