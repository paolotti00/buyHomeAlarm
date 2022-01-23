import smtplib
import ssl
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
        msg['Subject'] = 'This is my first Python email'
        msg['From'] = self.sender_mail
        msg['To'] = emails
        msg.set_content(content, subtype='html')
        result = service.send_message(msg)
        service.quit()


def draft_email(message):
    email_content_to_return = '''
<!DOCTYPE html>
<html>
    <body>
        <div style="background-color:#eee;padding:10px 20px;">
            <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">My newsletter</h2>
        </div>
        <div style="padding:20px 0px">
            <div style="height: 500px;width:400px">
                <img src="https://dummyimage.com/500x300/000/fff&text=Dummy+image" style="height: 300px;">
                <div style="text-align:center;">
                    <h3>Article 1</h3>
                    <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. A ducimus deleniti nemo quibusdam iste sint!</p>
                    <a href="#">Read more</a>
                </div>
            </div>
        </div>
    </body>
</html>
'''
    return email_content_to_return
