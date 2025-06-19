import asyncio
from dotenv import load_dotenv
from agents import Agent,input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, Runner, TResponseInputItem,  RunContextWrapper
from pydantic import BaseModel  

load_dotenv()
# -----------------------------------------------------------       
class Slangs_check_output(BaseModel):
    is_slang: bool
    reasoning: str

#-----------------------------------------------------------

guardrail_agent = Agent(
    model="gpt-4.1-mini",
    name="guardrail_agent",
    instructions="Check if user is using slang in any language.",
    output_type=Slangs_check_output,
)

#-------------------------------------------------------------
@input_guardrail
async def slangs_guardrail(ctx: RunContextWrapper[None], agent: Agent, input: str|list[TResponseInputItem]) -> GuardrailFunctionOutput:
    
    result  = await Runner.run(guardrail_agent, input, context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_slang,
    )
#-----------------------------------------------------------          

async def main():    
    agent = Agent(  
        model="gpt-4.1-mini",
        name="my_agent",    
        instructions="You are a helpful assistant",
        input_guardrails=[slangs_guardrail]
    )
    # -----------------------------------------------------------

    try:
        result =await Runner.run(agent, "kutty")  # Example query
        print(result.final_output)  # Output the final result
    except InputGuardrailTripwireTriggered as e:
        print("user is using bad words :", e)
    # -----------------------------------------------------------
    
if __name__ == "__main__":  
    asyncio.run(main())  # Run the main function