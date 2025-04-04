
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import Settings
import requests

import json





setting =Settings()
pass_code = setting.PASS_CODE
gmail_user =  setting.EMAIL


def create_html_table(transaction_data):
    table_html = "<table border='1'>"

    # Iterate over each transaction
    for transaction in transaction_data:
        for key, value in transaction.items():
            table_html += f"<tr><th>{key}</th><td>{value}</td></tr>"

    table_html += "</table>"
    return table_html

def notify_user_transaction(
    usecase_name,
    transcation_id,
    first_name,
    exexpéditeur,
    receiver,
    description,
    commantaire,
    status,
    assinged_to,
    cc_addresses,
    body,
):
    subject = f"Transcation {transcation_id} information"

    # Parse JSON data
    transaction_data = json.loads(body)
    if status is None:
        status = ""
    if assinged_to is None:
        assinged_to = ""
    if commantaire is None:
        commantaire = ""
    # Create HTML table
    table_html = create_html_table(transaction_data)
    # Include additional information before the HTML table
    additional_info = f"""
    <p> <b> {first_name} request investigation on the below case : </b> <p>
    <p><strong> - Expeditor:</strong> {exexpéditeur}</p>
        <p><strong> - Description:</strong> {description}</p>
        <b> <u> Data info: </u> </b> <br>
        <p> <strong> - Usecase name : </strong> {usecase_name} </p>
        <p><strong> - Comment:</strong> {commantaire}</p>
        <p><strong> - Status:</strong> {status}</p>
        <p><strong> - Assigned to:</strong> {assinged_to}</p>
    """

    try:
        
        sender_address = gmail_user
        sender_pass = pass_code
        receiver_address = receiver
        message = MIMEMultipart()
        message["From"] = sender_address
        message["Cc"] = ", ".join(cc_addresses)
        
        message["To"] = receiver
        message["Subject"] = subject
        all_recipients = [receiver] + cc_addresses

        # Attach the additional information and HTML table to the email
        message.attach(MIMEText(additional_info + table_html, "html"))

        # Create SMTP session for sending the mail
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, all_recipients, text)
        return True
    except Exception as e:
        return False


import asyncio
async def heavy_data_processing(data: dict):
    """Some (fake) heavy data processing logic."""
    await asyncio.sleep(2)
    message_processed = data.get("message", "")
    return message_processed

def send_restepassword_email(receiver, first_name,id_user):
    subject = "Password reset request for your Easink account"
    first_name=first_name[0].upper()  + first_name[1:]
    HTMLPart = f"""
    <img src="{setting.EMAIL_URL}assets/Easink.png" alt="" width="205" height="61" /> <br /> \
    Dear <b>{first_name}</b> , <br> \
    We have received a request to reset the password for your Easink account associated with this email address. <br> \
    If you did not make this request, please ignore this email and your account will remain secure.<br> \
    If you did request a password reset, please verify your email address by clicking on the link below: <br> \
   <a href="{setting.EMAIL_URL}auth/setpassword/{id_user}"> Set password </a>.<br>\
    Please note that this link will expire in 24 hours for security reasons. <br>\
    If you have any questions or concerns, please do not hesitate to contact our customer support team at contact@easink.app. <br>\
    Best regards,
"""



    try : 
        sender_address = gmail_user
        sender_pass = pass_code
        mail_content = HTMLPart
        receiver_address = receiver
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        return True
    except Exception as e :
        return False
    
def send_email(receiver,first_name,admin_name,id_user):
    subject = "Invitation to join Easink and set up your account"
    first_name = first_name[0].upper()  + first_name[1:]
    admin_name = admin_name[0].upper()  + admin_name[1:]
    HTMLPart = f"""
            <img src="{setting.EMAIL_URL}assets/Easink.png" alt="" width="205" height="61" /> <br /> \
            Dear <b>{first_name}</b>,<br>\
            The admin <b> {admin_name}  </b> has invited you to join Easink AI. To activate your account, please follow the steps below: <br> \
            <b> Step 1: Verify your email address </b> <br> \
            Please click on the verification link below to confirm your email address: <br> \
            <a href="{setting.EMAIL_URL}auth/setpassword/{id_user}">Verification Link</a> <br> \
            <b> Step 2: Set up your account </b> <br> \
            After verifying your email address, please click on the link below to set new password <br> \
            Please note that the password set up link will expire in 24 hours. <br> \
            If you did not expect this invitation or do not want to join Easink AI, please ignore this email. <br> \
            If you have any questions or concerns, please do not hesitate to contact us at contact@Easink.app. <br> \
            Best regards,<br> \
            Easink Team
"""

    try : 
        sender_address = gmail_user
        sender_pass = pass_code
        mail_content = HTMLPart
        receiver_address = receiver
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        return True
    except Exception as e :
        return False
    
def send_verify_email(receiver,first_name,id_user):
    subject = "Verify your email address to activate your account"
    first_name=first_name[0].upper()  + first_name[1:]
    HTMLPart = f"""
            <img src="{setting.EMAIL_URL}assets/servitia.png" alt="" width="205" height="61" /> <br /> \
            Dear <b>{first_name}</b>,<br>\
            Thank you for signing up for servitia. To activate your account, we require you to verify your email address by clicking the verification link below: <br> \
            <a href='{setting.EMAIL_URL}mydemandes'>Verification Link</a>.<br>            
            If you did not sign up for servitia, please ignore this email.<br> \
            If you have any questions or concerns, please do not hesitate to contact our customer support team at contact@servitia.app <br> \
            Thank you for choosing servitia AI. We look forward to providing you with a great user experience. <br> \
            Best regards, <br> \
            servitia Team"""

    try : 
        sender_address = gmail_user
        sender_pass = pass_code
        mail_content = HTMLPart
        receiver_address = receiver
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        return True
    except Exception as e :
        return False
    
def send_request_email(receiver,first_name,requestor,admin_name):
    subject = "New access request from "+first_name
    first_name=first_name[0].upper()  + first_name[1:]
    admin_name =admin_name[0].upper()  + admin_name[1:]
    HTMLPart = f"""
            <img src="{setting.EMAIL_URL}assets/Easink.png" alt="" width="205" height="61" /> <br /> \
            Dear <b>{admin_name}</b>,<br>\
            This email is to inform you that <b> {first_name} ({requestor}) </b> , a member of your organization, has requested access to Easink AI. They have submitted a request for access through our system. <br>         
            Please review this request as soon as possible and take appropriate action to grant or deny access. To do so, please log in to your account and navigate to the access management section.  <br> \
            If you have any questions or concerns, please do not hesitate to contact our customer support team at contact@Easink.app <br> \
            Best regards, <br> \
            Easink Team"""

    try : 
        sender_address = gmail_user
        sender_pass = pass_code
        mail_content = HTMLPart
        receiver_address = receiver
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        return True
    except Exception as e :
        return False
    


import requests




def send_request(
    token: str, data: dict, endpoint: str, rtype: str
) -> requests.Response:
    """
    Sends a  request to a specified endpoint with the provided token, data, and headers.

    Args:
        token (str): Authorization token for the request.
        data (dict): Data payload to be sent in the request body.
        endpoint (str): The API endpoint to send the request to.
        rtype (str) : The endpoint method

    Returns:
        requests.Response: The response object containing the server's response to the request.

    """

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json" , 'accept': 'application/json'}
    if rtype == "POST":
        response = requests.post(
            f"{setting.BACKEND_URL}/{endpoint}", headers=headers, json=data
        )
        return response
    elif rtype == "DELETE":
        response = requests.delete(f"{setting.BACKEND_URL}/{endpoint}", headers=headers)
        return response

    elif rtype == "GET":
        response = requests.get(f"{setting.BACKEND_URL}/{endpoint}", headers=headers)
        return response
    

def auth(token: str) -> bool:
    """
    Performs user authentication by sending an authentication request with the provided token.

    Args:
        token (str): The authentication token for user validation.

    Returns:
        bool: True if the authentication request is successful, False otherwise.

    """

    response = send_request(token, {}, "authentification_user", "POST")
    return response.text == "true"