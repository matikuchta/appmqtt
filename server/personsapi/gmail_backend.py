from django.core.mail.backends.base import BaseEmailBackend
from gmail_send import send_gmail

class GmailAPIEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        count = 0
        for message in email_messages:
            subject = message.subject
            body = message.body
            for recipient in message.to:
                send_gmail(subject, body, recipient)
                count += 1
        return count
