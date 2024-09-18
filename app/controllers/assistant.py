from fastapi import UploadFile
import app.utils.mongo_utils as mongo_utils
import app.utils.open_ai_utils as ai_utils
import app.models.model_types as model_type


async def create_new_assistant(assistant: model_type.Assistant):
    created_assistant = await ai_utils.create_assistant(assistant)
    mongo_utils.save_created_assistant(assistant, created_assistant.id)
    return {"assistant": created_assistant}


async def create_new_assistant_with_file(
    payload: model_type.Assistant, files: list[UploadFile]
):
    created_assistant = await ai_utils.create_assistant_with_file(payload, files)
    mongo_utils.save_created_assistant_with_file(payload, created_assistant)
    return {"assistant": created_assistant}


async def upload_assistant_files(ast_id: str, files: list[UploadFile]):
    uploaded_files = await ai_utils.upload_assistant_files(ast_id, files)
    mongo_utils.update_assistant_files(ast_id, uploaded_files)
    return {"files": []}


async def get_all_assistants():
    result = mongo_utils.fetch_all_assistants()
    return result


async def get_assistant_by_id(ast_id: str):
    db_assistant = mongo_utils.get_assistant_by_id(ast_id)
    return db_assistant


async def update_assistant(payload: model_type.UpdateAssistant):
    updated_assistant = await ai_utils.update_assistant(payload)
    mongo_utils.update_created_assistant(payload)
    return {"assistant": updated_assistant}
