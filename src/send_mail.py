import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import base64
from dotenv import load_dotenv
load_dotenv()
 
# retrieve environmental variables from .env
sendgrid_api_key = os.environ.get('API_KEY')
from_address = os.environ.get('FROM')
to_list = os.environ.get('TOS').split(',')
 
# create a new massage
message = Mail()
 
# setting a sender
message.from_email = From(from_address)

# setting recivers
for i in range(len(to_list)):
    message.to = To(to_list[i])
    print(to_list[i])
 
# decide a subject line
subject_line = 'The job has completed!'
message.subject = Subject(subject_line)
 
# put a mail body
mail_body = 'The job worked without problems.\n\nVideo files have been successfully uploaded to S3.' # The job doesn't seem to have worked well.\n\nThere should be something wrong with it.
message.content = Content(MimeType.text, mail_body)

     
# adding the category information
message.category = Category('Category1')
     
# designate a custome header
message.header = Header('X-Sent-Using', 'SendGrid-API')
     
# send a mail
sendgrid_client = SendGridAPIClient(sendgrid_api_key)
sendgrid_client.send(message = message)

