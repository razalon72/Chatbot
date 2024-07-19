from src.common.models import ServerSettings
from src.server.Server import ChatServer

if __name__ == "__main__":
    settings = ServerSettings()
    server = ChatServer(settings)
    server.run()
