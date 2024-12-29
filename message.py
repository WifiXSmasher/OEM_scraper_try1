DEimport smtplib
from email.message import EmailMessage
import ssl


class Mail:

    @staticmethod
    def email(product, link, data):
        sender = 'Email Here*'
        PASSWORD = 'Password Here*'
        receiver = 'SEnders Email here*'

        subject = "new vulnerability found !"
        body = f"the product {product} was reported to have a vulnerability on the following link: {link}\n with the following data: \n{data}"

        em = EmailMessage()

        em['from'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, PASSWORD)
            smtp.sendmail(sender, receiver, em.as_string())
