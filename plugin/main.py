from pyflowlauncher import Plugin, Result, Method, api as API
from pyflowlauncher.result import ResultResponse
from .ollama import Ollama

class Query(Method):
    def __init__(self, plugin: Plugin) -> None:
        super().__init__()
        self.plugin = plugin
        
        self.ollama_host = self.plugin.settings.get("ollama_host")
        self.ollama_model = self.plugin.settings.get("ollama_model")
        self.pull_model = self.plugin.settings.get("pull_model")
        self.prompt_stop = self.plugin.settings.get("prompt_stop")
        self.log_level = self.plugin.settings.get("log_level")
        self.plugin._logger.setLevel(self.log_level)
    
    def __call__(self, query: str) -> ResultResponse:
        try:
            if self.ollama_host:
                ollama_client = Ollama(ollama_host=self.ollama_host,
                                       ollama_model=self.ollama_model)
                
                model_exists = ollama_client.check_model(pull_model=self.pull_model)
                
                if model_exists:
                    return_val = "Model is available and already downloaded"
                    
                    chat_response = ollama_client.chat()
                    
                else:
                    return_val = "Model is not available and automatic download is set to <false>"
                
                
                JsonRPCAction = ollama_client.clipboard_copy(chat_response)
                self.add_result(Result(
                    Title="Copy Response to Clipboard",
                    # SubTitle=return_val,
                    SubTitle=("Response: " + chat_response),
                    JsonRPCAction=JsonRPCAction
                ))
            else:
                JsonRPCAction = API.open_url(self.plugin.manifest().get("Website"))
                self.add_result(Result(
                    Title="Error",
                    SubTitle="Cant identify ollama-host",
                    JsonRPCAction=JsonRPCAction
                ))
        except Exception as e:
            self._logger.error(e)
        return self.return_results()
