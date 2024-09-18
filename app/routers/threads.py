from fastapi import APIRouter
import app.controllers.threads as controller
import app.models.model_types as model_type
import app.models.response_model as response_model

router = APIRouter()


@router.post("/create-thread")
async def create_thread(thread: model_type.AssistantThread):
        created_thread = await controller.create_new_thread(thread)

        response = response_model.ApiResponse()
        response.message = "Thread created successfully"
        response.status = True
        response.data = created_thread

        return response


@router.get("/get-thread/{assistant_id}")
async def get_all_thread(assistant_id: str):
        thread_history = await controller.get_all_threads(assistant_id)

        response = response_model.ApiResponse()
        response.message = "Thread fetched successfully"
        response.status = True
        response.data = thread_history

        return response


@router.get("/get-thread-history/{thread_id}")
async def get_thread_history_by_id(thread_id: str):
        thread_history = await controller.get_thread_history_by_id(thread_id)
        response = response_model.ApiResponse()
        response.message = "Thread history fetched successfully"
        response.status = True
        response.data = thread_history

        return response

