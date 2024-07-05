import logging
import pyperclip
import os
import webbrowser
from datetime import datetime, timedelta
from typing import Optional
from ollama import Client as OllamaClient, ResponseError as OllamaResponseError

class Ollama:
    def __init__(self, ollama_host, ollama_model):
        """
        Initializes an Ollama client object.

        Args:
            * self (object): Reference to the current object instance.
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
        
    def check_model(self, pull_model: bool) -> bool:
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
    
    def chat(self, query: str) -> tuple[str, int]:
        """
        Sends the requested chat message to the Ollama model and retrieves the response.

        Args:
            * self (object): Reference to the current object instance.
            * message (str, optional): The message to send to the model. Defaults to "Whats 1 plus 1?".

        Returns:
            * str: The response content from the model, or None if an error occurs.
        """
        try:
            response = self.ollama_client.chat(model=self.ollama_model,
                                               messages=[
                                                   {
                                                       "role": "user",
                                                       "content": query,
                                                    },
                                                ])

            if isinstance(response, dict):
                return response["message"]["content"], response["total_duration"]
        except OllamaResponseError as e:
                logging.error(f"Error: <{e.status_code}> - {e.error}")

    def shorten(self, string: str, length: int):
        """
        Shortens a string and adds an ellipsis (...) if it exceeds a specified length.

        Args:
            * self (object): Reference to the current object instance.
            * string: The string to be shortened.
            * length: The maximum desired length of the output string.

        Returns:
            * str: The shortened string with an ellipsis
        """
        string = string.split("\n", 1)[0]

        if len(string) > length:
            shortened_string = string[:length - 3] + "..."
        else:
            shortened_string = string

        return shortened_string

    def clipboard_copy(self, response) -> None:
        """
        Copies the provided response text to the clipboard.

        Args:
            * self (object): Reference to the current object instance.
        """
        pyperclip.copy(response)

    def save_file(self, query: str, response: str, timestamp: datetime, duration: int) -> str:
        formatted_query_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        formatted_filename_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Create a timedelta object with milliseconds and remaining microseconds
        milliseconds = duration // 1000000
        microseconds = duration % 1000000
        delta = timedelta(milliseconds=milliseconds, microseconds=microseconds)
        response_timestamp = timestamp + delta
        formatted_response_timestamp = response_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        new_content = f"[{formatted_query_timestamp}] User: {query}\n[{formatted_response_timestamp}] Ollama: {response}\n\n"
        
        filename = f"Ollama_Chat_{formatted_filename_timestamp}.txt"
        
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    existing_content = file.read()
            except PermissionError:
                logging.error(PermissionError)
        else:
            existing_content = ""
            
        new_content = new_content + existing_content
        
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(new_content)
        except PermissionError:
            logging.error(PermissionError)
            
        return filename

    def open_file(self, filename: Optional[str], response: Optional[str]) -> None:
        """
        Open the response in the default text editor. If no filename is given,
        the conversation will be written to a new text file and opened.
        """
        if filename:
            webbrowser.open(filename)
            return

        if response:
            temp_file = "temp_text.txt"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(response)
            webbrowser.open(temp_file)
            return
