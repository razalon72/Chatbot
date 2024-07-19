from src.common.models import ServerSettings
from src.server.chat_server import ChatServer

if __name__ == "__main__":
    settings = ServerSettings()
    server = ChatServer(settings)
    server.run()
