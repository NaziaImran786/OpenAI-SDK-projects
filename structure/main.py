from dotenv import load_dotenv
from agents import Agent, Runner
from pydantic import BaseModel
import rich 

load_dotenv()
#-----------------------------------------------------------
class user_info(BaseModel):
    isfamous: bool        
    title: str
    author: str
    genre: str
    publication_year: int
    summary: str

#------------------------------------------------
agent =Agent(
    model= "gpt-4.1-nano",
    name="my_agent",
    instructions="You are a book helpful assistant",
    output_type=user_info,
)

#-----------------------------------------------------------

result = Runner.run_sync(agent, "Tell me about the book 'The Great Gatsby' and its main themes?")
rich.print(result.final_output)



