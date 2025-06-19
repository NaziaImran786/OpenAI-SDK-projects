import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, AsyncOpenAI , Runner, set_tracing_disabled
import chainlit as cl

load_dotenv()
set_tracing_disabled(disabled=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

#-----------------------------------------------------------
hisory = []
#------------------------------------------------------------
client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)
agent = Agent(
    model=OpenAIChatCompletionsModel(model="deepseek/deepseek-chat-v3-0324:free", openai_client=client),
    name="my_agent",
    instructions="You are a helpful asistant",    
)

#--------------------------------------------------------------
 
@cl.on_message
async def main(message: cl.Message): 
       
    content = message.content 
    
    hisory.append({"role": "user", "content": content}) 
        
    res = await Runner.run(agent, content)
    
    hisory.append({"role": "assistant", "content": res.final_output})
    
    await cl.Message(content=res.final_output).send()