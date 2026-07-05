import base64
import binascii
from typing import Dict

from pydantic import BaseModel, field_validator


class ImageData(BaseModel):
    image: str  # Base64 encoded image (data URL)
    dict_of_vars: Dict[str, str]  # Variables previously assigned by the user

    @field_validator("image")
    @classmethod
    def validate_base64(cls, v: str) -> str:
        try:
            base64.b64decode(v.split(",")[1])
        except (binascii.Error, IndexError):
            raise ValueError("Invalid base64 encoded image")
        return v
