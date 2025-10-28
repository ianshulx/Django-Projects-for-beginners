import smtplib
from email.mime.text import MIMEText

# Set up the server
smtp_server = 'live.smtp.mailtrap.io'
port = 587
login = 'api'
password = '41a94483113e0f93cb4a42b88d0eb3cd'

# Set up the MIME
message = MIMEText('This is a test email.')
message['Subject'] = 'Test Email'
message['From'] = 'admin@demomailtrap.com'
message['To'] = 'jilat13045@kernuo.com'

try:
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Secure the connection
    server.login(login, password)
    server.sendmail(message['From'], [message['To']], message.as_string())
    server.quit()
    print('Email sent successfully')
except Exception as e:
    print(f'Failed to send email: {e}')
