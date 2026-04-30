import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable
from  abc import ABC, abstractmethod

from app.services.util import generate_unique_id
class NotificationService:
    channel: str

    def send_notification(self, message: str) -> None:
        pass

    def send_bulk(self, messages: list ) -> int:
        pass

class NotificationChannel(ABC):
    @abstractmethod

    def send(self, massage: str) -> None:
        pass

    def get_channel_name(self) -> str:
        pass

class ConsoleChannel:
    pass

class MonkChannel:
    pass


