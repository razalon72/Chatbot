import struct
from socket import SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR

import openai
from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 12345
    socket_type: int = SOCK_STREAM  # indicate TCP socket
    address_family: int = AF_INET  # indicates we are using IPv4
    message_format: str = '!I'
    message_content_length: int = 4


class ServerSettings(Settings):
    max_queue_connections: int = 5
    socket_level = SOL_SOCKET
    refuse_local = SO_REUSEADDR  # Allow reuse of local addresses


class ClientSettings(Settings):
    pass


class AiClientSettings(ClientSettings):
    max_tokens: int = 150
    response_count_interval: int = 4
    periodic_response_interval: int = 20
    api_key: str = ""


class Message(BaseModel):
    username: str
    content: str

    @property
    def formatted(self) -> str:
        return f"{self.username}| {self.content}"

    def encode(self) -> bytes:
        formatted = self.formatted.encode('utf-8')
        return struct.pack('!I', len(formatted)) + formatted

    @classmethod
    def decode(cls, data: bytes) -> 'Message':
        message = data.decode('utf-8')
        username, content = message.split('|', 1)
        return cls(username=username.strip(), content=content.strip())
