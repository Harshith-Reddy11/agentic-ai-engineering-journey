from llm_client import LLMClient
from tool_definitions import TOOL_DEFINITIONS
from schemas import ToolCall
from tool_executor import execute_tool

llm = LLMClient()


def build_tool_prompt(user_input: str):

    return f"""
You are an AI assistant that can use tools.

Available tools:

{TOOL_DEFINITIONS}

For the user's request, decide whether a tool is needed.

If a tool is needed, return ONLY JSON in this format:

{{
    "tool_name": "tool name",
    "arguments": {{
        "argument": "value"
    }}
}}

If no tool is needed, return:

{{
    "tool_name": null,
    "arguments": {{}}
}}

User request:
{user_input}
"""

def build_final_answer_prompt(user_input, tool_call, tool_result):
    return f"""
You are an AI assistant.

The user asked:
{user_input}

You decided to use this tool:
{tool_call}

The tool returned:
{tool_result}

Using the tool result, answer the user's original question.

Give only the final answer to the user.
Do not mention internal tools, tool calls, or implementation details.
"""

def run_agent(user_input: str):

    # Step 1: Ask LLM to decide whether a tool is needed
    prompt = build_tool_prompt(user_input)

    response = llm.generate(prompt)

    # Step 2: Validate the LLM's tool call
    tool_call = ToolCall.model_validate_json(response)

    # Step 3: Execute the selected tool
    tool_result = execute_tool(tool_call)

    # Step 4: Send tool result back to LLM
    final_prompt = build_final_answer_prompt(
        user_input,
        tool_call,
        tool_result
    )

    final_answer = llm.generate(final_prompt)

    return final_answer

if __name__ == "__main__":

    user_input = "What is 25 multiplied by 8?"

    answer = run_agent(user_input)

    print("\nFinal answer:", answer)