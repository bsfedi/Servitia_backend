import re
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from datetime import datetime
from user.models import *
from database import db
from user.service import *
from argon2 import PasswordHasher
from secuirty import *
from utilities import *
from user.responses import *
from bson.binary import Binary
from typing import List
from utilities import heavy_data_processing
user_router = APIRouter(tags=["User"])
 
ph = PasswordHasher()


@user_router.post("/authentification_user")
async def check_user(token: dict = Depends(token_required)):
    if token:
        return True


@user_router.get(
    "/users/verify_email/{user_id}",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
    },
)
async def verify_email(user_id):
    """
    Verify the email address associated with a user account.

    Args:
        user_id (str): User ID of the account to be verified.

    Returns:
        dict: Dictionary containing a success message indicating that the email has been verified.

    """
    user = get_user_by_id(user_id)
    accept_invitation(user_id)
    return {"message": "Account verified successfully "}

@user_router.post(
    "/auth/signup",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **invalid_password_response,
        **send_email_response,
        **admin_response,
        **email_response,
        **business_email_response,
        **business_domain_response,
    },
)
async def sign_up(user: User):
    """
    Validates a password format based on specified requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    # Get date of today
    now = datetime.now()
    hashed_password = ph.hash(user.password)
    user.password = hashed_password
    
    user_id = signup(user)
    print(user_id)
    send_verify_email(user.email,user.email.split('@')[0],str(user_id['user_id']))
        
    return {"message": "user added succesfully !"}


@user_router.post(
    "/auth/login",
    responses={
        **bad_request,
        **validation_error,
        **incorrect_password_response,
        **invalid_password_response,
        **successful_response,
        **user_response,
        **verify_email_response,
    },
)
async def login_api(userr: User_login):
    """
    API endpoint for user login.

    Args:
        userr (User_login): User login information (email, password) .

    Returns:
        dict: Dictionary containing user email and access token.

    """
    # retrieves the user from the database by email
    user = get_user_by_email(userr.email)



    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if user's email is verified

    # verify the password hash
    verify_password(user.get("password"), userr.password)

    # Create an access token with user ID
    token = create_access_token({"id": str(user["_id"])})
    await heavy_data_processing({"message":token})

    return {"user": user["email"], "token": token,"role":user.get("role"),"user_id":str(user.get("_id"))}


@user_router.put(
    "/users/{user_id}",
    responses={**bad_request, **validation_error, **successful_response},
)
async def edit_user(
    user_id,
    first_name: str = Form(...),
    last_name: str = Form(...),
    specialite: str = Form(...),
    descriptif: str = Form(...),
    prix: str = Form(...),
    img_url: Optional[UploadFile] = File(None),
):
    """
    Update the user information in the database by user ID.

    Args:
        user_id (str): User ID of the user whose information needs to be updated.
        user (dict): Dictionary containing the updated user information.
            Example: {"first_name": "John", "last_name": "Doe", "img_url": "image_url"}

    Returns:
        pymongo.results.UpdateResult: Result of the update operation from the MongoDB collection.
    """
    user = get_user_by_id(user_id)


    image_bytes = await img_url.read()
    img_url = image_bytes

    user = {"first_name": first_name, "specialite": specialite, "descriptif": descriptif, "prix": prix, "last_name": last_name, "img_url": img_url}
    result = updat_user(user_id, user)
    updated_user = get_user_by_id(user_id)
    return {"message": "user updated successfully", "user": updated_user}


@user_router.get(
    "/user_by_id/{user_id}",
)
async def add_service(user_id):

    user = get_user_by_id(user_id)


    return {"user":user}




@user_router.post(
    "/service",
)
async def add_service(Service: Service):

    new_service= dict(Service)


    response = db["services"].insert_one(new_service)
    return {"message":"service added successfully"}



@user_router.get(
    "/searchservice/{name}",
)
async def searchçservice(name:str,token: dict = Depends(token_required)):
    print(name)
    
    response = db["services"].find({"nom":name})
    searchservice = []
    for ee in response:
        ee['_id']=str("_id")
        ee['user_info'] = get_user_by_id(ee["user_id"])
        searchservice.append(ee)
    return {"searchçservice":searchservice}



@user_router.get(
    "/get_services_by_user/{user_id}",
)
async def get_services_by_user(user_id:str):

    
    response = db["services"].find({"user_id":user_id})
    searchservice = []
    for ee in response:
        ee['_id']=str("_id")
        searchservice.append(ee)
    return {"services":searchservice}

@user_router.get(
    "/services",
)
async def services():
    
    response = db["services"].find()
    searchservice = []
    for ee in response:
        ee['_id']=str("_id")
        ee['user_info'] = get_user_by_id(ee["user_id"])
        searchservice.append(ee)
    return {"services":searchservice}


@user_router.get(
    "/searchprestataire/{first_name}",
)
async def searchprestataire(first_name:str,token: dict = Depends(token_required)):

    
    response = db["users"].find_one({"first_name":first_name})
   
    response['_id']=str(response['_id'])
    response['img_url']=""


    responses = db["services"].find({"user_id":response['_id']})
    searchservice = []
    for aa in responses:
        aa['_id']=str(aa['_id'])
        searchservice.append(aa)

    print(response)

    return {"services":searchservice, "user_info": response}





@user_router.post(
    "/auth/forgot-password",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
        **send_email_response,
    },
)
async def reset_password(user: User_email):
    """
    Reset password for a user by email address.

    Args:
        user (User_email): User_email object containing the email address of the user.

    Returns:
        dict: Dictionary containing a success message indicating that an email has been sent for password reset.

    Raises:
        HTTPException: If the user does not exist or if there is an error sending the email.

    """
    # Get user by email
    user = get_user_by_email(user.email)
    if not user:
        raise HTTPException(status_code=404, detail="user does not exist!")

    receiver = user["email"]
    first_name = user["first_name"]
    id_user = str(user["_id"])
    # Send password reset email
    sended = send_restepassword_email(receiver, first_name, id_user)
    if not sended:
        raise HTTPException(status_code=421, detail="fail to send the email")

    return {"message": "please check your email !"}  # Return success message


@user_router.put(
    "/users/set_password/{user_id}",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
        **invitation_reponse,
    },
)
async def set_password(user_password: User_password, user_id):
    """
    Update the password of a user in the database based on their user_id.

    Args:
        user_id (str): The user_id of the user whose password needs to be updated.
        password (str): The new password to be set.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
    """
    pattern = (
        r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\\[\]{};':\"\\\\|,.<>\\/?]).{8,}$"
    )
    # Hash the password

    hashed_password = ph.hash(user_password.password)
    user = get_user_by_id(user_id)
    if user.get("invitation_status") == "Expired":
        raise HTTPException(status_code=424, detail="Invitation Expired !")
    if user.get("password") == None:
        # Accept the invitation if password is not set
        accept_invitation(user_id)

    # Update the password in the database
    if re.match(pattern, user_password.password):
        update_password(user_id, hashed_password)
        return {"message": "password updated successfully !"}
    else:
        raise HTTPException(
            status_code=411,
            detail="Password format is invalid. It must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
        )


@user_router.get(
    "/users/verify_email/{user_id}",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
    },
)
async def verify_email(user_id):
    """
    Verify the email address associated with a user account.

    Args:
        user_id (str): User ID of the account to be verified.

    Returns:
        dict: Dictionary containing a success message indicating that the email has been verified.

    """
    user = get_user_by_id(user_id)
    accept_invitation(user_id)
    return {"message": "Account verified successfully "}


@user_router.get(
    "/auth/me",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
    },
)
async def me_api(token: dict = Depends(token_required)):
    """
    Get the user associated with the provided authentication token.

    Args:
        token (dict): Authentication token containing user information.

    Returns:
        dict: Dictionary containing the user information.

    """
    user = get_user_by_id(token["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return {"user": user}



# @user_router.get(
#     "/users_by_type/{type}",
#     responses={
#         **bad_request,
#         **validation_error,
#         **successful_response,
#         **user_response,
#     },
# )
# async def users_by_type(type):
#     """
#     Get the user associated with the provided authentication token.

#     Args:
#         token (dict): Authentication token containing user information.

#     Returns:
#         dict: Dictionary containing the user information.

#     """
#     user = get_users_by_type(type)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found!")
#     return {"user": user}

@user_router.post(
    "/users",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **email_response,
        **send_email_response,
        **business_email_response,
        **business_domain_response,
    },
)
async def invite_user(user: User, token: dict = Depends(token_required)):
    """
    API endpoint for inviting a new user.

    Args:
        user (User): User object containing the details of the user to be invited.
        token (dict): Token required for authentication.

    Returns:
        dict: Dictionary containing a success message.

    """
    now = datetime.now()  # Get the current timestamp
    user.created_on = now  # Set the created_on field of the user object
    user.verified_email = False
    user.invitation_status = "Pending"
    new_user = get_user_by_id(token["id"])
    admin_name = new_user["first_name"]  # Get the first name of the admin user
    invite_new_user(user, admin_name)
    return {"message": "User invited successfully!"}


@user_router.get(
    "/users",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
        **email_response,
        **send_email_response,
    },
)
async def get_list_users(token: dict = Depends(token_required)):
    """
    API endpoint for getting a list of all users.

    Args:
        token (dict): Token required for authentication.

    Returns:
        dict: Dictionary containing a list of all users.

    """
    # check if email expired
    is_email_expired()
    all_users = get_all_users()
    return {"users": all_users}


@user_router.delete(
    "/users/{user_id}",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **user_response,
    },
)
async def delete_user(user_id: str, token: dict = Depends(token_required)):
    """
    Delete a user from the database based on their user_id.

    Args:
        user_id (str): The user_id of the user to be deleted.

    Returns:
        pymongo.results.DeleteResult: The result of the delete operation.
    """
    result = deleteUser(user_id)
    if result.deleted_count == 1:
        return {"message": "user deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")




@user_router.put(
    "/users/update_user_role/{user_id}",
    responses={**bad_request, **validation_error, **successful_response},
)
async def update_user_role(
    user_id, role: User_role, token: dict = Depends(token_required)
):
    """
    API endpoint for updating the role of a user.

    Args:
        user_id (str): ID of the user to update.
        role (User_role): User_role object containing the new role.
        token (dict): Token required for authentication.

    Returns:
        dict: Dictionary containing a success message.

    """
    edit_role_user(user_id, role.role)
    return {"message": "User role updated successfully"}


@user_router.put(
    "/users/update_password/{user_id}",
    responses={
        **bad_request,
        **validation_error,
        **successful_response,
        **old_password_response,
    },
)
async def updatee_password(
    user_id, password: new_password_user, token: dict = Depends(token_required)
):
    """
    API endpoint for updating the password of a user.

    Args:
        user_id (str): ID of the user to update.
        password (new_password_user): new_password_user object containing old and new password.
        token (dict): Token required for authentication.

    Returns:
        dict: Dictionary containing a success message.

    """
    response = update_new_password(
        user_id, password.old_password, password.new_password
    )
    if response == True:
        return {"message": "Your password changed successfully"}


from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_sso.sso.google import GoogleSSO
from pydantic import BaseModel
import os
from typing import Optional

# Environment variables for your Google OAuth credentials
# You would need to register your app in Google Cloud Console and get these
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "29892117963-hrcit8lmdr856quhb7pkp1q4mhkh7iod.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "8jc-jIC-ZMfvXD-CGcng5gfE")
# This should be your application's base URL + the callback route
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://127.0.0.1:5001/auth/google/callback")


# Initialize the Google SSO helper
google_sso = GoogleSSO(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    allow_insecure_http=True,  # Set to False in production
)

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserInfo(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    picture: Optional[str] = None
    provider: str

@user_router.get("/")
async def root():
    return {"message": "Welcome to FastAPI Google OAuth demo"}

# Modify the login_google and auth_google_callback functions

@user_router.get("/auth/google/login")
async def login_google():
    """Initiates the Google OAuth authentication flow"""
    async with google_sso:
        # Redirects the user to the Google login page
        return await google_sso.get_login_redirect()

@user_router.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    """Handles the Google OAuth callback after user authentication"""
    try:
        async with google_sso:
            # Get the user info from Google
            user = await google_sso.verify_and_process(request)

            user = get_user_by_email(user.email)
            if user :
                token = create_access_token({"id": str(user["_id"])})
                return {"user": user["email"], "token": token}
            else:

                now = datetime.now()
                user_infor = {
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "email":user.email,
                    "password":"",
                    "created_on":now,
                    "img_url":user.picture,
                    "provider":"google",
                    "verified_email":True,
                    "invitation_status":"Accepted",
                    "role":"client"




                }
                response = signup(user_infor)
                token = create_access_token({"id": str(response["user_id"])})
                # Rest of your code...
                return {"message": "user added succesfully !" , "token": token}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not validate Google credentials: {str(e)}"
        )
# Example protected route using a simple bearer token
# In a real application, you would implement proper JWT validation
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="auth/google/login",
    tokenUrl="auth/google/callback"
)

@user_router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    """
    A protected route that requires authentication
    In a real app, you would validate the token properly
    """
    return {"message": "You have access to this protected route", "token": token}



