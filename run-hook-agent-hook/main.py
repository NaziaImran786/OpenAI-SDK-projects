
import os
from dotenv import load_dotenv
from agents import Agent, Runner,RunContextWrapper, RunHooks, AgentHooks
from dataclasses import dataclass
import rich

load_dotenv()
# -----------------------
@dataclass
class dynamic_function_information():
    name: str 
    description: str
    
# -----------------------

dynamic_information = dynamic_function_information("Nazia", "I want to become an AI expert" )
    
# -----------------------
class CustomRunHook(RunHooks):
    async def on_agent_start(
        self, ctx: RunContextWrapper[dynamic_function_information], agent: Agent
    ) -> None:
        rich.print(f"Agent '{agent.name}' is starting with context: {ctx.context}")
        
    async def on_agent_end(
        self, ctx: RunContextWrapper[dynamic_function_information], agent: Agent
    ) -> None:
        rich.print(f"Agent '{agent.name}' is starting with context: {ctx.context}")
        
# -----------------------
start_hook = CustomRunHook()
# -----------------------
class CustomAgentHook(AgentHooks):
    async def on_start(self, agent: Agent) -> None:
        rich.print(f"Agent '{agent.name}' is starting with model: {agent.model}")
        
    async def on_end(self, agent: Agent) -> None:
        rich.print(f"Agent '{agent.name}' has finished execution.")

# -----------------------
end_hook = CustomAgentHook()
# -----------------------
agent = Agent(
    name = "my agent",
    model = "gpt-4.1-nano",
    instructions ="you are a helpful assistant",
    hooks = [end_hook]
)
    
#----------------------------------------------------------------

jawab = Runner.run_sync(agent, "what is the name and age and address of the user?", context=dynamic_information, hooks=[start_hook])

print(jawab.final_output)
rich.print(jawab)














