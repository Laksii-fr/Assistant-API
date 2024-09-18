from typing_extensions import Any
from app.schemas import CreateAssistantBaseSchema
from app.schemas import CreateAssistantThreadBaseSchema
from app.database import OurAssistant
from app.database import AssistantThreads,UserProfiles,UsersCollection
from datetime import datetime
from fastapi import HTTPException, status
import app.models.model_types as modelType


def save_created_assistant(assistant: modelType.Assistant, assistant_id: str):
    new_assistant: CreateAssistantBaseSchema = {
        "userId": assistant.userId,
        "astId": assistant_id,
        "astName": assistant.astName,
        "astInstruction": assistant.astInstruction,
        "gptModel": assistant.gptModel,
        "astFiles": [],
        "astTools": assistant.astTools,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    try:
        OurAssistant.insert_one(new_assistant)
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during saving assistant in database.",
        )

def save_user_info(email: str, sub_id: str = None, is_confirmed: bool = False):
    try:
        # Define the update operation
        update_operation = {
            "email": email,
            "is_confirmed": is_confirmed
        }

        # Only update sub_id if it is provided
        if sub_id:
            update_operation["sub_id"] = sub_id

        # Use upsert=True to create the document if it doesn't exist
        UsersCollection.update_one(
            {"email": email},
            {"$set": update_operation},
            upsert=True
        )

    except Exception as e:
        print(f"Error saving user info: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while saving user info: {str(e)}")

def get_assistant_by_id(assistant_id: str):
    try:
        cur = OurAssistant.find(
            filter={"astId": assistant_id}, projection={"_id": 0}
        ).sort([("createdAt", -1)])
        result = []
        for doc in cur:
            result.append(doc)
        return result
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during fetching assistant.",
        )


def update_created_assistant(assistant: modelType.UpdateAssistant):
    new_assistant: CreateAssistantBaseSchema = {
        "userId": assistant.userId,
        "astId": assistant.astId,
        "astName": assistant.astName,
        "astInstruction": assistant.astInstruction,
        "gptModel": assistant.gptModel,
        "astTools": assistant.astTools,
        "updatedAt": datetime.utcnow(),
    }
    try:
        OurAssistant.update_one({"astId": assistant.astId}, {"$set": new_assistant})
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during saving assistant in database.",
        )


def save_created_assistant_with_file(assistant: modelType.Assistant, assistant_info):
    new_assistant: CreateAssistantBaseSchema = {
        "userId": assistant.userId,
        "astId": assistant_info["assistant"].id,
        "astName": assistant.astName,
        "astInstruction": assistant.astInstruction,
        "gptModel": assistant.gptModel,
        "astTools": assistant.astTools,
        "astFiles": assistant_info["files"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    try:
        OurAssistant.insert_one(new_assistant)
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during saving assistant in database.",
        )


def update_assistant_files(ast_id: str, assistant_files):
    try:
        files = assistant_files["files"]
        OurAssistant.update_one(
            {"astId": ast_id}, {"$push": {"astFiles": {"$each": files}}}
        )
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during saving assistant in database.",
        )


def save_created_thread(payload: modelType.AssistantThread, threadId: str):
    new_assistant: CreateAssistantThreadBaseSchema = {
        "userId": payload.userId,
        "astId": payload.astId,
        "threadId": threadId,
        "threadTitle": payload.threadTitle,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    try:
        AssistantThreads.insert_one(new_assistant)
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during saving assistant thread in database.",
        )


def fetch_all_assistants():
    try:
        cur = OurAssistant.find(filter={}, projection={"_id": 0}).sort(
            [("createdAt", -1)]
        )
        result = []
        for doc in cur:
            result.append(doc)
        return result
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during fetching assistant.",
        )


def fetch_threads_by_assistant_id(assistant_id: str):
    try:
        cur = AssistantThreads.find(
            filter={"astId": assistant_id}, projection={"_id": 0}
        ).sort([("createdAt", -1)])
        result = []
        for doc in cur:
            result.append(doc)
        print(f"Find assistants", result)
        return result
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during fetching assistant.",
        )

def find_user_by_email(email: str):
    """Find a user by email."""
    return UsersCollection.find_one({"email": email})

def insert_new_user(email: str, sub_id: str, is_confirmed: bool = False):
    """Insert a new user into the database."""
    user_data = {
        "email": email,
        "sub_id": sub_id,
        "is_confirmed": is_confirmed
    }
    return UsersCollection.insert_one(user_data)

def update_user_confirmation_status(email: str, is_confirmed: bool):
    """Update the confirmation status of a user."""
    return UsersCollection.update_one(
        {"email": email},
        {"$set": {"is_confirmed": is_confirmed}}
    )

def save_user_profile(userId,payload: modelType.UserProfile):
    new_profile = {
        "userID": userId,
        "UserName": payload.User_name,
        "UserMail": payload.User_email,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    } # type: ignore
    try:
        UserProfiles.insert_one(new_profile)
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Something went wrong during saving assistant thread in database.",
        )
