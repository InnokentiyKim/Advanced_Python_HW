import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_SMTP = "smtp.gmail.com"
GMAIL_IMAP = "imap.gmail.com"


class UserMessage:
    def __init__(self, user_login, user_password):
        self.user_login = user_login
        self.user_password = user_password

    def _form_send_message(self, message_text, recipients, subject):
        message = MIMEMultipart()
        message['From'] = self.user_login
        message['To'] = ', '.join(recipients)
        message['Subject'] = subject
        message.attach(MIMEText(message_text))
        return message

    def send_message(self, message_text: str, recipients: list[str], subject: str = '') -> None:
        message = self._form_send_message(message_text, recipients, subject)
        mail_client = smtplib.SMTP(GMAIL_SMTP, 587)
        mail_client.ehlo()
        mail_client.starttls()
        mail_client.ehlo()
        mail_client.login(self.user_login, self.user_password)
        mail_client.sendmail(self.user_login, recipients, message.as_string())
        mail_client.quit()

    @staticmethod
    def _form_receive_message(mail_client, header: str = None) -> tuple:
        header = 'ALL' if not header else header
        criterion = f"(HEADER Subject '{header}')"
        result, data = mail_client.uid('search', criterion)
        return result, data

    def receive_message(self, header: str = None):
        mail_client = imaplib.IMAP4_SSL(GMAIL_IMAP)
        mail_client.login(self.user_login, self.user_password)
        mail_client.list()
        mail_client.select("inbox")
        letters_response, letters_data = self._form_receive_message(mail_client, header)
        try:
            assert letters_data[0]
        except AssertionError:
            print('There are no letters with current header')
            return
        latest_email_uid = letters_data[0].split()[-1]
        message_response, message_data = mail_client.uid('fetch', latest_email_uid, '(RFC822)')
        email_message = email.message_from_string(message_data[0][1])
        mail_client.logout()
        return email_message


def main():
    login = 'login@gmail.com'
    password = 'qwerty'
    subject = 'Subject'
    recipients = ['vasya@email.com', 'petya@email.com']
    user = UserMessage(login, password)
    message_text = 'Message'
    user.send_message(message_text, recipients, subject)
    received_message = user.receive_message()


if __name__ == '__main__':
    main()
