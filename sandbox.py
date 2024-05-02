import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime as dt
import time

# def send_email():
#     smtp_server = "smtp.gmail.com"
#     port = 587  
#     sender_email = "reach543210@gmail.com"
#     receiver_email = "alopez53@uncc.edu"
#     password = "sfjw uond wezc fnsl"

#     server = smtplib.SMTP(smtp_server, port)
#     server.starttls()
#     server.login(sender_email, password)

#     message = MIMEMultipart('alternative')
#     message["Subject"] = "cum 3.0"
#     message["From"] = sender_email
#     message["To"] = receiver_email

#     html = """\
#     <html>
#     <head></head>
#     <body>
#         <p>cum<br>
#         cummuc<br>
#         cum time <a href="http://www.sdfsfdsfdf.com">link</a> you wanted.
#         </p>
#     </body>
#     </html>
#     """

#     content = MIMEText(html, 'html')
#     message.attach(content)

#     server.sendmail(sender_email, receiver_email, message.as_string())
#     server.quit()
#     print("Email sent!")



# now = dt.datetime.now()
# send_time = dt.datetime(now.year, now.month, now.day, 1, 6)

# if now < send_time:
#     time_to_wait = (send_time - now).total_seconds()
#     time.sleep(time_to_wait)

# send_email()







import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    try:
        smtp_server = "smtp.gmail.com"
        port = 587  
        sender_email = "reach543210@gmail.com"
        receiver_email = "alopez53@uncc.edu"
        password = "sfjw uond wezc fnsl"

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Log in to the server

        message = MIMEMultipart('alternative')
        message["Subject"] = "cum 3.0"
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
        print("Email sent!")
    except Exception as e:
        print("Failed to send email:", e)

# Example call to the function
send_email()


















# # # import asyncio
# # # import datetime as dt
# # # from email.mime.text import MIMEText
# # # from email.mime.multipart import MIMEMultipart
# # # import aiosmtplib

# # # async def send_email():
# # #     smtp_server = "smtp.gmail.com"
# # #     port = 587
# # #     sender_email = "reach543210@gmail.com"
# # #     receiver_email = "alopez53@uncc.edu"
# # #     password = "sfjw uond wezc fnsl"

# # #     server = aiosmtplib.SMTP(hostname=smtp_server, port=port, use_tls=False)
# # #     await server.connect()
# # #     await server.starttls()
# # #     await server.login(sender_email, password)

# # #     message = MIMEMultipart('alternative')
# # #     message["Subject"] = "Event Notification"
# # #     message["From"] = sender_email
# # #     message["To"] = receiver_email

# # #     html = """\
# # #     <html>
# # #     <head></head>
# # #     <body>
# # #         <p>Event Reminder:<br>
# # #         Here is the <a href="http://www.yourlink.com">link</a> you requested.
# # #         </p>
# # #     </body>
# # #     </html>
# # #     """

# # #     content = MIMEText(html, 'html')
# # #     message.attach(content)

# # #     await server.send_message(message)
# # #     await server.quit()
# # #     print("Email sent!")

# # # # async def schedule_email(send_time):
# # # #     now = dt.datetime.now()
# # # #     if now < send_time:
# # # #         time_to_wait = (send_time - now).total_seconds()
# # # #         await asyncio.sleep(time_to_wait)
# # # #     await send_email()

# # # # Usage
# # # # now = dt.datetime.now()
# # # # send_time = dt.datetime(now.year, now.month, now.day, 16, 58)  # Set the intended send time

# # # # Start the asyncio event loop and schedule the email
# # # loop = asyncio.get_event_loop()
# # # loop.run_until_complete(send_email())


    
# # # # count = 0
# # # # while count < 10:
# # # #     print('cum')









# # # import smtplib
# # # from email.mime.text import MIMEText
# # # from email.mime.multipart import MIMEMultipart
# # # import datetime as dt
# # # import time
# # # import threading

# # # def send_email():
# # #     smtp_server = "smtp.gmail.com"
# # #     port = 587  
# # #     sender_email = "reach543210@gmail.com"
# # #     receiver_email = "alopez53@uncc.edu"
# # #     password = "sfjw uond wezc fnsl"

# # #     server = smtplib.SMTP(smtp_server, port)
# # #     server.starttls()
# # #     server.login(sender_email, password)

# # #     message = MIMEMultipart('alternative')
# # #     message["Subject"] = "cum 3.0"
# # #     message["From"] = sender_email
# # #     message["To"] = receiver_email

# # #     html = """\
# # #     <html>
# # #     <head></head>
# # #     <body>
# # #         <p>cum<br>
# # #         cummuc<br>
# # #         cum time <a href="http://www.sdfsfdsfdf.com">link</a> you wanted.
# # #         </p>
# # #     </body>
# # #     </html>
# # #     """

# # #     content = MIMEText(html, 'html')
# # #     message.attach(content)

# # #     server.sendmail(sender_email, receiver_email, message.as_string())
# # #     server.quit()
# # #     print("Email sent!")

# # # def schedule_email(send_time):
# # #     now = dt.datetime.now()
# # #     if now < send_time:
# # #         time_to_wait = (send_time - now).total_seconds()
# # #         time.sleep(time_to_wait)
# # #     send_email()

# # # # Schedule emails at specific times using threading
# # # times_to_send = [dt.datetime.now() + dt.timedelta(seconds=10), dt.datetime.now() + dt.timedelta(seconds=20)]

# # # for send_time in times_to_send:
# # #     threading.Thread(target=schedule_email, args=(send_time,)).start()

# # # # Example of another function that runs simultaneously
# # # def other_function():
# # #     for i in range(10):
# # #         print("Other function is running")
# # #         time.sleep(1)

# # # other_function_thread = threading.Thread(target=other_function)
# # # other_function_thread.start()











# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # import datetime as dt
# # import time
# # import threading
# # from dateutil import parser  # You might need to install this with `pip install python-dateutil`

# # def send_email():
# #     smtp_server = "smtp.gmail.com"
# #     port = 587  
# #     sender_email = "reach543210@gmail.com"
# #     receiver_email = "alopez53@uncc.edu"
# #     password = "sfjw uond wezc fnsl"

# #     server = smtplib.SMTP(smtp_server, port)
# #     server.starttls()
# #     server.login(sender_email, password)

# #     message = MIMEMultipart('alternative')
# #     message["Subject"] = "Event Notification"
# #     message["From"] = sender_email
# #     message["To"] = receiver_email

# #     html = """\
# #     <html>
# #     <head></head>
# #     <body>
# #         <p>Hello,<br>
# #         Here is the <a href="http://www.example.com">link</a> you requested.
# #         </p>
# #     </body>
# #     </html>
# #     """

# #     content = MIMEText(html, 'html')
# #     message.attach(content)

# #     server.sendmail(sender_email, receiver_email, message.as_string())
# #     server.quit()
# #     print("Email sent!")

# # def schedule_email(send_time_str):
# #     send_time = parser.parse(send_time_str) if isinstance(send_time_str, str) else send_time_str
# #     now = dt.datetime.now()
# #     if now < send_time:
# #         time_to_wait = (send_time - now).total_seconds()
# #         time.sleep(time_to_wait)
# #     send_email()

# # # Example Usage
# # # Schedule emails using threading, and parse datetime string if needed
# # times_to_send = ["2023-10-05 15:30:00", "2023-10-05 15:35:00"]  # PostgreSQL timestamp strings

# # for send_time_str in times_to_send:
# #     threading.Thread(target=schedule_email, args=(send_time_str,)).start()

# # # Example of another function that runs simultaneously
# # def other_function():
# #     for i in range(10):
# #         print("Other function is running")
# #         time.sleep(1)

# # other_function_thread = threading.Thread(target=other_function)
# # other_function_thread.start()





















# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import datetime as dt
# import time
# import threading

# # def send_email():
# #     smtp_server = "smtp.gmail.com"
# #     port = 587  
# #     sender_email = "reach543210@gmail.com"
# #     receiver_email = "alopez53@uncc.edu"
# #     password = "sfjw uond wezc fnsl"

# #     server = smtplib.SMTP(smtp_server, port)
# #     server.starttls()
# #     server.login(sender_email, password)

# #     message = MIMEMultipart('alternative')
# #     message["Subject"] = "cum 3.0"
# #     message["From"] = sender_email
# #     message["To"] = receiver_email

# #     html = """\
# #     <html>
# #     <head></head>
# #     <body>
# #         <p>cum<br>
# #         cummuc<br>
# #         cum time <a href="http://www.sdfsfdsfdf.com">link</a> you wanted.
# #         </p>
# #     </body>
# #     </html>
# #     """

# #     content = MIMEText(html, 'html')
# #     message.attach(content)

# #     server.sendmail(sender_email, receiver_email, message.as_string())
# #     server.quit()
# #     print("cum time")

# # def schedule_email(event_time_str, hours_before = 0, minutes_before=0, seconds_before=0):

# #     event_time = dt.datetime.strptime(event_time_str, '%Y-%m-%d %H:%M:%S')
    
# #     send_time = event_time - dt.timedelta(hours=hours_before, minutes=minutes_before, seconds=seconds_before)
    
# #     now = dt.datetime.now()
    
# #     if now < send_time:
# #         time_to_wait = (send_time - now).total_seconds()
# #         time.sleep(time_to_wait)  
# #         send_email()
# #     else:
# #         print("Send time is in the past. Email will not be sent.")

# # event_time_str = "2024-5-02 00:37:00" 
# # hours_before = 0    
# # minutes_before = 0 
# # # seconds_before = 0

# # # thread = threading.Thread(target=schedule_email, args=(event_time_str, hours_before, minutes_before, seconds_before))
# # # thread.start()

# # # for i in range(10):
# # #     print(i)
# # #     time.sleep(1)















# # smtp_server = "smtp.gmail.com"
# # port = 587  
# # sender_email = "reach543210@gmail.com"
# # receiver_email = "alopez53@uncc.edu"
# # password = "sfjw uond wezc fnsl"

# # server = smtplib.SMTP(smtp_server, port)
# # server.starttls()
# # server.login(sender_email, password)

# # message = MIMEMultipart('alternative')
# # message["Subject"] = "cum 3.0"
# # message["From"] = sender_email
# # message["To"] = receiver_email

# # html = """\
# # <html>
# # <head></head>
# # <body>
# #     <p>cum<br>
# #     cummuc<br>
# #     cum time <a href="http://www.sdfsfdsfdf.com">link</a> you wanted.
# #     </p>
# # </body>
# # </html>
# # """

# # content = MIMEText(html, 'html')
# # message.attach(content)

# # server.sendmail(sender_email, receiver_email, message.as_string())
# # server.quit()
# # print("Email sent!")


