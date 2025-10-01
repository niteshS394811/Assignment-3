# --- FILE: models/sentiment_model.py ---
from transformers import pipeline

# Import necessary classes and decorators
from models.base_model import BaseModel
from utils.decorators import log_action, measure_time


# Inheritance: Inherits from BaseModel
class SentimentModel(BaseModel):
    def __init__(self):
        # Call BaseModel constructor for Encapsulation
        super().__init__(
            model_name="cardiffnlp/twitter-roberta-base-sentiment-latest",
            category="Text Classification",
            description="Classifies text sentiment as Positive/Neutral/Negative"
        )
        self.classifier = None
        
    # Overrides abstract method
    def load_model(self):
        try:
            self.classifier = pipeline("sentiment-analysis", model=self._model_name)
            self._is_loaded = True
            return True
        except Exception:
            return False

    # Multiple Decorators: Apply both log_action and measure_time
    @log_action 
    @measure_time
    def predict(self, input_data): # Overrides abstract method
        if not self._is_loaded:
            raise RuntimeError("Model not loaded.")
            
        print(f"Running Sentiment Analysis on: {input_data}")
        result = self.classifier(input_data)[0] 
        label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        result["label"] = label_map.get(result["label"], result["label"])
        return f"Sentiment: {result['label']} (Confidence: {result['score']:.4f})"

    # Overrides abstract method
    def get_usage_example(self):
        return "Enter text like 'I love this course!'"