from constants import EMAIL_SUBJECT
from functions_email import Mail, render_email_template
from functions_scrape import scrape_data, get_only_the_new, create_message

emails_to_send = ["pa.tripodi@hotmail.it", "denisediprima@virgilio.it"]

homes = scrape_data()
homes = get_only_the_new(homes)
# create message
message = create_message(homes)
# send email
Mail().send(emails_to_send, EMAIL_SUBJECT, render_email_template("email_jinja_template.html", homes=homes))
