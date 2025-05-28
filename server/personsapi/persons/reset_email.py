from djoser.email import PasswordResetEmail
from gmail_send import send_gmail
class PasswordResetEmail(PasswordResetEmail):
    def get_subject(self):
        return "Reset your password"

def get_email_body(self):
    uid = self.context.get('uid', '')
    token = self.context.get('token', '')
    url = f"http://yourdomain.com/password_reset_confirm/?uid={uid}&token={token}"
    return "Click the link below to reset your password:\n" + url

    # Jeśli chcesz wysyłać email przez swoją funkcję:
    def send(self, to):
        subject = self.get_subject()
        body = self.get_email_body()
        if isinstance(to, (list, tuple)):
            to = ", ".join(to)
        # tutaj wywołaj własną funkcję wysyłającą maila, np. send_gmail(subject, body, to)
        send_gmail(subject, body, to)
