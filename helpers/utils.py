from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:

    @classmethod
    def send_simple_email(cls, to_email, subject, message):
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to_email]
        
        send_mail(subject, message, email_from, recipient_list)

    @classmethod
    def send_qr_code(cls, to_email, path, display_name):
        subject = 'Topnotchkiddiz Strict Invite'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [to_email]
        
        # Load your HTML template and attach an image
        html_content = render_to_string('qr_code.html', {'display_name': display_name})  # Pass context if needed
        text_content = strip_tags(html_content)  # Strip the HTML tags for the plain text version

        msg = EmailMultiAlternatives(subject, text_content, email_from, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        
        # Attach an image file
        with open(path, 'rb') as img:
            msg.attach('image.jpg', img.read(), 'image/jpeg')
        try:
            msg.send()
        except Exception as e:
            print(e, "Error: *********************")
