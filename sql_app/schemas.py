from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessLog(BaseModel):
    student_id: int
    entered_at: datetime
    exited_at: datetime

    class Config():
        orm_mode = True


class InRoomUserBase(BaseModel):
    id: int


class InRoomUser(InRoomUserBase):
    entered_at: Optional[datetime] = None
    """(models.py) entered_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP()'))"""

    class Config():
        orm_mode = True
