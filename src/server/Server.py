import socket
import struct

import select
import structlog

from src.common.errors import ConnectionAcceptError, MessageReceiveError, ServerOperationError
from src.common.models import Message, ServerSettings

ENABLE_SET_SOCKET = 1

logger = structlog.get_logger()


class ChatServer:
    def __init__(self, settings: ServerSettings):
        self.settings = settings
        self.server_socket: socket.socket = socket.socket(settings.address_family, settings.socket_type)
        self.server_socket.setsockopt(settings.socket_level, settings.refuse_local, ENABLE_SET_SOCKET)
        self.server_socket.bind((settings.host, settings.port))
        self.server_socket.listen(settings.max_queue_connections)
        self.sockets_list = [self.server_socket]
        self.clients = {}
        logger.info(f"Chat server started on {settings.host}:{settings.port}")

    def send_broadcast(self, message: Message, sender_socket: socket.socket) -> None:
        encoded_message = message.encode()
        for client_socket in self.clients:
            if client_socket != sender_socket:
                client_socket.send(encoded_message)

    def handle_new_connection(self) -> None:
        client_socket, client_address = self.server_socket.accept()
        try:
            message_header = client_socket.recv(self.settings.message_content_length)
            if not len(message_header):
                raise ConnectionAcceptError("Failed to receive message header from new connection.")
            message_length = struct.unpack(self.settings.message_format, message_header)[0]
            message_data = client_socket.recv(message_length)
            message = Message.decode(message_data)

            self.sockets_list.append(client_socket)
            self.clients[client_socket] = {"username": message.username}

            logger.info(
                f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{message.username}")
            self.send_broadcast(Message(username="Server", content=f"{message.username} joined the chat."),
                                client_socket)
        except (socket.error, ConnectionResetError) as e:
            client_socket.close()
            raise ConnectionAcceptError(f"Error handling new connection: {e}")

    def handle_client_message(self, notified_socket: socket.socket) -> None:
        try:
            message_header = notified_socket.recv(self.settings.message_content_length)
            if not len(message_header):
                logger.info(f"Closed connection from {self.clients[notified_socket]['username']}")
                self.remove_client(notified_socket)
                return

            message_length = struct.unpack(self.settings.message_format, message_header)[0]
            message_data = notified_socket.recv(message_length)
            message = Message.decode(message_data)

            sender_username = self.clients[notified_socket]['username']
            logger.info(f"Received message from {sender_username}: {message.content}")

            self.send_broadcast(Message(username=sender_username, content=message.content), notified_socket)
        except (socket.error, ConnectionResetError) as e:
            self.remove_client(notified_socket)
        except Exception as e:
            raise MessageReceiveError(e)

    def remove_client(self, client_socket: socket.socket) -> None:
        username = self.clients[client_socket]['username']
        self.sockets_list.remove(client_socket)
        del self.clients[client_socket]
        client_socket.close()
        logger.info(f"{username} left the chat.")
        self.send_broadcast(Message(username="Server", content=f"{username} left the chat."), client_socket)

    def run(self) -> None:
        while True:
            try:
                read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

                for notified_socket in read_sockets:
                    if notified_socket == self.server_socket:
                        self.handle_new_connection()
                    else:
                        self.handle_client_message(notified_socket)

                for notified_socket in exception_sockets:
                    self.remove_client(notified_socket)
            except Exception as e:
                raise ServerOperationError(e)
