import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import const

def send_email(subject, body, to_email):
    # Gmail SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port_ssl = 465  # SSL port
    gmail_email = const.gmail_email  # Replace with your Gmail address
    gmail_password = const.gmail_password  # Replace with your app-specific password


    # Create a MIME object
    msg = MIMEMultipart()
    msg['From'] = gmail_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body to the MIME message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establish SSL connection
        server = smtplib.SMTP_SSL(smtp_server, smtp_port_ssl)
        if const.debug:
            server.set_debuglevel(1)  # Enable debugging output
        server.login(gmail_email, gmail_password)

        # Send email
        server.sendmail(gmail_email, to_email, msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication error: {e}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


if __name__ == "__main__":
    subject = "Test Email"
    body = "This is a test email sent from Python."
    to_email = const.gmail_email  # Replace with recipient's email
    send_email(subject, body, to_email)
