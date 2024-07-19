import socket
import struct
import threading

from src.common.errors import MessageDecodeError, ConnectionClosedError, RecivingMessageError
from src.common.models import Message, ClientSettings


class ChatClient:
    def __init__(self, settings: ClientSettings):
        self.settings = settings
        self.client_socket: socket.socket = socket.socket(settings.address_family, settings.socket_type)
        self.client_socket.connect((settings.host, settings.port))
        self.username = input("Enter your username: ")
        self.send_message(f"{self.username} has joined the chat.")

    def send_message(self, content: str) -> None:
        message = Message(username=self.username, content=content)
        self.client_socket.send(message.encode())

    def _decode_message(self) -> Message:
        message_header = self.client_socket.recv(self.settings.message_content_length)
        if not len(message_header):
            raise ConnectionClosedError()
        message_length = struct.unpack(self.settings.message_format, message_header)[0]
        message_data = self.client_socket.recv(message_length)
        try:
            return Message.decode(message_data)
        except struct.error as e:
            raise MessageDecodeError(f"Failed to decode message: {e}")

    def receive_message(self) -> None:
        while True:
            try:
                message = self._decode_message()
                if message is None:
                    break
                print(message.formatted)
            except Exception as e:
                raise RecivingMessageError(e)

    def run(self) -> None:
        receive_thread: threading.Thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        while True:
            message_content: str = input(f"{self.username} | ")
            if message_content.lower() == 'bye':
                break
            self.send_message(message_content)

        self.client_socket.close()
