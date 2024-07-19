from src.clients.ai_chat_client import AIChatClient
from src.common.models import ServerSettings, AiClientSettings

if __name__ == "__main__":
    settings = AiClientSettings()
    server = AIChatClient(settings)
    server.run()
