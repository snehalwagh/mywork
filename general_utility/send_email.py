"""
Author: Snehal Wagh
"""
import smtplib
import os
# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from titlecase import titlecase


def send_email(fromaddr='snehal.wagh@innoplexus.com', toaddr=['snehal.wagh@innoplexus.com', 'mrunmayee.jog@innoplexus.com'], cc=['jaimin.mehta@innoplexus.com'], datasets=None, therapeutic_assets=None, imgFileName=None):
    COMMASPACE = ', '
    datestr = datetime.today().strftime('%Y-%m-%dT%H:%M')
    msg = MIMEMultipart()
    msg['Subject'] = "Data has been updated for {} {}".format(
        therapeutic_assets, datasets)
    msg['To'] = COMMASPACE.join(toaddr)
    msg['From'] = fromaddr
    body = "Hi Team, \n \n{0} {1} data has been updated in oilbird-v4 portal at {2} \n\nThanks".format(
        therapeutic_assets, datasets, datestr)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.mailgun.org:587')
    server.starttls()

    print "logging in to server"
    server.login(
        "postmaster@sandboxfb20732ce1194972881b3c982ae7e327.mailgun.org",
        "a854b9984ddf0ce2d557a072149e387e")
    print "connected to server"
    if cc:
        msg['cc'] = COMMASPACE.join(cc)
        toaddr = toaddr + cc

    if imgFileName:
        img_data = open(imgFileName, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(imgFileName))
        msg.attach(image)
    response = server.sendmail(fromaddr, toaddr, msg.as_string())
    if not response:
        print "Successfully Sent mail!!!"
    server.quit()


if __name__ == "__main__":
    send_email(toaddr=['snehal.wagh@innoplexus.com', 'mrunmayee.jog@innoplexus.com'], cc=['jaimin.mehta@innoplexus.com'], datasets="Patents", therapeutic_assets="Oncology", imgFileName='/home/snehal.wagh/Downloads/maria-sharapova-tennis-wimbledon_3322430.jpg')
