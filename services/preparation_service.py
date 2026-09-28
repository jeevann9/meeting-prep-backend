from services.hindsight_service import recall_client_memory
from agent.meeting_agent import generate_meeting_brief


def prepare_meeting(
    client: str,
    query: str
):

    memory_response = recall_client_memory(
        client_name=client,
        query=query
    )

    memories = memory_response["memories"]

    ai_brief = generate_meeting_brief(
        client_name=client,
        meeting_notes=query,
        memories=memories
    )

    return {
        "client": client,
        "brief": ai_brief
    }