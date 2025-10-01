from models.text_to_image_model import TextToImageModel
from models.sentiment_model import SentimentModel

class ModelSelector:
    """Handles the selection and instantiation of model objects."""
    def __init__(self):
        # Instantiating the models here establishes Composition
        self.models = {
            "Text-to-Image": TextToImageModel(),
            "Sentiment Analysis": SentimentModel()
        }

    def get_model(self, model_name):
        return self.models.get(model_name)