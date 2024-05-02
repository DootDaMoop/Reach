import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime as dt
import time
import os
import threading
from repositories import user_repo, group_repo, event_repo

def send_email(receiver_email: str, subject: str, HTML_message: str):
    smtp_server = "smtp.gmail.com"
    port = 587  
    sender_email = "reach202425@gmail.com" # Default Email for Reach
    password = os.getenv('EMAIL_PASSWORD',)

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, password)

    message = MIMEMultipart('alternative')
    message["Subject"] = subject      #subject of email
    message["From"] = sender_email      
    message["To"] = receiver_email

    html = HTML_message

    content = MIMEText(html, 'html')
    message.attach(content)

    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

def schedule_email(event_start_timestamp, hours_before = 0, minutes_before=0, seconds_before=0):
    event_time = dt.datetime.strptime(event_start_timestamp, '%Y-%m-%d %H:%M:%S')
    
    send_time = event_time - dt.timedelta(hours=hours_before, minutes=minutes_before, seconds=seconds_before)
    
    now = dt.datetime.now()
    
    if now < send_time:
        time_to_wait = (send_time - now).total_seconds()
        time.sleep(time_to_wait)  
        send_email()
    else:
        print("Send time is in the past. Email will not be sent.")

# Hard Coded Example
# event_time_str = "2024-5-02 05:40:50" 
# hours_before = 0    
# minutes_before = 0 
# seconds_before = 0

# thread = threading.Thread(target=schedule_email, args=(event_time_str, hours_before, minutes_before, seconds_before))
# thread.start()

# for i in range(10):
#     print(i)
#     time.sleep(1)