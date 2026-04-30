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

@dataclass
class DeliveryReport:
    channel_name: str
    total_attempted: int
    total_delivered: int
    messages: list = field(default_factory=list)
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def success_rate(self) -> float:
        if self.total_attempted == 0:
            return 0.0
        return self.total_delivered / self.total_attempted

    def is_empty(self) -> bool:
        return self.total_delivered == 0

    def __str__(self) -> str:
        return (
            f"DeliveryReport | Canal: {self.channel_name} | "
            f"Intentados: {self.total_attempted} | "
            f"Entregados: {self.total_delivered} | "
            f"Tasa de éxito: {self.success_rate():.0%} | "
            f"ID: {self.report_id}"
        )
class NotificationService:
    def __init__(self, channel: NotificationChannel):
        self._channel = channel
        self._history: list[str] = []

    def send_notification(self, message: str) -> None:
        if not self._channel.is_available():
            raise ChannelUnavailableError(f"Canal '{self._channel.get_channel_name()}' no disponible.")
        self._channel.send(message)
        self._history.append(message)

    def send_bulk(self, messages: list[str]) -> int:
        delivered = 0
        for message in messages:
            try:
                self.send_notification(message)
                delivered += 1
            except NotificationError:
                continue
        return delivered

    def get_history(self) -> list[str]:
        return self._history.copy()

    def generate_report(self) -> DeliveryReport:
        history = self.get_history()
        return DeliveryReport(
            channel_name=self._channel.get_channel_name(),
            total_attempted=len(history),
            total_delivered=len(history),
            messages=list(history),
        )