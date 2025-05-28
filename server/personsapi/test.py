from gmail_send import send_gmail

# Email details
subject = "Test Email from Python"
body = "This is a test message sent using Gmail API."
to_email = "mateuszkuchta2007@gmail.com"  # Change this to the recipient email

# Send the email
try:
    send_gmail(subject, body, to_email)
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
