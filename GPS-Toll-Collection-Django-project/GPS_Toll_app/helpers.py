from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_forget_email(email, token):
    subject = 'Forget Password link'
    
    # Render the HTML content from a template
    html_message = render_to_string('authrization/forget_password_email.html', {'token': token})
    
    # Set the sender email address
    from_email = settings.EMAIL_HOST_USER
    
    # Set the recipient list (can be a list of emails)
    recipient_list = [email]
    
    # Generate plain text message by stripping HTML tags from html_message
    message = strip_tags(html_message)
    
    # Create EmailMessage object
    email = EmailMessage(subject=subject, body=message, from_email=from_email, to=recipient_list)
    
    # Attach the HTML content to the email
    email.content_subtype = 'html'
    
    # Send the email
    email.send()


