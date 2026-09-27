from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.meeting import (
    Meeting,
    StoredMeeting,
    RecallRequest,
    PrepareRequest,
    MeetingResponse,
    RecallResponse,
    PrepareResponse
)

from services.meeting_service import (
    save_meeting,
    get_all_meetings,
    recall_meetings
)

from services.preparation_service import prepare_meeting


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/meetings", response_model=MeetingResponse)
def create_meeting(meeting: Meeting):
    return save_meeting(meeting)


@app.get("/meetings", response_model=list[StoredMeeting])
def get_meetings():
    return get_all_meetings()


@app.post("/meetings/recall", response_model=RecallResponse)
def recall_meeting(request: RecallRequest):
    try:
        return recall_meetings(
            request.client,
            request.query
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/meetings/prepare", response_model=PrepareResponse)
def prepare_meeting_endpoint(request: PrepareRequest):
    try:
        return prepare_meeting(
            client=request.client,
            query=request.query
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )