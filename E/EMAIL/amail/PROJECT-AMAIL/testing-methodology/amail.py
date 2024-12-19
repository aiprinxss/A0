import smtplib

HOST = "smtp.localhost.com"
SUBJECT = "A0-MAIL-SERVER"
TO = "temp-mail.org"
FROM = "admin@localhost.com"
text = "AaBbCc09&%"
BODY = "\r\n".join((
    f"From:{FROM}",
    f"To:{TO}",
    f"Subject:{SUBJECT}",
    "",
    text)
)
server = smtplib.SMTP(HOST)
server.sendmail(FROM, [TO], BODY)
seerver.quit()
