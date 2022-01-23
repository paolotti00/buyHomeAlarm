from constants import EMAIL_SUBJECT
from functions_email import Mail, render_email_template
from functions_repository import Repository
from functions_scrape import scrape_data, get_only_the_new, create_message

emails_to_send = ["pa.tripodi@hotmail.it", "denisediprima@virgilio.it"]

homes = scrape_data()
homes = get_only_the_new(homes)
if len(homes) > 0:
    # create message
    message = create_message(homes)
    # send email
    Mail().send(emails_to_send, EMAIL_SUBJECT, render_email_template("email_jinja_template.html", homes=homes))
    # save in db
    repository = Repository()
    repository.save_many_homes(homes)
    repository.save_many_messages(message)

