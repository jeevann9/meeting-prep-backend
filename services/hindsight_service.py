import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()


HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_API_URL = os.getenv("HINDSIGHT_API_URL")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID")


client = Hindsight(
    base_url=HINDSIGHT_API_URL,
    api_key=HINDSIGHT_API_KEY
)

def retain_meeting(
    client_name: str,
    meeting_date: str,
    participants: list[str],
    notes: str
):
    content = f"""
Client: {client_name}
Meeting Date: {meeting_date}
Participants: {", ".join(participants)}
Meeting Notes:
{notes}
"""

    try:
        result = client.retain(
            bank_id=HINDSIGHT_BANK_ID,
            content=content,
            context="client meeting",
            timestamp=meeting_date
        )

        return result

    except Exception as e:
        raise Exception(f"Failed to save meeting to Hindsight: {str(e)}")

def recall_client_memory(client_name: str, query: str):
    full_query = f"{client_name}: {query}"

    try:
        result = client.recall(
            bank_id=HINDSIGHT_BANK_ID,
            query=full_query
        )

        memories = [item.text for item in result.results]

        cleaned_memories = clean_memories(memories)

        return {
            "client": client_name,
            "query": query,
            "memories": cleaned_memories
        }

    except Exception as e:
        raise Exception(f"Failed to recall memories from Hindsight: {str(e)}")


def clean_memories(memories: list[str]):
    cleaned = []

    for memory in memories:
        text = memory.split(" | When:")[0].strip()

        if text not in cleaned:
            cleaned.append(text)

    return cleaned

def test_hindsight():
    return client.recall(
        bank_id=HINDSIGHT_BANK_ID,
        query="security"
    )