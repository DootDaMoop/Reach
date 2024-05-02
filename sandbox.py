import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime as dt
import time
import threading
from repositories import user_repo, group_repo, event_repo

def send_email():
    smtp_server = "smtp.gmail.com"
    port = 587  
    sender_email = "reach543210@gmail.com"
    receiver_email = "ynieban@uncc.edu"
    password = "sfjw uond wezc fnsl"

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)

    message = MIMEMultipart('alternative')
    message["Subject"] = "cum 4.0"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
    <html>
    <head></head>
    <body>
        <p>cum<br>
        cummuc<br>
        cum time <a href="http://www.sdfsfdsfdf.com">link</a> you wanted.
        </p>
    </body>
    </html>
    """

    content = MIMEText(html, 'html')
    message.attach(content)

    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("cum time")

def schedule_email(event_time_str, hours_before = 0, minutes_before=0, seconds_before=0):

    event_time = dt.datetime.strptime(event_time_str, '%Y-%m-%d %H:%M:%S')
    
    send_time = event_time - dt.timedelta(hours=hours_before, minutes=minutes_before, seconds=seconds_before)
    
    now = dt.datetime.now()
    
    if now < send_time:
        time_to_wait = (send_time - now).total_seconds()
        time.sleep(time_to_wait)  
        send_email()
    else:
        print("Send time is in the past. Email will not be sent.")

event_time_str = "2024-5-02 03:03:50" 
hours_before = 0    
minutes_before = 0 
seconds_before = 0

thread = threading.Thread(target=schedule_email, args=(event_time_str, hours_before, minutes_before, seconds_before))
thread.start()

for i in range(10):
    print(i)
    time.sleep(1)


    