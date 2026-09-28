import os
import json

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SYSTEM_PROMPT = """
You are MemoryMeet AI, a meeting preparation assistant.

Your job is to prepare a useful meeting brief using ONLY:
1. Current meeting information.
2. Previous information recalled from Hindsight.

Never invent facts.

If information is unavailable, return an empty list.

For important_stakeholders:
- Include all named participants provided in the current meeting information.
- Preserve their names exactly.
- Include their roles only when explicitly provided.
- Do not invent roles or other personal details.

Return ONLY valid JSON.

The JSON must contain exactly these fields:

{
    "client_overview": [],
    "previous_interests": [],
    "key_concerns": [],
    "important_stakeholders": [],
    "competitors": [],
    "talking_points": [],
    "questions_to_ask": [],
    "suggested_next_steps": []
}

Every field must contain a list of strings.
"""


def generate_meeting_brief(
    client_name: str,
    meeting_notes: str,
    memories: list[str]
):

    recalled_memory = "\n".join(
        f"- {memory}"
        for memory in memories
    )

    if not recalled_memory:
        recalled_memory = "No previous information found."

    user_prompt = f"""
Prepare a meeting brief for:

CLIENT:
{client_name}

CURRENT MEETING INFORMATION:
{meeting_notes}

RECALLED INFORMATION FROM HINDSIGHT:
{recalled_memory}

Use ONLY the information provided above.

Return ONLY JSON.
Do not include markdown.
Do not include ```json.
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    return json.loads(content)