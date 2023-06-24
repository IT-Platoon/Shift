from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

TEMPLATES = {
    "info": "info/info.html",
}


def send_email(action, email_context, emails_to):
    """Function for send email with html template."""
    context = {
        "app_label": settings.APP_LABEL,
        **email_context,
    }
    html = get_template(TEMPLATES[action])
    msg = EmailMultiAlternatives(
        from_email=settings.EMAIL_HOST_USER,
        to=emails_to,
    )
    msg.attach_alternative(html.render(context), "text/html")
    msg.send()
