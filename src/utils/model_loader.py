from utils.config_loader import load_config
import os 

class ModelLoader:
    def __init__(self, config_path: str | None = None):
        self.config = load_config(config_path)
        self.models = self.config.get("Model")
        self.provider = self.models["llm"]
        self.anthropic = self.provider["provider_1"]["model_id"]
        self.groq = self.provider["provider_2"]["model_id"]