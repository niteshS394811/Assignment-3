from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.classifier = None
        self.load_model()

    def load_model(self):
        print("⏳ Loading Sentiment Analysis model...")
        self.classifier = pipeline("sentiment-analysis", model=self.model_name)
        print("✅ Model loaded successfully")

    def analyze(self, text: str) -> dict:
        print(f"🔍 Analyzing: {text}")
        result = self.classifier(text)[0]
        label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        result["label"] = label_map.get(result["label"], result["label"])
        return result