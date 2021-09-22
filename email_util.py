import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(to, subject, text_data, html_data):
    mail_content = text_data

    # The mail addresses and password
    sender_address = 'vsite.nationwide@gmail.com'
    sender_pass = 'Vsite@4321'
    receiver_address = to
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    message['Subject'] = subject  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)

    html = html_data
    message.attach(MIMEText(html, 'html'))
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def generate_html_from_dics(value_dic):
    table = '''<table style="border:1px solid black;">'''
    rows = ''
    for val in value_dic:
        rows = rows + '<tr>'
        cols = ''
        for col in val:
            cols = cols + '<td style="border:1px solid black;">' + str(col) + '</td>'

        rows = rows + cols + '</tr>'

    table = table + rows + '</table>'
    html = '<html><head></head><body>'+table+'</body></html>'
    return html
