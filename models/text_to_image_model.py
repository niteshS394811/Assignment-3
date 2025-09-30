from diffusers import StableDiffusionPipeline
import torch
import os
import time

class TextToImageModel:
    def __init__(self):
        self.model_name = "nota-ai/bk-sdm-small"
        self.category = "Image Generation"
        self.description = "Generates images from text prompts"
        self.pipe = None
        self.is_loaded = False

    def load_model(self):
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_name,
                torch_dtype=torch.float32,
                safety_checker=None
            )
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.pipe = self.pipe.to(device)
            self.is_loaded = True
            return True
        except Exception:
            return False

    def predict(self, input_data):
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Click 'Load Model' first.")
        image = self.pipe(input_data).images[0]
        output_path = f"output_{int(time.time())}.png"
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        image.save(output_path)
        return output_path

    def get_usage_example(self):
        return "Enter text like 'a cute puppy wearing sunglasses'"