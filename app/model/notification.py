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

    def get_channel_name(self) -> str:
        return f"file({self.file_path})"

    def send(self, message: str) -> None:
        if not self.is_available():
            raise ChannelUnavailableError(f"No se puede escribir en: {self.file_path}")
        try:
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except IOError as e:
            raise DeliveryError(f"Error al escribir en archivo: {e}") from e


class MockChannel(NotificationChannel):
    def is_available(self) -> bool:
        return False

    def get_channel_name(self) -> str:
        return "mock"

    def send(self, message: str) -> None:
        raise ChannelUnavailableError("MockChannel siempre está no disponible.")


