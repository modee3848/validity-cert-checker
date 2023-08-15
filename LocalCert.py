import os
import ssl
import smtplib
import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from OpenSSL import crypto
import email.message
import sys

def check_certificate_expiration_cryptography(cert_file: str) -> int:
    try:
        with open(cert_file, 'rb') as f:
            cert_data = f.read()
        certificate = x509.load_pem_x509_certificate(cert_data, default_backend())
        cert_expires = datetime.datetime.strptime(certificate.not_valid_after.strftime('%Y%m%d%H%M%SZ'),
                                                  '%Y%m%d%H%M%SZ')
        return (cert_expires - datetime.datetime.now()).days
    except ValueError:
        pass
    except FileNotFoundError:
        return None

def check_certificate_expiration_openssl(cert_file: str) -> int:
    try:
        with open(cert_file, 'rb') as f:
            cert_data = f.read()
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        cert_expires = datetime.datetime.strptime(certificate.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        return (cert_expires - datetime.datetime.now()).days
    except crypto.Error:
        return None
    except FileNotFoundError:
        return None

def check_certificate_expiration(cert_file: str) -> int:
    days_to_expiration = check_certificate_expiration_cryptography(cert_file)
    if days_to_expiration is None:
        days_to_expiration = check_certificate_expiration_openssl(cert_file)
    return days_to_expiration

def find_and_check_certificates(msg: str):
    for root, dirs, files in os.walk('/'):
        for file in files:
            if file.endswith('.pem') or file.endswith('.crt') or file.endswith('.key'):
                cert_file = os.path.join(root, file)
                days_to_expiration = check_certificate_expiration(cert_file)
                if days_to_expiration is not None and days_to_expiration < 7 and days_to_expiration >= 0:
                    line = f"Certificate {cert_file} will expire in {days_to_expiration} days."
                    msg = msg + line + '\n'
                elif days_to_expiration is not None and days_to_expiration < 0:
                    line = f"Certificate {cert_file} has expired."
                    msg = msg + line + '\n'
                elif days_to_expiration is None:
                    pass
                else:
                    pass
    if msg != '':
        send_email(sys.argv[1], sys.argv[2], "smtp.elasticemail.com", 465,
                   msg)

def send_email(creds, recipient: str, host: str, port: int, content):
    with open(creds, "r") as input_file:
        lines = input_file.read().splitlines()
        credentials = []
        for line in lines:
            credentials.append(line)
    message = email.message.EmailMessage()
    content = content
    message.set_content(content)
    message['Subject'] = 'Expired local certificate'
    message['From'] = str(credentials[0])
    message['To'] = recipient
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        # To log into the email account using the provided username and password
        server.login(credentials[0], credentials[1])
        # An email message is then created using a text template and sent using the sendmail method
        server.send_message(message)

def main():
    msg = ''
    find_and

