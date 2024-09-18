from fastapi import APIRouter
import app.controllers.chats as controller
import app.models.model_types as model_type
import app.models.response_model as response_model

router = APIRouter()


@router.post("/create-chat")
async def create_chat(chat: list[model_type.AssistantChat]):
        created_response = await controller.create_new_chat(chat)

        response = response_model.ApiResponse()
        response.message = "Chat created successfully"
        response.status = True
        response.data = created_response

        return response


# @router.get("/get-chat")
# async def get_all_chat():
#         chat_files = await controller.get_all_assistants()
#         return {"message": "Blogs fetched successfully", "data": chat_files}
#
#
# @router.put("/update-chat")
# async def update_chat():
#         chat_files = await controller.get_all_assistants()
#         return {"message": "Blogs fetched successfully", "data": chat_files}
#
#
# @router.delete("/remove-chat")
# async def remove_chat():
#         chat_files = await controller.get_all_assistants()
#         return {"message": "Blogs fetched successfully", "data": chat_files}
