
import os
from dotenv import load_dotenv
from agents import Agent, Runner,RunContextWrapper
from dataclasses import dataclass

load_dotenv()
# -----------------------
@dataclass
class dynamic_function_information():
    name: str 
    description: str
    
# -----------------------

dynamic_information = dynamic_function_information("Nazia", "I want to become an AI expert" )
    
# -----------------------
def dynamic_function(ctx: RunContextWrapper[dynamic_function_information], agent: Agent ) -> str:
    return f"dynamic function executed instructions: {ctx.context.name} and {ctx.context.description}"

# -----------------------

agent = Agent(
    name = "my agent",
    model = "gpt-4.1-nano",
    instructions = dynamic_function,    
)

jawab = Runner.run_sync(agent, "what is the name and description of the user?", context=dynamic_information)

print(jawab.final_output)
# rich.print(jawab)




