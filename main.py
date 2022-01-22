from functions_email import Mail
from scrapes_functions import scrape_data, draft_email

homes = scrape_data()
for home in homes:
    print(vars(home))
    print("---")
email_content = draft_email(homes)
email_sender = Mail()
emails_to_send=["pa.tripodi@hotmail.it"]
email_sender.send(emails_to_send, homes, email_content)
