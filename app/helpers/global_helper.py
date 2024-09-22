import app.utils.open_ai_utils as ai_utils
import app.models.model_types as modelType
import datetime
import asyncio


def print_current_time():
        now = datetime.datetime.now()
        print(now)


async def create_chat(chat:modelType.AssistantChat,content):
        response = await ai_utils.create_assistant_chat(chat,content)
        print(f"Processing....")
        await asyncio.sleep(1)
        print(f"Processing completed ==> {chat}")
        return response