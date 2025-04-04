

successful_response={   
          '200': {'description': 'Successful Response',
          'content': {'application/json': {'example': { 'message': 'user added succesfully !'}}}
          }
          }
bad_request = {    
    '400': {'description': 'Bad Request', 
    'content': {'application/json': {'description': 'The request is invalid.',
              'example': {'error': 'Bad Request', 'message': ''}}}}}

validation_error ={   
    '422': {'description': 'Validation Error', 
    'content': {'application/json': {'description': 'The request validation is failed .',
    'example': {
      "detail": [
      {
        "loc": [
          "body",
          "email,role,..."
          ],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
  }}}}
  }


forbidden_response={          
    '403': {'description': 'Error: Forbidden',
          'content': {'application/json': {'example': {"detail": "Not authenticated"}}}
          }}

unauthorized_response={          
    '401': {'description': 'Error: Forbidden',
          'content': {'application/json': {'example': {"detail": "Invalid token"}}}
          }}

email_response={
    '409':{'description': 'Email used',
          'content': {'application/json': {'example': {"detail": "Email address already in use"}}}
          }}

business_email_response={
    '408':{'description': 'business email',
          'content': {'application/json': {'example': {"detail": "We can only accept emails that are associated with a business domain."}}}
          }}

business_domain_response={
    '412':{'description': 'business domain',
          'content': {'application/json': {'example': {"detail": "The email you provided is not associated with any registered organization that matches your business domain."}}}
          }}

admin_response={
    '410':{'description': 'admin exist',
          'content': {'application/json': {'example': {"detail": "A member of your organisation is already registered, your request has been sent to your admin organization."}}}
}}

send_email_response={
    '421':{'description': 'Failed send email',
          'content': {'application/json': {'example': {"detail": "Failed to send the email"}}}
}}

user_response={
    '404':{'description': 'not found',
          'content': {'application/json': {'example': {"detail": "User is not found."}}}
}}

invalid_password_response={
    '411':{'description': 'Invalid password',
          'content': {'application/json': {'example': {"detail": "Password is invalid to sign up."}}}
}}

incorrect_password_response={
    '412':{'description': 'Incorrect password',
          'content': {'application/json': {'example': {"detail": "Incorrect password"}}}
}}
old_password_response={
    '426':{'description': 'Incorrect password',
          'content': {'application/json': {'example': {"detail": "Your old password is incorrect"}}}
}}
verify_email_response={
    '406':{'description': 'verify email',
          'content': {'application/json': {'example': {"detail": "Please verify your email and try again!"}}}
}}

invitation_reponse={
    '424':{'description': 'Invitation',
          'content': {'application/json': {'example': {"detail": "Invitation Expired !"}}}
}}