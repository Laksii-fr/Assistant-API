import app.models.model_types as model_type
import app.helpers.global_helper as global_helper
import asyncio


async def create_new_chat(chats: list[model_type.AssistantChat]):
        users_chat_list = chats
        list_of_response = [global_helper.create_chat(element) for element in users_chat_list]
        all_results = await asyncio.gather(*list_of_response)

        return all_results

