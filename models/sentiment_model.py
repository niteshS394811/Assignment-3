from transformers import pipeline

class SentimentModel:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.category = "Text Classification"
        self.description = "Classifies text sentiment as Positive/Neutral/Negative"
        self.classifier = None
        self.is_loaded = False

    def load_model(self):
        try:
            self.classifier = pipeline("sentiment-analysis", model=self.model_name)
            self.is_loaded = True
            return True
        except Exception:
            return False

    def predict(self, input_data):
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Click 'Load Model' first.")
        result = self.classifier(input_data)[0]
        label_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        result["label"] = label_map.get(result["label"], result["label"])
        return f"Sentiment: {result['label']} (Confidence: {result['score']:.4f})"

    def get_usage_example(self):
        return "Enter text like 'I love this course!'"