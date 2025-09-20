from models.text_to_image_model import TextToImageModel
from models.sentiment_model import SentimentModel

class ModelSelector:  # ← MUST be exactly this name
    def __init__(self):
        self.models = {
            "Text-to-Image": TextToImageModel(),
            "Sentiment Analysis": SentimentModel()
        }

    def get_model(self, model_name):
        return self.models.get(model_name)