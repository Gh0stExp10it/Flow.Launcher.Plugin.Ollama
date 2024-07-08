from pyflowlauncher import Plugin, Result, Method, api as API
from pyflowlauncher.result import ResultResponse
from datetime import datetime
from .ollama import Ollama

class Query(Method):
    def __init__(self, plugin: Plugin) -> None:
        super().__init__()
        self.plugin = plugin

        self.ollama_host = self.plugin.settings.get("ollama_host")
        self.ollama_model = self.plugin.settings.get("ollama_model")
        self.pull_model = self.plugin.settings.get("pull_model")
        self.prompt_stop = self.plugin.settings.get("prompt_stop")
        self.save_response = self.plugin.settings.get("save_response")
        self.log_level = self.plugin.settings.get("log_level")

        if self.log_level:
            self.plugin._logger.setLevel(self.log_level)
    
    def __call__(self, query: str) -> ResultResponse:
        try:
            if query.endswith(self.prompt_stop):
                if self.ollama_host:
                    ollama_client = Ollama(ollama_host=self.ollama_host,
                                           ollama_model=self.ollama_model)
                    
                    timestamp = datetime.now()
                    model_exists = ollama_client.check_model(pull_model=self.pull_model)
                    
                    if model_exists:                      
                        # Send query to Ollama and ensure that the prompt_stop characters are removed
                        chat_response, chat_duration = ollama_client.chat(query=query[:-len(self.prompt_stop)])
                        
                        title_clipboard = f"Copy Response to Clipboard"
                        message_clipboard = f"{ollama_client.shorten(string=chat_response, length=30)}"
                        json_rpc_action_clipboard = API.copy_to_clipboard(text=chat_response)
                    else:
                        title_clipboard = f"ERROR"
                        json_rpc_action_clipboard = API.open_url(self.plugin.manifest().get("Website"))
                        
                        if not self.pull_model:
                            message_clipboard = f"Error: The specified model <{self.ollama_model}> does not exist and is not allowed to be pulled automatically - please check your configuration!"
                        else:
                            message_clipboard = f"Error: The specified model <{self.ollama_model}> does not exist and could not be pulled automatically - please check your configuration!"
                    
                    if self.save_response and chat_response and chat_duration:
                        absolute_filename = ollama_client.save_file(query=query,
                                                                    response=chat_response,
                                                                    timestamp=timestamp,
                                                                    duration=chat_duration)
                        
                        title_file = f"Open Chat in Editor"
                        message_file = f"Just select the Entry, file will be opened automatically"
                        json_rpc_action_file = API.shell_run(command=f"start {absolute_filename}",
                                                             filename= "cmd.exe")
                    else:
                        title_file = f"ERROR"
                        message_file = f"Error: Can't write and open file - please check your configuration!"
                        json_rpc_action_file = API.open_url(self.plugin.manifest().get("Website"))
                    
                    self.add_result(Result(
                        Title=title_clipboard,
                        SubTitle=message_clipboard,
                        JsonRPCAction=json_rpc_action_clipboard,
                        IcoPath=self.plugin.manifest().get("IcoPath")
                    ))
                    
                    self.add_result(Result(
                        Title=title_file,
                        SubTitle=message_file,
                        JsonRPCAction=json_rpc_action_file,
                        IcoPath=self.plugin.manifest().get("IcoPath")
                    ))
                else:
                    title = f"ERROR"
                    message = f"Error: Cant identify Ollama host <{self.ollama_host}>"
                    json_rpc_action = API.open_url(self.plugin.manifest().get("Website"))
                
                    self.add_result(Result(
                        Title=title,
                        SubTitle=message,
                        JsonRPCAction=json_rpc_action,
                        IcoPath=self.plugin.manifest().get("IcoPath")
                    ))
            else:
                title = f"To start Ollama, enter your prompt and end it with {self.prompt_stop}"
                message = f"Current model: {self.ollama_model}"
                json_rpc_action = None
                
                self.add_result(Result(
                    Title=title,
                    SubTitle=message,
                    JsonRPCAction=json_rpc_action,
                    IcoPath=self.plugin.manifest().get("IcoPath")
                ))
        except Exception as e:
            self._logger.error(e)
        
        return self.return_results()
