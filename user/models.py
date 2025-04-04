from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
import base64

from enum import Enum


class User(BaseModel):
    # id:str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: Optional[str]
    img_url: Optional[str] = None
    provider:Optional[str] = None
    specialite:Optional[str] = None
    descriptif:Optional[str] = None
    prix:Optional[str] = None
    role: Optional[str] = None
    invitation_status: Optional[str] = "Pending"


class Edit_user(BaseModel):
    first_name: str
    last_name: str
    specialite:Optional[str] = None
    descriptif:Optional[str] = None
    prix:Optional[str] = None
    password: str
    img_url: Optional[str] = None


class Service(BaseModel):
    nom :str 
    description : str
    user_id : str
    prix : str
    lieux :str

class User_password(BaseModel):
    password: str


class new_password_user(BaseModel):
    old_password: str
    new_password: str


class User_email(BaseModel):
    email: EmailStr


class User_role(BaseModel):
    role: Optional[list] = []


class User_login(BaseModel):
    email: EmailStr
    password: str


class Domaine(BaseModel):
    # id:str
    name: str


