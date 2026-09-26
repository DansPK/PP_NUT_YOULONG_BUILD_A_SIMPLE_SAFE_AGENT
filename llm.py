import os
from litellm import completion, api_base
from dotenv import load_dotenv


load_dotenv()

def ask_llm(messages, tools=None):
    return completion(
        model=f"openai/{os.environ['LLM_MODEL']}",
        api_base=os.environ['LLM_BASE_URL'],
        api_key=os.environ['LLM_API_KEY'],
        messages=messages,
        tools=tools,
    )