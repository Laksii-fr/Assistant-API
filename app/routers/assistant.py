from fastapi import APIRouter, UploadFile, Depends, File
import app.controllers.assistant as controller
import app.models.model_types as model_type
import app.models.response_model as response_model

router = APIRouter()


@router.post("/create-assistant")
async def create_assistant(assistant: model_type.Assistant):
    response = await controller.create_new_assistant(assistant)
    return {"message": f"Assistant created successfully", "Assistant": f"{response}"}


@router.post("/create-assistant-with-file")
async def create_assistant_with_file(
    files: list[UploadFile],
    assistant: model_type.Assistant = Depends(),
) -> response_model.ApiResponse:
    new_assistant = await controller.create_new_assistant_with_file(assistant, files)
    response = response_model.ApiResponse()
    response.message = "Assistant created successfully"
    response.status = True
    response.data = new_assistant
    return response


@router.post("/upload-assistant-files/{ast_id}")
async def upload_assistant_files(
    ast_id: str,
    files: list[UploadFile],
) -> response_model.ApiResponse:
    uploaded_files = await controller.upload_assistant_files(ast_id, files)
    response = response_model.ApiResponse()
    response.message = "Files uploaded successfully"
    response.status = True
    response.data = uploaded_files
    return response


@router.get("/get-assistant")
async def get_all_assistant() -> response_model.ApiResponse:
    chat_files = await controller.get_all_assistants()

    response = response_model.ApiResponse()
    response.message = "Assistant fetched successfully"
    response.status = True
    response.data = chat_files
    return response


@router.get("/get-assistant/{ast_id}")
async def get_all_assistant_by_id(ast_id: str) -> response_model.ApiResponse:
    assistant = await controller.get_assistant_by_id(ast_id)
    response = response_model.ApiResponse()
    response.message = "Assistant fetched successfully"
    response.status = True
    response.data = assistant
    return response


@router.put("/update-assistant")
async def update_assistant_with_file(
    assistant: model_type.UpdateAssistant,
) -> response_model.ApiResponse:
    updated_assistant = await controller.update_assistant(assistant)
    response = response_model.ApiResponse()
    response.message = "Assistant updated successfully"
    response.status = True
    response.data = updated_assistant
    return response


# @router.delete("/remove-assistant")
# async def remove_assistant():
#     chat_files = await controller.get_all_assistants()
#     return {"message": "Blogs fetched successfully", "data": chat_files}
