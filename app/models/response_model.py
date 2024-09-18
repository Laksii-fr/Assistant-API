from pydantic import BaseModel


class ApiResponse(BaseModel):
        status: bool = False
        message: str = ""
        data: dict | list = None
