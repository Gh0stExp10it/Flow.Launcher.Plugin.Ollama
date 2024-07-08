# Flow Launcher Plugin - Ollama
This Flow Launcher Plugin allows you to interact with a local Ollama instance and your favorite and private LLMs (e.g. Llama 3, Gemma 2, Phi-3, TinyLlama, ...). It provides a convenient way to access the power of these language models directly from Flow Launcher.
The plugin offers two interaction options, copying the answer directly to the clipboard and writing the conversation (question + response) to a text file, which can be opened directly via the plugin.

![Plugin Example](./Images/plugin-example.gif)

## Prerequisites
To be able to communicate with a local LLM and use this plugin, you need a running Ollama instance (server). There are two different installation variants here, which you can also select depending on the underlying OS:
1. Installation via Docker (OS independent)
    - Go to [Install Docker Engine](https://docs.docker.com/engine/install/) and follow the installation instructions
    - Pull the [Ollama Image](https://hub.docker.com/r/ollama/ollama) and start the Container
    - Optional: If the container and the Large Language Model are to be operated using a graphics card, follow the next steps
        - Download and installation of the [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
        - Download and Installation of the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
        - Here is an example of a Docker-Compose that you can use to deploy Ollama with an NVIDIA graphics card:
            ```yaml
            ---
            services:
            ollama:
                image: ollama/ollama:latest
                container_name: ollama
                ports:
                  - "11434:11434"
                restart: always
                volumes:
                  - $HOME/.ollama:/root/.ollama
                deploy:
                resources:
                    reservations:
                    devices:
                        - driver: nvidia
                        count: 1
                        capabilities: [gpu]
            ```
2. Direct installation OS
    - Go to [Ollama Download](https://ollama.com/download) and select your operating system
    - Follow the installation instructions and then ensure that the instance is running

## Installation
1. Download and install [Flow Launcher](https://www.flowlauncher.com/).
2. Open the Flow Launcher settings
3. Go to the **Plugin Store** tab
4. Search for **'Ollama'**
5. Click and Install **Ollama**
6. Flow Launcher should restart automatically. If not, restart Flow Launcher manually
7. Re-open the Flow Launcher settings and head to the **Plugins** tab
8. Customize the [Settings](#settings) according to your configuration
9. Run the **'Save Settings'** command in Flow Launcher

## Settings
|Setting|Default|Description|
|---|---|---|
|Ollama Host|http://localhost:11434|URL of the local Ollama instance to communicate via API.|
|Ollama Model|tinyllama:1.1b|The LLM to be used ([Ollama model library](https://ollama.com/library)).|
|Automatic Model Download|[ ] - *false*|Download LLM automatically if not already installed.<br>*Be careful - the download may take some time and storage on your disk*.|
|Save Chat to File|[x] - *true*|Should the chat be saved as a text file? This allows it to be opened directly in a text editor.|
|Prompt Stop|&#124;&#124;|Characters to indicate end of prompt. This saves computing time, as otherwise the LLM is executed every time a key is pressed.|
|Log Level|ERROR|The Log Level can be adjusted for error analysis. Normally not of interest for users.|
