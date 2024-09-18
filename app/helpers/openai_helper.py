import asyncio

from fastapi import UploadFile
from openai import OpenAI
import time
import datetime
import io

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


import io
from fastapi import UploadFile
from openai import OpenAI

async def create_file(file: UploadFile, vector_storeId):
    print('1.4.1')
    client = OpenAI()
    
    # Read the file contents
    contents = await file.read()
    
    # Create a BytesIO object and set its name attribute to include the filename with extension
    file_like = io.BytesIO(contents)
    file_like.name = file.filename  # Add this to ensure the file has its original name
    
    print('1.4.2')
    created_file = client.files.create(file=file_like, purpose="assistants")
    
    print('1.4.3')
    fileId = created_file.id
    
    # Associate the file with the vector store
    vector_store_file = client.beta.vector_stores.files.create(
        vector_store_id=vector_storeId,
        file_id=fileId
    )
    
    print('1.4.4')
    
    # Create a file object with metadata
    file_object = {
        "fileId": created_file.id,
        "fileName": file.filename,
        "fileSize": file.size,
        "fileType": file.content_type,
    }
    
    print('1.4.5')
    return file_object



async def create_files(files: [UploadFile],vector_storeId):
        print('1.4.1')
        async_files = [create_file(file,vector_storeId) for file in files]
        files = await asyncio.gather(*async_files)
        return files
