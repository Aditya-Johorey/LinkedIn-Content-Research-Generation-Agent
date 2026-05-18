from pydantic import BaseModel
from typing import List

class LinkedInPost(BaseModel):
    title: str
    hook: str
    body: str
    hashtags: List[str]