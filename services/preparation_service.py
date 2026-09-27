from services.hindsight_service import recall_client_memory


def prepare_meeting(client: str, query: str):

    memory_response = recall_client_memory(
        client_name=client,
        query=query
    )

    memories = memory_response["memories"]

    return {
        "client": client,
        "brief": {
            "key_topics": memories[:5],
            "previous_discussions": memories,
            "talking_points": [
                "Review the client's main concerns.",
                "Address the requirements discussed in previous meetings.",
                "Clarify any unresolved questions."
            ],
            "questions_to_ask": [
                "Are there any new requirements?",
                "Has the client made any decisions since the previous meeting?",
                "Are there any remaining concerns we should address?"
            ]
        }
    }