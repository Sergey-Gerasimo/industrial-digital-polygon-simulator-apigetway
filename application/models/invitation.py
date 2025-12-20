from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from .room import GameRole


class InvitationBase(BaseModel):
    room_id: str
    receiver_id: str
    player_role: GameRole = GameRole.PLAYER


class InvitationCreate(InvitationBase):
    pass


class InvitationInDB(InvitationBase):
    invite_id: str
    inviter_id: str
    is_accepted: bool = False
    created_at: datetime
    updated_at: datetime
    ct: str  # invitation token

    class Config:
        from_attributes = True


class Invitation(InvitationInDB):
    pass


class GetMyInvitesRequest(BaseModel):
    inviter_id: Optional[str] = None
    player_role: Optional[str] = None
    is_accepted: Optional[bool] = None


class GetMyInvitesResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    invitations: List[Invitation]
    total_count: int
