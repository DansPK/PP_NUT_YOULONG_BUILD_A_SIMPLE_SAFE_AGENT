import json

from harness import run_tool
from llm import ask_llm
from schemas import TOOLS

response = ask_llm(
    [{"role": "user", "content": "Use search_books to find The Hobbit."}],
    tools=TOOLS,
)

message = response.choices[0].message

if not message.tool_calls:
    print("No tool call:", message.content)
else:
    for call in message.tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments)

        print("Model requested:", name, args)
        print("Tool returned:", run_tool(name, args, role="visitor"))