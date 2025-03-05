import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelLoader:
    def __init__(self, model_name: str, model_dir: str):
        self.model_name = model_name
        self.model_dir = model_dir
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """Load the local LLM model and tokenizer."""
        model_path = os.path.join(self.model_dir, self.model_name)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model directory '{model_path}' does not exist.")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

    def generate_response(self, prompt: str, max_length: int = 100) -> str:
        """Generate a response from the loaded model based on the input prompt."""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model and tokenizer must be loaded before generating a response.")
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=max_length)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return response