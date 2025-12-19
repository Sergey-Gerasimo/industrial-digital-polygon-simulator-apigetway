python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class GameRole(str, Enum):
    PLAYER = "player"
    SPECTATOR = "spectator"
    ADMIN = "admin"


class Player(BaseModel):
    user_id: str
    game_role: GameRole


class RoomBase(BaseModel):
    room_name: str


class RoomCreate(RoomBase):
    pass


class RoomInDB(RoomBase):
    room_id: str
    created_at: datetime
    is_closed: bool = False
    is_ready: bool = False
    creator_id: str
    players: List[Player] = []

    class Config:
        from_attributes = True


class Room(RoomInDB):
    pass


class GetAllRoomsRequest(BaseModel):
    is_closed: Optional[bool] = None
    is_ready: Optional[bool] = None
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)


class GetAllRoomsResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    rooms: List[Room]
    total_count: int


class CreateRoomRequest(BaseModel):
    room_name: str


class GetMyRoomsResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    rooms: List[Room]
    total_count: int


class InviteToRoomRequest(BaseModel):
    user_name: str
    player_role: GameRole = GameRole.PLAYER


class JoinToRoomRequest(BaseModel):
    ct: str 