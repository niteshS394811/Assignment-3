from transformers import pipeline

# Import necessary classes and decorators
from models.base_model import BaseModel
from utils.decorators import log_action, measure_time


# Inheritance: Inherits from BaseModel
class SentimentModel(BaseModel):
    def __init__(self):
        # Call BaseModel constructor for Encapsulation
        # UPDATED: Using 'j-hartmann/emotion-english-distilroberta-base'. 
        # This is a highly stable model for 7 key emotion labels (anger, joy, sadness, etc.)
        super().__init__(
            model_name="j-hartmann/emotion-english-distilroberta-base",
            category="Text Classification (7 Emotion Labels)",
            description="Classifies text into 7 key emotion labels (e.g., anger, joy, sadness, fear, love, surprise, neutral)."
        )
        self.classifier = None
        
    # Overrides abstract method
    def load_model(self):
        try:
            # The model ID is fetched from self._model_name
            # This model is specifically compatible with the 'text-classification' pipeline.
            self.classifier = pipeline("text-classification", model=self._model_name)
            self._is_loaded = True
            return True
        except Exception as e:
            # Display the actual error message that caused the failure
            print(f"Error loading model {self._model_name}: {e}") 
            return False

    # Multiple Decorators: Apply both log_action and measure_time
    @log_action 
    @measure_time
    def predict(self, input_data): # Overrides abstract method
        if not self._is_loaded:
            raise RuntimeError("Model not loaded.")
            
        print(f"Running Sentiment Analysis on: {input_data}")
        # The model returns the most likely emotion (label) and its score
        result = self.classifier(input_data)[0] 
        
        # The model returns the human-readable emotion label (e.g., 'anger').
        emotion_label = result['label'].replace("_", " ").title()
        
        return f"Detected Emotion: {emotion_label} (Confidence: {result['score']:.4f})"

    # Overrides abstract method
    def get_usage_example(self):
        # Updated usage example to reflect the 7-emotion classification
        return "Enter text like 'I was totally surprised by the ending of that show!'"
