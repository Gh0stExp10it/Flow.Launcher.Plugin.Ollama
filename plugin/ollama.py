import sys
import logging
import requests
from flox import Flox
from ollama import Client as OllamaClient, ResponseError as OllamaResponseError

class Ollama(Flox):
    def __init__(self):
        self.ollama_host = self.settings.get("ollama_host")
        self.ollama_model = self.settings.get("ollama_model")
        self.prompt_stop = self.settings.get("prompt_stop")
        self.log_level = self.settings.get("log_level")
        self.logger_level(self.log_level)
        
    def hello_world(self, flag: bool):
        logging.critical(f"Hello World!")
        logging.critical(f"Model: {self.ollama_model}")
        
        if flag:
            return "Hello World!"
        else:
            return "Flag is not set!"
           
    def query(self, query: str) -> None:
        if not self.ollama_host:
            self.add_item(
                title="Unable to load Ollama",
                subtitle=(
                    "Please enter a valid URL - e.g. http://localhost:11434"
                ),
            )
            return
        else:
            self.add_item(
                title="Result",
                subtitle=f"Answer: {self.hw(True)}",
                method=self.hw(True),
                parameters=["answer"],
            )

        return

if __name__ == "__main__":
    Ollama().run()
