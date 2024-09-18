from typing_extensions import Any
from app.schemas import CreateAssistantBaseSchema
from app.schemas import CreateAssistantThreadBaseSchema
from app.database import OurAssistant
from app.database import AssistantThreads
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
