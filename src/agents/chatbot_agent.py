from pydantic import BaseModel

from agents import Agent


class ChatbotResponse(BaseModel):
    response: str
    """The response to the user's question."""

INSTRUCTIONS = (
    "You are a chatbot companion that will try to converse with the user. You will need to respond to the user's message based on the conversation history. Try to make the conversation feel like a natural conversation with a human."
)

chatbot_agent = Agent(
    name="ChatbotAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4.1",
)