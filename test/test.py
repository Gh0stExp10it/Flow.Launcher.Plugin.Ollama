import sys
import os
parent_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))
sys.path.append(os.path.join(parent_folder_path, 'test'))

from plugin.ollama import Ollama

def test_ollama(ollama_host, ollama_model, pull_model, prompt_stop, query):
    ollama_client = Ollama(ollama_host=ollama_host,
                           ollama_model=ollama_model)
    
    model_exists = ollama_client.check_model(pull_model=pull_model)
    
    if model_exists:
        chat_response, chat_duration = ollama_client.chat(query=query[:-len(prompt_stop)])
        
        print(f"Response: {chat_response}")
        print(f"Duration: {chat_duration}")
    else:
        print(f"Error: LLM {ollama_model} does not exist")
    
if __name__ == "__main__":
    # Local variables
    ollama_host     = "http://localhost:11434/"
    ollama_model    = "llama3.2:1b"
    pull_model      = False
    prompt_stop     = "||"
    query           = "Why is the sky blue? ||"
    
    # Test Ollama-API
    test_ollama(ollama_host=ollama_host,
                ollama_model=ollama_model,
                pull_model=pull_model,
                prompt_stop=prompt_stop,
                query=query)
