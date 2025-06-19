from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()
#-----------------------------------------------------------
billing_agent = Agent(
    model="gpt-4.1-nano",
    name="billing_agent",
    instructions="You are expert in billing and finance.",
    handoff_description="You are expert in billing and finance. You can handle queries related to billing.",
)

#-----------------------------------------------------------

refund_agent = Agent(
    model="gpt-4.1-nano",
    name="refund_agent",
    instructions="You are expert in refund and returns.",
    handoff_description="You are expert in refund and returns. You can handle queries related to refunds.",
)

#-----------------------------------------------------------
triage_agent = Agent(
    model="gpt-4.1-nano",
    name="triage_agent",
    instructions="You route user queries to appropriate agents.", 
    handoffs=[billing_agent, refund_agent],
)

#-----------------------------------------------------------

result=Runner.run_sync(triage_agent, "I want to refund and check my billing ?")

print(result.final_output)
print(result._last_agent.name)

