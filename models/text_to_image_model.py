# --- FILE: models/text_to_image_model.py ---
from diffusers import StableDiffusionPipeline
import torch
import os
import time

# Import necessary classes
from models.base_model import BaseModel
from models.mixins import TimingMixin


# Multiple Inheritance: Inherits from BaseModel (core) and TimingMixin (utility)
class TextToImageModel(BaseModel, TimingMixin):
    def __init__(self):
        # Call BaseModel constructor for Encapsulation
        super().__init__(
            model_name="nota-ai/bk-sdm-small",
            category="Image Generation",
            description="Generates images from text prompts (Stable Diffusion)"
        )
        self.pipe = None
        
    # Overrides abstract method
    def load_model(self):
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self._model_name,
                torch_dtype=torch.float32,
                safety_checker=None
            )
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.pipe = self.pipe.to(device)
            self._is_loaded = True
            return True
        except Exception as e:
            print(f"Error loading TTI model: {e}")
            return False

    # Overrides abstract method
    def predict(self, input_data):
        if not self._is_loaded:
            raise RuntimeError("Model not loaded.")
            
        print(f"Running TTI with prompt: {input_data}")
        image = self.pipe(input_data).images[0]
        output_path = f"output_{int(time.time())}.png"
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        image.save(output_path)
        
        return output_path

    # Overrides abstract method
    def get_usage_example(self):
        return "Enter text like 'a cute puppy wearing sunglasses'"