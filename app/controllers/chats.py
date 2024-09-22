import app.models.model_types as model_type
import app.helpers.global_helper as global_helper
import app.utils.open_ai_utils as ai_utils
import asyncio
from fastapi import APIRouter,Depends,File, UploadFile,Form
from typing import *

async def create_new_chat(chats: list[model_type.AssistantChat],content
):
        users_chat_list = chats
        
        list_of_response = [global_helper.create_chat(element,content) for element in users_chat_list]
        all_results = await asyncio.gather(*list_of_response)

        return all_results

async def process_chat_content(chat: list[model_type.AssistantChat],image : List[UploadFile] = File(None)):
    content = []
    for chat_item in chat:
        if image:
            for img in image:
                file_id = await ai_utils.upload_image_to_openai(img,chat_item.astId)
                content.append({
                    "type": "image_file",
                    "image_file": {
                        "file_id": file_id
                        }
                    }
                )

        content.append({
            "type": "text",
            "text": chat_item.message
        })
    return content