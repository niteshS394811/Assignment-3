import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import os

# Import core components
from gui.model_selector import ModelSelector
from models.base_model import BaseModel 

class AIModelGUI:
    """
    Main Tkinter application class handling the GUI layout, model interaction,
    and display logic.
    """
    def __init__(self, root):
        self._root = root
        self._setup_window()
        self._model_selector = ModelSelector()
        self._current_model: BaseModel = None
        self._uploaded_file = None
        self._create_widgets()
        
    def _setup_window(self):
        """Sets up the main window properties and custom button styles."""
        self._root.title("HIT137 Assignment 3 - AI Model GUI")
        self._root.geometry("1100x750") 
        self._root.resizable(True, True)
        
        # Define custom styles for colored buttons
        style = ttk.Style()
        style.theme_use('clam')
        # Green for Run Model
        style.configure('G.TButton', background='#4CAF50', foreground='black', font=('Arial', 10, 'bold')) 
        style.map('G.TButton', background=[('active', '#66BB6A')])
        # Red for Clear All
        style.configure('R.TButton', background='#F44336', foreground='white', font=('Arial', 10, 'bold'))  
        style.map('R.TButton', background=[('active', '#E57373')])
        
    def _create_widgets(self):
        """Builds the overall application layout."""
        self._create_menu()
        self._create_model_selection()
        
        # Main container for Input (Left) and Output (Right)
        main_content = ttk.PanedWindow(self._root, orient=tk.HORIZONTAL)
        main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side: User Input (30% width)
        self._input_frame = self._create_input_section(main_content)
        main_content.add(self._input_frame, weight=30) 
        
        # Right side: Output (70% width)
        self._output_frame = self._create_output_section(main_content)
        main_content.add(self._output_frame, weight=70) 
        
        # FIX: Explicitly set the initial sash position to 30% of the 1100px width (330px).
        # This ensures the 30% width is applied immediately upon launch.
        self._root.update_idletasks() # Ensures geometry is calculated
        main_content.sashpos(0, 330)
        
        # Bottom section: Model Information and OOP Explanation
        self._create_info_section()
        self._on_model_selected() # Initialize info display on startup
        
    def _create_menu(self):
        """Creates the File menu."""
        menubar = tk.Menu(self._root)
        self._root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self._root.quit)
        
    def _create_model_selection(self):
        """Creates the model selection dropdown and Load button."""
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
        
    def _create_input_section(self, parent):
        """Creates the User Input section (Left Column - 30%)."""
        input_frame = ttk.LabelFrame(parent, text="Text Input Prompt", padding="10")
        
        # Only text input is supported in this final version
        self._input_type = tk.StringVar(value="text") 
        
        # ScrolledText area for user input. Decreased height from 15 to 8.
        self._input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD) 
        self._input_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Action Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Run Button (Green)
        ttk.Button(btn_frame, text="Run Model", command=self._run_model, 
                   style='G.TButton').pack(side=tk.LEFT, padx=5, expand=True)
        
        # Clear Button (Red)
        ttk.Button(btn_frame, text="Clear All", command=self._clear_all, 
                   style='R.TButton').pack(side=tk.LEFT, padx=5, expand=True)
        
        return input_frame
        
    def _create_output_section(self, parent):
        """Creates the Output section (Right Column - 70%)."""
        output_frame = ttk.LabelFrame(parent, text="Model Output", padding="10")
        
        self._output_container = ttk.Frame(output_frame)
        self._output_container.pack(fill=tk.BOTH, expand=True)
        
        # Text output area
        self._output_text = scrolledtext.ScrolledText(self._output_container, height=10, wrap=tk.WORD)
        self._output_text.pack(fill=tk.BOTH, expand=True)
        
        # Image output label (for Text-to-Image results)
        self._output_image_label = tk.Label(self._output_container)
        
        return output_frame
        
    def _create_info_section(self):
        """Creates the Model Information and OOP Explanation section (Bottom Row)."""
        info_frame = ttk.LabelFrame(self._root, text="OOP Explanation & Info Reference", padding="10")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self._info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, height=10, font=("Arial", 9))
        self._info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def _on_model_selected(self, event=None):
        """Updates the information panel when a new model is selected."""
        self._update_info_display()
            
    def _load_model(self):
        """
        Loads the selected model instance using the ModelSelector factory.
        Demonstrates Polymorphism by interacting with the BaseModel interface.
        """
        model_name = self._model_var.get()
        if not model_name:
            messagebox.showwarning("Warning", "Please select a model")
            return
            
        try:
            # Polymorphism: get_model returns an object implementing BaseModel
            self._current_model = self._model_selector.get_model(model_name) 
            if self._current_model is None:
                messagebox.showerror("Error", "Model not found")
                return
                
            self._output_text.insert(tk.END, f"Loading {model_name}...\n")
            self._root.update()
            
            # Polymorphism: Calls the correct load_model() implementation
            if self._current_model.load_model(): 
                self._output_text.insert(tk.END, f"✅ {model_name} loaded successfully!\n\n")
            else:
                self._output_text.insert(tk.END, f"❌ Failed to load {model_name}. Check console for errors.\n\n")
                self._current_model = None
        except Exception as e:
            messagebox.showerror("Error", f"Error loading model: {str(e)}")
            self._current_model = None
            
    def _run_model(self):
        """
        Runs the currently loaded model with the input prompt.
        Demonstrates Polymorphism by calling the predict method.
        """
        if not self._current_model:
            messagebox.showwarning("Warning", "Please load a model first")
            return
            
        input_data = self._get_input_data()
        if input_data is None:
            return
            
        try:
            self._output_text.insert(tk.END, "Running model...\n")
            self._root.update()
            
            # Polymorphism: Calls the correct predict() implementation
            result = self._current_model.predict(input_data) 
            self._display_result(result)
        except Exception as e:
            messagebox.showerror("Error", f"Error running model: {str(e)}")
            
    def _get_input_data(self):
        """Retrieves the text input from the prompt box."""
        text = self._input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter text")
            return None
        return text
            
    def _display_result(self, result):
        """Displays the result, handling both text and generated images."""
        self._output_text.delete(1.0, tk.END)
        self._output_image_label.pack_forget()
        self._output_text.pack_forget()
        
        if isinstance(result, str) and result.endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(result)
                img.thumbnail((450, 450)) 
                photo = ImageTk.PhotoImage(img)
                self._output_image_label.config(image=photo)
                self._output_image_label.image = photo
                
                # Image at the top, text below for file path/confirmation
                self._output_image_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                self._output_text.pack(fill=tk.X)
                self._output_text.insert(tk.END, f"✅ Image generated and saved!\nFile: {result}")
            except Exception as e:
                self._output_text.pack(fill=tk.BOTH, expand=True)
                self._output_text.insert(tk.END, f"❌ Image error: Could not display image: {str(e)}")
        else:
            # Display text result only
            self._output_text.pack(fill=tk.BOTH, expand=True)
            self._output_text.insert(tk.END, f"Result:\n{result}\n{'-'*40}\n")
            
        self._output_text.see(tk.END)
        
    def _update_info_display(self):
        """Populates the bottom information panel with model details and OOP explanations."""
        model_name = self._model_var.get()
        
        temp_model = self._model_selector.get_model(model_name)
        if not temp_model:
            model_info = {"Model Name": "N/A", "Category": "N/A", "Description": "N/A"}
            usage_example = "N/A"
        else:
            model_info = temp_model.get_model_info()
            usage_example = temp_model.get_usage_example()
            
        info = f"""
*** MODEL INFORMATION ***
• Model Name: {model_info.get('Model Name')}
• Category: {model_info.get('Category')}
• Short Description: {model_info.get('Description')}
• Usage Example: {usage_example}

*** OOP CONCEPTS EXPLANATION ***
• Encapsulation: Applied by using **private-like attributes** (prefixed with `_`, e.g., `self._is_loaded` in BaseModel, `self._root` in GUI) to manage internal state and control access via public methods (e.g., `get_model_info()`).

• Polymorphism & Method Overriding: The `AIModelGUI` interacts with all models through a common interface defined by the **BaseModel** abstract class. Each concrete model (**SentimentModel**, **TextToImageModel**) implements its own specific logic in methods like `load_model()` and `predict()`, formally **overriding** the abstract base methods.

• Multiple Inheritance: Used in the **TextToImageModel** class, which inherits from **BaseModel** and the **TimingMixin** class, allowing it to inherit core model functionality and timing utilities.

• Multiple Decorators: Applied to the **SentimentModel.predict()** method, using both **@log_action** and **@measure_time** to log function calls and execution duration simultaneously.
"""
        self._info_text.delete(1.0, tk.END)
        self._info_text.insert(tk.END, info)
        
    def _clear_all(self):
        """Clears all input and output fields."""
        self._input_text.delete(1.0, tk.END)
        self._output_text.delete(1.0, tk.END)
        self._output_image_label.pack_forget()
        self._output_text.pack(fill=tk.BOTH, expand=True)
        self._uploaded_file = None 
        self._input_type.set("text") 
