import json
from typing import Any
from harness import run_tool, TOOL_PERMISSIONS
from llm import ask_llm
from schemas import TOOLS





def run_agents(request: str, role:str, history=None, confirm_delete=None) -> tuple[str | Any, list[Any]] | tuple[str, list[Any]]:
    history = list(history or [])
    messages = [
        {
            "role": "system",
            "content": (
                # make sure that the llm detect the role and refuse the action without proper permission
                f"The user's role is {role}. "
                "If an action is unavailable to this role, explain that before asking for details. "
            ),
        },
        *history,
        {"role": "user", "content": request},
    ]


    # Pre-define allowed tool to llm
    allowed_tools = [
        tool for tool in TOOLS
        if role in TOOL_PERMISSIONS.get(
            tool["function"]["name"],set()
        )
    ]


    # Limit how many times the agent can decide what to do next
    for _ in range(5):
        response = ask_llm(messages, tools=allowed_tools)
        message = response.choices[0].message
        calls = message.tool_calls or []

        #No tools call and give final answer
        if not calls:
            answer = message.content or "I could not answer that request."

            # Remember this completed exchange for the next CLI question.
            history.extend([
                {"role": "user", "content": request},
                {"role": "assistant", "content": answer},
            ])
            return answer, history

        # Keep the llm action in history
        messages.append(message.model_dump(exclude_none=True))


        for call in calls:
            # The model provides arguments as JSON text.
            try:
                args = json.loads(call.function.arguments)
                result = run_tool(call.function.name, args, role, confirm_delete)
            except json.JSONDecodeError:
                result = {
                    "error": "Invalid tool arguments",
                }

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })
    return "Stopped after 5 rounds.", history
