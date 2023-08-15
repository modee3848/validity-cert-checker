import ssl
import socket
import smtplib
from datetime import datetime
import sys
import email.message

def check_certificate_expiration(host: str, port: int) -> int:
    context = ssl.create_default_context()
    # Create a connection with the provided host and port
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            context.set_default_verify_paths()
            certificate = ssock.getpeercert()
            # This date is converted into a datetime object using datetime.strptime and subtracted from the current
            # date (retrieved via datetime.now())
            cert_expires: datetime = datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
            return (cert_expires - datetime.now()).days

def send_email(creds, recipient: str, host: str, port: int, days_to_expiration: int, page :str, port2 :int):
    with open(creds, "r") as input_file:
        lines = input_file.read().splitlines()
        credentials = []
        for line in lines:
            credentials.append(line)
    message = email.message.EmailMessage()
    content = f"Certificate Expiration Warning \n\nThe certificate on host {socket.gethostname()} on port {port2} " \
              f"will expire in {days_to_expiration} days for the website {page}."
    message.set_content(content)
    message['Subject'] = 'Expired remote certificate'
    message['From'] = str(credentials[0])
    message['To'] = str(recipient)
    # To log into the mail account using the provided username and password
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(credentials[0], credentials[1])
        # Then an email message is created using a text template and sent using the sendmail method
        server.send_message(message)

def main():
    try:
        with open(sys.argv[1], "r") as input_file:
            lines = input_file.readlines()
            
            # For each line in the file
            for line in lines:
                # Split the line into host name and port number
                host, port = line.strip().split(':')
                port = int(port)
                days_to_expiration = check_certificate_expiration(host, port)
            # If the validity is less than 7 days, we send an email warning
            # the send_email function takes the sender's credentials, the email address of the message recipient, the host address and number
            # port for the mail server, and the number of days until the certificate expires
            if days_to_expiration < 7:
                send_email(sys.argv[2], sys.argv[3], "smtp.elasticemail.com", 465 , days_to_expiration, host, port)
    except FileNotFoundError:
        host, port = sys.argv[1].strip().split(':')
        port = int(port)
        days_to_expiration = check_certificate_expiration(host, port)
        # If the validity is less than 7 days, we send an email warning
        if days_to_expiration < 7:
            send_email(sys.argv[2], sys.argv[3], "smtp.elasticemail.com", 465, days_to_expiration, host, port)
if __name__ == "__main__":
    main()

