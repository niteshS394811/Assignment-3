from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import os

class TextToImageModel:
    def __init__(self):
        self.model_id = "nota-ai/bk-sdm-small"
        self.pipe = None
        self.load_model()

    def load_model(self):
        print("⏳ Loading Text-to-Image model...")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float32
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = self.pipe.to(device)
        print(f"✅ Model loaded on {device.upper()}")

    def generate(self, prompt: str, output_path: str = "output.png") -> str:
        print(f"🎨 Generating image for: {prompt}")
        image = self.pipe(prompt).images[0]
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        image.save(output_path)
        return output_path