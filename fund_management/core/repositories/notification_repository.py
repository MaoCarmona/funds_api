from typing import Protocol

class NotificationsRepository(Protocol):
    def send_sms(self, to: str, body: str) -> None:
        """ Send a sms to a phone number"""
        ...
