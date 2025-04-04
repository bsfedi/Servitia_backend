from datetime import datetime, timedelta
from bson import Binary, ObjectId
from fastapi import HTTPException
from utilities import send_email, send_request_email
from database import db
import argon2
import base64
import re
import requests
import bson.binary
import pymongo

ph = argon2.PasswordHasher()



def get_user_by_role(role):
    all_users = []
    users = db["users"].find({"role": role})

    for user in users:
        # Check if invitation_status is present and expired
        if "invitation_status" in user and user["invitation_status"] == "Expired" or user["invitation_status"] == "Pending":
            continue  # Skip users with expired invitation_status
        user["_id"] = str(user["_id"])
        # bindata = base64.b64encode(user["img_url"]).decode("utf-8")
        user["img_url"] = ""
        user["item_first_name"] = user["first_name"] 
        user["item_last_name"] = user["last_name"] 
        all_users.append(user)

    return all_users




def signup(user):
    # Create a new dictionary to store the user data
    new_user = dict(user)
    # Check if the email belongs to an admin and send a request email to the admin
    if new_user["provider"] == None :
        if db["users"].count_documents({}) == 0:
            with open("C:/Users/fedi/Desktop/Easink/user/avatar.png", "rb") as f:
                img_data = f.read()
            new_user["img_url"] = bson.binary.Binary(img_data)
            # The collection is empty, so we can add the new user without further checks
            response = db["users"].insert_one(new_user)
            if response:
                return {
                    "message": "User added successfully !",
                    "user_id": response.inserted_id,
                }
        else:
            if db["users"].find_one({"email": new_user["email"]}):
                raise HTTPException(status_code=409, detail="Email address already in use")

            response = db["users"].insert_one(new_user)

            if response:
                return {
                    "message": "User added successfully !",
                    "user_id": response.inserted_id,
                }
    else:
        response = db["users"].insert_one(new_user)
        if response:
            return {
                    "message": "User added successfully !",
                    "user_id": response.inserted_id,
                }


def update_user_access(usecase_id, user_id):
    try:
        # Get the current user_access list from the usecase document
        new_usecases = db["usecases"].find_one({"_id": ObjectId(usecase_id)})[
            "user_access"
        ]

        # Append the user_id to the user_access list
        new_usecases.append(str(user_id))

        # Update the usecase document with the new user_access list
        response = db["usecases"].update_one(
            {"_id": ObjectId(usecase_id)}, {"$set": {"user_access": new_usecases}}
        )
        # Return the response from the database update operation
        return response
    except Exception as ex:
        # Return an error message if an exception occurs
        return {"message": f"{str(ex)}"}


def invite_new_user(user, admin_name):
    new_user = dict(user)



    # Check if email address is already in use
    if db["users"].find_one({"email": new_user["email"]}):
        raise HTTPException(status_code=409, detail="Email address already in use")


    with open("C:/Users/fedi/Desktop/Easink/user/avatar.png", "rb") as f:
        img_data = f.read()
    new_user["img_url"] = bson.binary.Binary(img_data)
    response = db["users"].insert_one(new_user)

    # Insert new user into the database
    

    # Check if user was successfully inserted into the database
    if response:
        # Send invitation email to the new user
        sended = send_email(
            new_user["email"], new_user["first_name"], admin_name, response.inserted_id
        )

        # Raise an exception if email sending failed
        if not sended:
            raise HTTPException(status_code=421, detail="Failed to send the email")

        # Return success message with user_id
        return {
            "message": "User invited successfully !",
            "user_id": response.inserted_id,
        }


def get_user_by_email(email):
    # Query the database to find a user by email
    user = db["users"].find_one(dict(email=email))
    # Return the user object if found, or None if not found
    return user


def verify_account(user_id):
    # Update the account verification status for the user with the given user_id
    # to mark it as verified
    response = db["users"].update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"verified_email": True}}
    )

    # Return the response object from the update operation
    return response


def get_user_by_id(uid):
    # Retrieve a user from the database based on the given user ID (uid)
    user = db["users"].find_one(dict(_id=ObjectId(uid)))

    # If no user is found with the given user ID, raise an HTTPException with a 404 status code
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert ObjectId fields to string in the user dictionary
    user = {i: str(user[i]) if isinstance(user[i], ObjectId) else user[i] for i in user}
    if user["img_url"] is not None:
        # If the user's img_url field is not None, encode it as base64
        # before returning it in the user dictionary
        bindata = base64.b64encode(user["img_url"]).decode("utf-8")
        user["img_url"] = bindata

    # Return the user dictionary
    return user


def accept_invitation(user_id):
    # Update the invitation status and verified email field of a user to "Accepted" in the database
    response = db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"invitation_status": "Accepted", "verified_email": True}},
    )
    return response


def get_users_by_type(type):
    users = []
    all_users= list(db["users"].find({"type_project": {"$in": [type]}}))
    for user in all_users:
        if user["img_url"] is not None:
            # If the user's img_url field is not None, encode it as base64
            # before returning it in the user dictionary
            bindata = base64.b64encode(user["img_url"]).decode("utf-8")
            user["img_url"] = ""
        user['_id']=str(user['_id'])
        users.append(user)
    
    return users


def expired_invitation(user_id):
    # Update the invitation status of a user to "Expired" in the database
    response = db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "invitation_status": "Expired",
            }
        },
    )
    return response


def  get_all_users():
    user_list = []
    try:
        for user in db["users"].find():
            # Convert ObjectId to string
            user["_id"] = str(user["_id"])
            # Convert the bytes to a base64-encoded string using base64.b64encode
            if user["img_url"] is not None:
                # bindata = base64.b64encode(user["img_url"]).decode("utf-8")
                user["img_url"] = ""
            user_list.append(user)  # Append user object to user_list

        return user_list  # Return the list of users
    except Exception as ex:
        return {
            "message": f"{str(ex)}"
        }  # Return an error message with exception details if an exception occurs


def deleteUser(user_id):
    result = db["users"].delete_one(dict(_id=ObjectId(user_id)))
    return result


def update_password(user_id, password):
    response = db["users"].update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"password": password}}
    )
    return response


def updat_user(user_id, user):
    # Update the first_anem and last_name and img_url field of  user in the database
    response = db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "specialite": user["specialite"],
                "descriptif": user["descriptif"],
                "prix": user["prix"],
                "img_url": user["img_url"],
            }
        },
    )
    return response


def edit_role_user(user_id, role):
    role_to_project = {
        "admin": ["Administration", "Lab", "AML", "Fraud", "Risk", "CDP", "Module Attribution"],
        "devops": ["Administration", "Lab"],
        "Data science": ["Lab"],
        "AML auditor": ["AML"],
        "AML Manager": ["AML"],
        "Fraud Controller": ["Fraud"],
        "Fraud manager": ["Fraud"],
        "Risk Analyst": ["Risk"],
        "Risk Manager": ["Risk"],
        "CDP Marketer": ["CDP"],
        "CDP Manager": ["CDP"],
        "MMM Marketer": ["Module Attribution"],
        "MMM Manager": ["Module Attribution"],
        "MMM Agency consultant": ["Module Attribution"]
    }

    type_project = []

    for new_role, projects in role_to_project.items():
        if new_role in role:
            type_project.extend(projects)

    response = db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {
            "$set": {
                "role": role,
                "type_project":list(set(type_project))
            }
        },
    )
    return response


def update_usecase(user_id, usecase_id):
    try:
        # Get the user's existing use cases and add the new use case
        user = get_user_by_id(user_id)
        new_usecases = user["use_case"] + [usecase_id]

        # Remove duplicates from the list of new use cases
        new_usecases = list(dict.fromkeys(new_usecases))

        # Update the user's use cases in the database
        response = db["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"use_case": new_usecases}}
        )
        return response
    except Exception as ex:
        return {"message": f"{str(ex)}"}


def delete_usecase(user_id, usecase_id):
    usecases = get_user_by_id(user_id)["use_case"]
    try:
        # Remove the use case from the user's existing use cases
        usecases.remove(usecase_id)

        # Update the user's use cases in the database
        response = db["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"use_case": usecases}}
        )

        # Return the response from the database update
        return response
    except Exception as ex:
        return {"message": f"{str(ex)}"}


def is_email_expired():
    # Set the expiration time to 24 hours
    expiration_time = timedelta(hours=24)
    # Get the current time
    current_time = datetime.now()

    users = get_all_users()
    for user in users:
        # Check if user's invitation status is "Pending"
        if user["invitation_status"] == "Pending":
            # Calculate time difference
            time_difference = current_time - user["created_on"]
            # Check if invitation has expired
            if time_difference > expiration_time:
                expired_invitation(user["_id"])
    return {"message": "All invitation status changes"}


def update_new_password(user_id, old_password, new_password):
    user = get_user_by_id(user_id)
    try:
        # Verify old password
        verify_password(user["password"], old_password)
        # Hash the new password
        hashed_password = ph.hash(new_password)
        # Update the password in the database
        update_password(user_id, hashed_password)
        return True
    except:
        # Raise an HTTPException with appropriate error message if old password is incorrect
        raise HTTPException(status_code=426, detail="Your old password is incorrect")


def verify_password(hashed_password, password):
    try:
        # Verify if the provided password matches the hashed password
        if argon2.PasswordHasher().verify(hashed_password, password):
            # Return a message indicating that the password is correct
            return {"message": "Password is correct!"}
        else:
            # Raise an HTTPException with appropriate error message if password is invalid
            raise HTTPException(status_code=411, detail="Invalid password")
    except argon2.exceptions.VerifyMismatchError:
        # Raise an HTTPException with appropriate error message if password is incorrect
        raise HTTPException(status_code=412, detail="Incorrect password!")
