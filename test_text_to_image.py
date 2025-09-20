from diffusers import StableDiffusionPipeline
import torch

# Lightweight, CPU-friendly model
model_id = "nota-ai/bk-sdm-small"

print("⏳ Loading lightweight model... (fast, ~500MB)")

try:
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32,  # ← Required for CPU
        safety_checker=None
    )
except Exception as e:
    print(f"❌ Failed to load model: {str(e)}")
    exit(1)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)
print(f"✅ Model loaded on {device.upper()}")

prompt = "a cute puppy wearing sunglasses"
print(f"🎨 Generating image for: '{prompt}'...")

try:
    image = pipe(prompt).images[0]
    image.save("test_output.png")
    print("✅ Image saved as 'test_output.png'")
    print("🎉 Success! Ready for GUI integration.")
except Exception as e:
    print(f"❌ Error: {str(e)}")