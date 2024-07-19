from src.clients.chat_client import ChatClient
from src.common.models import ClientSettings

if __name__ == "__main__":
    settings = ClientSettings()
    client = ChatClient(settings)
    client.run()