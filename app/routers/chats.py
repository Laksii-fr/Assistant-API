from fastapi import APIRouter,UploadFile,Depends,Form,File
import app.controllers.chats as controller
import app.models.model_types as model_type
from app.controllers.cognito import get_current_user
from typing import *
router = APIRouter()


@router.post("/create-chat")
async def create_chat(
    astId: str = Form(...),
    threadId: str = Form(...),
    message: str = Form(...),
    user: dict = Depends(get_current_user),
    image: List[UploadFile] = File(None),
):
    userId = user.get('login_id')
    # Create an instance of AssistantChat
    chat_instance = model_type.AssistantChat(
        userId=userId,
        astId=astId,
        threadId=threadId,
        message=message
    )
    content = await controller.process_chat_content([chat_instance], image)
    created_response = await controller.create_new_chat([chat_instance], content)
    response = {
        "status": True,
        "message": "Chat created successfully",
        "data": created_response
    }

    return response
