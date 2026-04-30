from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import os
import uuid


class NotificationError(Exception):
    pass


class ChannelUnavailableError(NotificationError):
    pass


class DeliveryError(NotificationError):
    pass


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...

    @abstractmethod
    def get_channel_name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...


class ConsoleChannel(NotificationChannel):
    def is_available(self) -> bool:
        return True

    def get_channel_name(self) -> str:
        return "console"

    def send(self, message: str) -> None:
        try:
            print(message)
        except IOError as e:
            raise DeliveryError(f"Error al imprimir en consola: {e}") from e


class FileChannel(NotificationChannel):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def is_available(self) -> bool:
        pass




