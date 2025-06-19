import os
import asyncio
import chainlit as cl
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    AsyncOpenAI,
)
from openai.types.responses import ResponseTextDeltaEvent

# ————— Setup —————
load_dotenv()
set_tracing_disabled(True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

agent = Agent(
    model=OpenAIChatCompletionsModel(
        model="deepseek/deepseek-r1:free",
        openai_client=client,
    ),
    name="Agent",
    instructions="You are a helpful assistant.",
)

# ————— Chainlit Lifecycle —————

@cl.on_chat_start
def start_chat():
    # initialize message history in the user session
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": agent.instructions}],
    )

@cl.on_message
async def handle_user_message(message: cl.Message):
    # 1. Append user message to history
    history = cl.user_session.get("message_history")
    history.append({"role": "user", "content": message.content})

    # 2. Create an empty Chainlit Message to stream into
    reply = cl.Message(author=agent.name, content="")

    # 3. Launch the agent in streaming mode
    stream = Runner.run_streamed(
        starting_agent=agent,
        input=message.content,
    )

    # 4. Stream tokens into the Chainlit UI
    async for event in stream.stream_events():
        if (
            event.type == "raw_response_event"
            and isinstance(event.data, ResponseTextDeltaEvent)
        ):
            await reply.stream_token(event.data.delta)

    # 5. Update history and finalize the message
    history.append({"role": "assistant", "content": reply.content})
    await reply.update()
