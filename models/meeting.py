from pydantic import BaseModel


class Meeting(BaseModel):
    client: str
    meeting_date: str
    participants: list[str]
    notes: str


class StoredMeeting(Meeting):
    id: int


class RecallRequest(BaseModel):
    client: str
    query: str


class RecallResponse(BaseModel):
    client: str
    query: str
    memories: list[str]


class PrepareRequest(BaseModel):
    client: str
    query: str


class MeetingResponse(BaseModel):
    message: str
    meeting: StoredMeeting


class Brief(BaseModel):
    key_topics: list[str]
    previous_discussions: list[str]
    talking_points: list[str]
    questions_to_ask: list[str]


class PrepareResponse(BaseModel):
    client: str
    brief: Brief