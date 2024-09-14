from dataclasses import dataclass, field
from uuid import uuid4
from typing import Optional

class User:
    id: str = uuid4().hex
    name: str
    email: str
    phone_number: str
