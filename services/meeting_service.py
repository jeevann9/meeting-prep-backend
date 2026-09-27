from models.meeting import Meeting, StoredMeeting
from services.hindsight_service import (
    retain_meeting,
    recall_client_memory
)

meetings = []
next_id = 1


def save_meeting(meeting: Meeting):
    global next_id

    stored_meeting = StoredMeeting(
        id=next_id,
        client=meeting.client,
        meeting_date=meeting.meeting_date,
        participants=meeting.participants,
        notes=meeting.notes
    )

    meetings.append(stored_meeting)
    next_id += 1

    retain_meeting(
        client_name=meeting.client,
        meeting_date=meeting.meeting_date,
        participants=meeting.participants,
        notes=meeting.notes
    )

    return {
        "message": "Meeting saved successfully",
        "meeting": stored_meeting
    }


def get_all_meetings():
    return meetings

def recall_meetings(client: str, query: str):
    return recall_client_memory(client, query)