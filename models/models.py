from pydantic import BaseModel
from typing import List

class FormData(BaseModel):
    username: str
    password: str
    comment: str
    file_path: str
    checkbox_values: List[str]
    radio_value: str
    multi_select_values: List[str]
    dropdown_value: str

class InputSchema(BaseModel):
    url: str
    form_data: FormData
