from fastapi import UploadFile
from pydantic import BaseModel
from pydantic import BaseModel, EmailStr, constr
from typing import *

class InitiatePasswordResetRequest(BaseModel):
    email: str


class ConfirmPasswordResetRequest(BaseModel):
    email: str
    confirmation_code: str
    new_password: constr(min_length=8)


class ConfirmUserRequest(BaseModel):
    email: str
    confirmation_code: str


class SignUpRequest(BaseModel):
    email: str
    password: constr(min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str


class Assistant(BaseModel):
    userId: str
    astName: str
    astInstruction: str
    gptModel: str
    astTools: list[str]


class UpdateAssistant(BaseModel):
    userId: str
    astId: str
    astName: str
    astInstruction: str
    gptModel: str
    astTools: list[str]


class AssistantWithFile(BaseModel):
    userId: str
    astName: str
    astInstruction: str
    gptModel: str
    astTools: list[str]
    file: UploadFile


class AssistantThread(BaseModel):
    userId: str
    astId: str
    threadTitle: str


class AssistantChat(BaseModel):
    userId: str
    astId: str
    threadId: str
    message: str


class AssistantFile(BaseModel):
    fileId: str
    fileName: str
    fileSize: str
    fileType: str
