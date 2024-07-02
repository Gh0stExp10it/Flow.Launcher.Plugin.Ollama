import logging
import pyperclip
from ollama import Client as OllamaClient, ResponseError as OllamaResponseError

class Ollama:
    def __init__(self, ollama_host, ollama_model):
        """
        Initializes an Ollama client object.

        Args:
            * ollama_host (str): The hostname or IP address of the Ollama server.
            * ollama_model (str): The name of the Ollama model to use for communication.
        """
        self.ollama_host = ollama_host
        self.ollama_model = ollama_model
        self.initialized = False
            
    def initialize(self):
        """
        Establishes a connection to the Ollama server.

        Args:
            * self (object): Reference to the current object instance.
        """
        if not self.initialized:
            # Initialize connection to InfluxDB
            self.ollama_client = OllamaClient(host=self.ollama_host)
            self.initialized = True
            logging.info("Ollama-Client initialized.")
        
    def check_model(self, pull_model):
        """
        Checks if the specified Ollama model exists and attempts to download it if not.
        
        Args:
            * self (object): Reference to the current object instance.
            * pull_model (bool, optional): A flag indicating whether to automatically download the model if it's not found. Defaults to False.

        Returns:
            * bool: True if the model exists and can be communicated with, False otherwise.
        """
        self.initialize()
        
        try:
            self.ollama_client.chat(self.ollama_model)
            logging.info(f"LLM/Model '{self.ollama_model}' exists, no download required!")
            return True
        except OllamaResponseError as e:
            logging.error(f"Error: <{e.status_code}> - {e.error}")
            
            if e.status_code == 404:
                if pull_model:
                    logging.info(f"The model '{self.ollama_model}' will now be downloaded automatically!!")
                    self.ollama_client.pull(self.ollama_model)
                    return True
                else:
                    logging.error(f"The model cannot be pulled if the automatic download has not been configured by the user!")
                    return False
            else:
                return False
    
    def chat(self):
        """
        Sends the requested chat message to the Ollama model and retrieves the response.

        Args:
            * self (object): Reference to the current object instance.
            * message (str, optional): The message to send to the model. Defaults to "Whats 1 plus 1?".

        Returns:
            * str: The response content from the model, or None if an error occurs.
        """
        try:
            response = self.ollama_client.chat(model=self.ollama_model, messages=[
                {
                    'role': 'user',
                    'content': 'Whats 1 plus 1?',
                },
            ])
        
            if isinstance(response, dict):
                # logging.critical(f"RESPONSE: {response['message']['content']}")
                return response['message']['content']
        except OllamaResponseError as e:
                logging.critical(f"Error: <{e.status_code}> - {e.error}")

    def clipboard_copy(self, response: str) -> None:
        """
        Copies the provided response text to the clipboard.

        Args:
            * self (object): Reference to the current object instance.
        """
        pyperclip.copy(response)
