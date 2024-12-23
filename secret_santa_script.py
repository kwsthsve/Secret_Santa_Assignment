import random
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def organize_secret_santa(emails, names):
    indices = list(range(len(emails)))
    email_dict = dict(zip(indices, emails))
    name_dict = dict(zip(indices, names))
    
    while True:
        assignments = list(range(len(indices)))
        random.shuffle(assignments)
        if all(i != j for i, j in enumerate(assignments)):
            break
    
    return email_dict, name_dict, assignments

def delete_sent_emails(sender_email, app_password):

    # Connect to Gmail's IMAP server
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(sender_email, app_password)
    
    # Select the "Sent Mail" folder
    imap.select('"[Gmail]/Sent Mail"')
    
    # Search for all emails in sent folder
    _, messages = imap.search(None, 'SUBJECT "Your Secret Santa Assignment!"')
    
    # Convert messages to a list of email IDs
    email_ids = messages[0].split()
    
    # Delete the emails (moves them to trash)
    for email_id in email_ids:
        imap.store(email_id, '+FLAGS', '\\Deleted')
    imap.expunge()
    
    print("\nSent emails have been deleted!")
    
    # Now empty the trash
    imap.select('"[Gmail]/Trash"')
    imap.store("1:*", '+FLAGS', '\\Deleted')
    imap.expunge()
    
    imap.close()
    imap.logout()
    print("Trash has been emptied!")

def send_emails(email_dict, name_dict, assignments, sender_email, app_password):

    # Connect to Gmail's SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, app_password)
    
    # Create email
    for santa_idx, recipient_idx in enumerate(assignments):
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_dict[santa_idx]
        msg['Subject'] = "Your Secret Santa Assignment!"
        
        body = f"Hello {name_dict[santa_idx]}!\n\nYou are the Secret Santa for: {name_dict[recipient_idx]}\n\nHappy gifting!"
        msg.attach(MIMEText(body, 'plain'))
        
        server.send_message(msg)
        print(f"Email sent to {email_dict[santa_idx]}")
    
    server.quit()

    # Wait a moment for emails to appear in sent folder
    time.sleep(5)
    
    # Delete sent emails
    delete_sent_emails(sender_email, app_password)

# Usage
if __name__ == "__main__":

    # Emails and names must be aligned!

    emails = ["person1@email.com", "person2@email.com", "person3@email.com"]
    names = ["Person 1", "Person 2", "Person 3"]
    
    # Your Gmail credentials
    sender_email = "your.email@gmail.com"
    app_password = "your-app-password"
    
    email_dict, name_dict, assignments = organize_secret_santa(emails, names)
    send_emails(email_dict, name_dict, assignments, sender_email, app_password)