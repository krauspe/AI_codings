teimport os
import requests
import json
import argparse
from datetime import datetime
from typing import Optional

# --- Configuration ---
# Set this to True if you are connecting to a remote/cloud Ollama instance
# If False, it assumes the local Ollama server is running on http://localhost:11434
IS_CLOUD_MODE = False 
DEFAULT_MODEL = "gemma4:e4b" # Change this to your desired model

class OllamaChatClient:
    """
    A client to chat with Ollama models, supporting both local and remote connections.
    """
    def __init__(self, model: str, is_cloud: bool = False, base_url: str = "http://localhost:11434"):
        self.model = model
        self.is_cloud = is_cloud
        self.base_url = base_url
        
        if self.is_cloud:
            print("⚠️ Warning: Using Cloud/Remote mode. Ensure the base_url is correct.")
        else:
            print("✅ Using Local Ollama mode.")

    def _get_api_url(self, endpoint: str) -> str:
        """Constructs the full API URL based on the connection mode."""
        if self.is_cloud:
            return f"{self.base_url}/{endpoint}"
        else:
            return f"{self.base_url}/{endpoint}"

    def generate_response(self, prompt: str, history: list) -> Optional[str]:
        """
        Sends the prompt and chat history to the Ollama API and returns the response.
        
        Args:
            prompt: The current user message.
            history: A list of previous messages (role, content).
        
        Returns:
            The model's response text, or None if an error occurred.
        """
        
        # Ollama chat API expects a list of messages
        messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        api_url = self._get_api_url("api/chat")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False # Set to True for streaming output
        }

        try:
            print(f"\n🤖 Sending request to {api_url}...")
            response = requests.post(api_url, headers=headers, json=payload, timeout=120)
            response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
            
            data = response.json()
            return data['message']['content']

        except requests.exceptions.ConnectionError:
            print("\n❌ Error: Could not connect to the Ollama server.")
            print("Please ensure Ollama is running locally, or check the 'base_url' for cloud mode.")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"\n❌ HTTP Error occurred: {e}")
            print("Check if the model name is correct and if the API endpoint is valid.")
            return None
        except requests.exceptions.Timeout:
            print("\n❌ Error: The request timed out. The model might be slow or the connection unstable.")
            return None
        except json.JSONDecodeError:
            print("\n❌ Error: Failed to decode JSON response from the server.")
            return None
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")
            return None


def chat_loop(client: OllamaChatClient, save_flag: bool, filename: Optional[str] = None):
    """
    Main interactive chat loop.
    """
    if save_flag:
        print(f"✍️ Output will be saved to: {filename}")
    
    print("\n===================================================")
    print(f"🤖 Chat initialized with model: {client.model}")
    print("Type 'quit' or 'exit' to end the chat.")
    print("=====================================================")

    # History stores the conversation context: [{"role": "user", "content": "..."}]
    conversation_history = []

    def save_to_file(content: str):
        """Helper function to append content to the specified file."""
        if save_flag and filename:
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    # Append a recognizable separator/newline for readability
                    f.write(content + "\n")
            except IOError as e:
                print(f"\n🚨 Warning: Could not write to file {filename}. Error: {e}")


    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("\n👋 Goodbye!")
            # Save a final entry when exiting
            save_to_file("--- Session ended by user ---")
            break
        
        if not user_input.strip():
            continue

        # 1. Log and update history (User input)
        save_to_file(f"[USER] {user_input}")
        conversation_history.append({"role": "user", "content": user_input})
        
        # 2. Get response from the model
        response_text = client.generate_response(user_input, conversation_history[:-1])
        
        if response_text:
            # 3. Display response
            print("\n🤖 Response:")
            print(response_text)
            
            # 4. Log response
            save_to_file(f"[AI] {response_text}")
            
            # 5. Update history (Model response)
            conversation_history.append({"role": "assistant", "content": response_text})
        else:
            # If response failed, remove the user message to prevent context corruption
            conversation_history.pop()


def get_default_filename() -> str:
    """Generates the default filename using date and time (YYYY-MM-DD_HH-MM-SS)."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")
    return f"{date_str}_{time_str}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interactive chat client for Ollama.")
    
    # Use standard add_argument for flags and options
    parser.add_argument(
        "--save", 
        action="store_true", 
        help="Enable saving the chat to a file."
    )
    parser.add_argument(
        "--save-file", 
        type=str, 
        default=None, 
        help="Specify an explicit filename for saving. If only --save is used, a default timestamp filename will be generated."
    )

    args = parser.parse_args()

    # --- Determine Save Filename ---
    save_flag = args.save
    save_filename = None
    
    if save_flag:
        if args.save_file:
            # User provided a specific filename
            save_filename = args.save_file
        else:
            # User only used --save, generate default name
            default_name = get_default_filename()
            # Construct filename: YYYY-MM-DD_HH-MM-SS.ollama.modelname.txt
            save_filename = f"{default_name}.ollama.{DEFAULT_MODEL.split(':')[0]}.txt"

    # --- Initialization Logic ---
    
    # 1. Determine connection type
    is_cloud = IS_CLOUD_MODE
    
    # 2. Determine base URL
    cloud_base_url = os.environ.get("OLLAMA_CLOUD_URL")
    
    if is_cloud and cloud_base_url:
        base_url = cloud_base_url
    elif is_cloud and not cloud_base_url:
        print("⚠️ Warning: Cloud mode is enabled but OLLAMA_CLOUD_URL environment variable is not set.")
        base_url = "http://remote-ollama-api.com" # Placeholder for actual cloud URL
    else:
        base_url = "http://localhost:11434"

    # 3. Initialize and run the chat client
    try:
        client = OllamaChatClient(
            model=DEFAULT_MODEL, 
            is_cloud=is_cloud, 
            base_url=base_url
        )
        # Pass the save flag and filename to the chat loop
        chat_loop(client, save_flag=save_flag, filename=save_filename)
    except Exception as e:
        print(f"\n[FATAL ERROR] Could not start the chat client: {e}")
