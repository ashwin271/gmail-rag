import imaplib
import email
from email.header import decode_header

# Connect to an IMAP server
def connect_to_email(username, password, server='imap.gmail.com'):
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    return mail

# Fetch and parse emails
def fetch_emails(mail, mailbox='inbox'):
    mail.select(mailbox)
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()
    emails = []
    
    for e_id in email_ids:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                emails.append(msg)
    return emails
