import os
from dotenv import load_dotenv
from agents import Agent, Runner, FileSearchTool, WebSearchTool, function_tool

load_dotenv()
#-----------------------------------------------------------
@function_tool
def weather_karachi():
    print("The weather in Karachi is sunny with a high of 30°C.")

#-----------------------------------------------------------

@function_tool
def prime_minister_of_karachi():
    print("The prime minister of pakistan is Imran Khan.")
#-----------------------------------------------------------

agent = Agent(
    model="gpt-4.1-mini",
    name="my_agent",
    instructions="You are a helpful assistant",
    tools=[weather_karachi, prime_minister_of_karachi])
#-----------------------------------------------------------

runner = Runner.run_sync(agent, "Who is the prime minister of pakistan?")
print(runner.final_output)

