import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, output_guardrail, RunContextWrapper, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered
from pydantic import BaseModel
import asyncio
load_dotenv()

# -----------------------------------------------------------
class MessageOutput(BaseModel):    
    Respone: str
    
class prime_minister_check(BaseModel):
    is_prime_minister: bool
from dotenv import load_dotenv
from agents import Agent, Runner, output_guardrail, RunContextWrapper, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered
from pydantic import BaseModel

load_dotenv()

# -----------------------------------------------------------
class MessageOutput(BaseModel):    
    Respone: str
    
class prime_minister_check(BaseModel):
    is_prime_minister: bool
    Reason: str
    
# ---------------------------------------------------------
guardrail_agent = Agent(
    model="gpt-4.1-mini",
    name="guardrail_agent",
    instructions="Check if the user is a prime minister based on the reasoning provided.",  # Instructions should be a string, not a BaseModel
    output_type=prime_minister_check,  # Assuming the output type is a custom type
) 

# ------------------------------------------------------------
@output_guardrail
async def prime_minister_guardrail(ctx: RunContextWrapper, agent: Agent, output: str) -> GuardrailFunctionOutput:
    # Handle the output as a string, not as a MessageOutput
    result = await Runner.run(guardrail_agent, output, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_prime_minister,  # Trigger if the output indicates a prime minister
    )

# -----------------------------------------------------------
agent = Agent(
    model="gpt-4.1-mini",
    name="my_agent",
    instructions="Provide reasoning and check if the user is a prime minister.",  # Instructions as a string
    output_guardrails=[prime_minister_guardrail],  
)

# -----------------------------------------------------------

async def main():
    try:
        result = await Runner.run(agent, "Hello")
        print(result.final_output.Respone)  # Output the final result
    except OutputGuardrailTripwireTriggered as e:
        print("Tripwire triggered:", e)

if __name__ == "__main__": 
    asyncio.run(main())

    Reason: str
    
# ---------------------------------------------------------
guardrail_agent = Agent(
    model="gpt-4.1-mini",
    name="guardrail_agent",
    instructions="Check if the user is a prime minister based on the reasoning provided.",  # Instructions should be a string, not a BaseModel
    output_type=prime_minister_check,  # Assuming the output type is a custom type
) 

# ------------------------------------------------------------
@output_guardrail
async def prime_minister_guardrail(ctx: RunContextWrapper, agent: Agent, output: MessageOutput) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.Respone, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_prime_minister,  # Trigger if the output indicates a prime minister
    )

# -----------------------------------------------------------
agent = Agent(
    model="gpt-4.1-mini",
    name="my_agent",
    instructions="Provide reasoning and check if the user is a prime minister.",  # Instructions as a string
    output_guardrails=[prime_minister_guardrail],  
)

# -----------------------------------------------------------

async def main():
    try:
        result = await Runner.run(agent, "Hello")
        print(result.final_output.Respone)  # Output the final result
    except OutputGuardrailTripwireTriggered as e:
        print("Tripwire triggered:", e)

if __name__ == "__main__": 
    asyncio.run(main())
