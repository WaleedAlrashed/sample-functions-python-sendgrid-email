from http import HTTPStatus
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

def main(args):
    '''
    Takes in the email address, subject, and message to send an email using SendGrid, 
    returns a json response letting the user know if the email sent or failed to send.

        Parameters:
            args: Contains the from email address, to email address, subject and message to send

        Returns:
            json body: Json response if the email sent successfully or if an error happened
    '''
    key = os.getenv('API_KEY')
    user_from = args.get("from")
    user_to = args.get("to")
    user_subject = args.get("subject")
    content = args.get("content")
    attachment_base64 = args.get("attachment_base64")  # Base64-encoded attachment
    attachment_filename = args.get("attachment_filename")  # Filename for the attachment


    if not user_from:
        return {
            "statusCode" : HTTPStatus.BAD_REQUEST,
            "body" : "no user email provided"
        }
    if not user_to:
        return {
            "statusCode" : HTTPStatus.BAD_REQUEST,
            "body" : "no receiver email provided"
        }
    if not user_subject:
        return {
            "statusCode" : HTTPStatus.BAD_REQUEST,
            "body" : "no subject provided"
        }
    if not content:
        return {
            "statusCode" : HTTPStatus.BAD_REQUEST,
            "body" : "no content provided"
        }

    # sg = SendGridAPIClient(key)
    # message = Mail(
    #     from_email = user_from,
    #     to_emails = user_to,
    #     subject = user_subject,
    #     html_content = content)
    # response = sg.send(message)

    message = Mail(
        from_email=user_from,
        to_emails=user_to,
        subject=user_subject,
        html_content=content)

    # If there's an attachment, process and add it to the message
     # If there's a base64-encoded attachment, add it to the message
    if attachment_base64 and attachment_filename:
        attachment = Attachment()
        attachment.file_content = FileContent(attachment_base64)
        attachment.file_type = FileType('image/png')  # Adjust the MIME type according to your file
        attachment.file_name = FileName(attachment_filename)
        attachment.disposition = Disposition('attachment')
        message.attachment = attachment
   

    sg = SendGridAPIClient(key)
    response = sg.send(message)

    if response.status_code != 202:
        return {
            "statusCode" : response.status_code,
            "body" : "email failed to send"
        }
    return {
        "statusCode" : HTTPStatus.ACCEPTED,
        "body" : "success"
    }


# {
#     "from": "dev@drhero.ae",
#     "to": "wmr121@gmail.com",
#     "subject": "Testing",
#     "content": "<html><body><p style=\"font-family: Arial, sans-serif; font-size: 16px; color: green;\">Hello serverless</p><p style=\"font-family: Arial, sans-serif; font-size: 14px;\">This is a <strong>test</strong> email with <em>HTML</em> content. Visit <a href=\"https://www.google.com\">Google</a>.</p><img src=\"https://picsum.photos/100/200\" alt=\"Random Image\"></body></html>"
# }

# doctl serverless deploy /Users/waleedalrashed/Documents/dev/workspace/micro_services/sample-functions-python-sendgrid-email --remote-build