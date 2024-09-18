import asyncio

from fastapi import UploadFile
from openai import OpenAI
import time
import datetime


def wait_on_run(run, thread_id):
        client = OpenAI()
        while run.status == "queued" or run.status == "in_progress":
                run = client.beta.threads.runs.retrieve(
                        thread_id=thread_id,
                        run_id=run.id,
                )
                time.sleep(0.5)
        return run


def submit_message(assistant_id, thread_id, user_message):
        client = OpenAI()
        client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=user_message,

        )
        return client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
        )


def create_run(assistant_id: str, thread_id: str, user_input: str):
        run = submit_message(assistant_id, thread_id, user_input)
        return run


async def get_response(thread_id: str):
        client = OpenAI()
        return client.beta.threads.messages.list(thread_id=thread_id, order="asc")


def pretty_print(messages):
        print("# Messages")
        for m in messages:
                print(f"{m.role}: {m.content[0].text.value}")
        print()


def prettify_all_response(response):
        assistant_response = []
        for m in response:
                response = {
                        "id": m.id,
                        "role": m.role,
                        "message": m.content[0].text.value,
                        "thread_id": m.thread_id,
                        "created_at": m.created_at
                }
                assistant_response.append(response)

        return assistant_response


def prettify_single_response(response):
        all_messages = []

        for m in response:
                all_messages.append(m)

        last_response = all_messages[len(all_messages) - 1]

        assistant_response = [
                {
                        "id": last_response.id,
                        "role": last_response.role,
                        "message": last_response.content[0].text.value,
                        "thread_id": last_response.thread_id,
                        "created_at": last_response.created_at
                }
        ]

        return assistant_response


async def create_file(file: UploadFile):

        client = OpenAI()
        contents = await file.read()
        created_file = client.files.create(file=contents, purpose="assistants")

        file_object = {
                "fileId": created_file.id,
                "fileName": file.filename,
                "fileSize": file.size,
                "fileType": file.content_type,
        }
        return file_object


async def create_files(files: [UploadFile]):
        async_files = [create_file(file) for file in files]
        files = await asyncio.gather(*async_files)
        return files
