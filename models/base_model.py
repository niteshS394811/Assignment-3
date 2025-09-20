from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for all AI models"""
    
    def __init__(self, model_name, category, description):
        self._model_name = model_name
        self._category = category
        self._description = description
        self._is_loaded = False
    
    @abstractmethod
    def load_model(self):
        """Load the model - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def predict(self, input_data):
        """Make prediction - must be implemented by subclasses"""
        pass
    
    def get_model_info(self):
        """Get model information"""
        return {
            "Model Name": self._model_name,
            "Category": self._category,
            "Description": self._description,
            "Status": "Loaded" if self._is_loaded else "Not Loaded"
        }
    
    @abstractmethod
    def get_usage_example(self):
        """Get usage example - must be implemented by subclasses"""
        pass
    
    @property
    def is_loaded(self):
        return self._is_loaded