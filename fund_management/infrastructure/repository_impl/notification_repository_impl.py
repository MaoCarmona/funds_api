from fund_management.core.repositories import NotificationsRepository
from fund_management.infrastructure.environment import config
from twilio.rest import Client

class NotificationRepositoryImpl(NotificationsRepository):
    def __init__(self):
        self.twilio_tk = config.twilio_tk
        self.twilio_account_sid = config.twilio_account_sid
        self.host_number = config.host_number

    def send_sms(self, to: str, body: str) -> None:
        account_sid = self.twilio_account_sid
        auth_token = self.twilio_tk
        client = Client(account_sid,auth_token)
        client.messages.create(from_=self.host_number,to=to,body=body)
