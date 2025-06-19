
import os
import chainlit as cl
from dotenv import load_dotenv
from agents import Agent,Runner, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI

# ————— Setup —————
load_dotenv()
set_tracing_disabled(True)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ————— History —————
hisory = []
models = {
    "DeepSeek": "deepseek/deepseek-r1:free",
    "Gemini_2.0_Flash": "google/gemini-2.0-flash-exp:free",
    "Mistral": "mistralai/devstral-small:free",
    "Qwen": "qwen/qwen3-14b:free",
    "Meta_Llama": "meta-llama/Llama-4-maverick:free"
}

# ——————— Handle User Input —————

@cl.on_chat_start
async def handle_user_message():
    await cl.Message(content="Hello, Welcome to Nazia Multi-LLM Chainlit?").send()
    
    settings = await cl.ChatSettings(
        [
            cl.input_widget.Select(
                id= "Model",
                label="Choose Any LLM model",
                values = list(models.keys()),
                initial_index = 0,
            )            
        ]
    ).send()
    handle_settings_update(settings)
    
# —————— Handle Settings Update —————   
@cl.on_settings_update
async def handle_settings_update(settings):
    model_name = settings["Model"]
    cl.user_session.set("model", models[model_name])
    
    await cl.Message(content=f"You have selected {model_name} Ai model.").send()



@cl.on_message
async def handle_user_input(msg: cl.Message):  
    user_input = msg.content 
    hisory.append({"role": "user", "content": user_input})
    
    
    selected_model = cl.user_session.get("model")

    # ————— OpenAI Client —————
    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    # ————— Initialize Agent —————
    agent = Agent(
        name="My Agent",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(model=selected_model, openai_client=client),
    )


    # ——————— Run Agent —————
    result = Runner.run_sync(agent, hisory)
    await cl.Message(content=result.final_output).send()
  
