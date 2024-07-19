import threading
import time

import openai

from src.clients.chat_client import ChatClient
from src.common.errors import PeriodicMessageError, RecivingMessageError
from src.common.models import AiClientSettings

MODEL = "text-davinci-003"


class AIChatClient(ChatClient):
    def __init__(self, settings: AiClientSettings):
        super().__init__(settings)
        self.settings = settings
        self.last_n_messages = []
        self.message_count = 0
        self.response_count_interval = settings.response_count_interval
        self.periodic_response_interval = settings.periodic_response_interval
        openai.api_key = settings.api_key
        self.periodic_message_thread = threading.Thread(target=self.send_periodic_message)
        self.periodic_message_thread.daemon = True  # Ensure this thread also exits when the main program exits
        self.periodic_message_thread.start()

    def _format_last_messages(self) -> str:
        return "\n ".join(self.last_n_messages)

    def receive_message(self) -> None:
        while True:
            try:
                message = self._decode_message()
                self.message_count += 1
                self.last_n_messages.append(message.content)
                if self.message_count >= self.response_count_interval:
                    self.generate_response(self._format_last_messages())
                    self.message_count = 0
                    self.last_n_messages = []
            except Exception as e:
                raise RecivingMessageError(e)

    def send_periodic_message(self) -> None:
        while True:
            try:
                time.sleep(self.periodic_response_interval)
                self.generate_response(self._format_last_messages())
            except Exception as e:
                raise PeriodicMessageError(e)

    def generate_response(self, received_message: str) -> None:
        response = openai.Completion.create(
            model=MODEL,
            prompt=f"Respond to the following messages be kind, with helpful and engaging way: {received_message}",
            max_tokens=self.settings.max_tokens
        )
        response_content = response.choices[0].text.strip()
        self.send_message(response_content)
