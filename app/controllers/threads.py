import uuid
from app.utils.mongo_utils import save_created_thread
from app.utils.mongo_utils import fetch_threads_by_assistant_id
from app.utils.open_ai_utils import create_thread
from app.utils.open_ai_utils import create_thread_title
from app.utils.open_ai_utils import get_all_thread_history
import app.models.model_types as model_type


async def create_new_thread(userId,thread: model_type.AssistantThread):
        created_thread = await create_thread()
        thread_title = await create_thread_title(thread.threadTitle)
        thread.threadTitle = thread_title
        save_created_thread(userId,thread, created_thread.id)
        return {"thread": created_thread}


async def get_all_threads(userId,assistant_id: str):
        result = fetch_threads_by_assistant_id(userId,assistant_id)
        return result


async def get_thread_history_by_id(thread_id: str):
        result = await get_all_thread_history(thread_id)
        return result
