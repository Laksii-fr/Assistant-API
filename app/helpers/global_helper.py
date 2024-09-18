from app.utils.open_ai_utils import create_assistant_chat
import app.models.model_types as modelType
import datetime
import asyncio


def print_current_time():
        now = datetime.datetime.now()
        print(now)


async def create_chat(chat:modelType.AssistantChat):
        response = await create_assistant_chat(chat)
        print(f"Processing....")
        await asyncio.sleep(1)
        print(f"Processing completed ==> {chat}")
        return response