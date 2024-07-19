class ChatError(Exception):
    pass


class MessageDecodeError(ChatError):
    pass


class MessageProcessingError(ChatError):
    pass


class ServerOperationError(ChatError):
    def __init__(self, error):
        super().__init__(f"Error during server operation: {error}")


class ConnectionAcceptError(ChatError):
    def __init__(self, message):
        super().__init__(message)


class MessageReceiveError(ChatError):
    def __init__(self, error):
        super().__init__(f"Error handling message from client: {error}")


class ConnectionClosedError(ChatError):
    def __init__(self):
        super().__init__("Connection closed by the server :(")


class PeriodicMessageError(ChatError):
    def __init__(self, error):
        super().__init__(f"Error handling message from client: {error}")

class RecivingMessageError(ChatError):
    def __init__(self, error):
        super().__init__(f"Error receiving message: {error}")
