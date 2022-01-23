import os
import smtplib
import ssl
import sys
from email.message import EmailMessage


class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = "paolo.varie00@gmail.com"
        self.password = "paolo.varie0027..06..88$"

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        msg = EmailMessage()
        msg['Subject'] = 'Ecco le nuove case!'
        msg['From'] = self.sender_mail
        msg['To'] = emails
        msg.set_content(content, subtype='html')
        result = service.send_message(msg)
        service.quit()


def render_email_template(template, **kwargs):
    # renders a Jinja template into HTML
    # check if template exists
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()

    import jinja2
    template_loader = jinja2.FileSystemLoader(searchpath=".")
    template_env = jinja2.Environment(loader=template_loader)
    templ = template_env.get_template(template)
    return templ.render(**kwargs)
