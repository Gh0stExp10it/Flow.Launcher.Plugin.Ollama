import sys
import logging
from flox import Flox
from ollama import Client as OllamaClient, ResponseError as OllamaResponseError

class Ollama(Flox):
    def __init__(self):
        self.ollama_host = self.settings.get("ollama_host")
        self.ollama_model = self.settings.get("ollama_model")
        self.prompt_stop = self.settings.get("prompt_stop")
        self.log_level = self.settings.get("log_level")
        self.logger_level(self.log_level)
        
    def hello_world(self):
        logging.critical(f"Hello World!")
        logging.critical(f"Model: {self.ollama_model}")

if __name__ == "__main__":
    Ollama()
