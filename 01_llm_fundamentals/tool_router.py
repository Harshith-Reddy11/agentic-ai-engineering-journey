from llm_client import LLMClient
from tool_definitions import TOOL_DEFINITIONS
from schemas import ToolCall, ToolCallBatch
from tool_executor import execute_tool

llm = LLMClient()


def build_tool_prompt(user_input: str):

    return f"""
You are an AI assistant that can use tools.

Available tools:

{TOOL_DEFINITIONS}

For the user's request, decide whether a tool is needed.

If one or more tools are needed, return ONLY JSON in this format:

{{
    "tool_calls": [
        {{
            "tool_name": "tool name",
            "arguments": {{
                "argument": "value"
            }}
        }}
    ]
}}

If no tool is needed, return:

{{
    "tool_calls": []
}}

User request:
{user_input}
"""

def build_final_answer_prompt(
    user_input,
    tool_batch,
    tool_results
):

    return f"""
You are an AI assistant.

The user asked:
{user_input}

The tools that were used:
{tool_batch}

The tool results were:
{tool_results}

Using these tool results, answer the user's original question.

Give only the final answer.
Do not mention internal tools, tool calls, or implementation details.
"""

def clean_json_response(response: str):

    response = response.strip()

    if response.startswith("```json"):
        response = response[len("```json"):]

    if response.startswith("```"):
        response = response[len("```"):]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()

def run_agent(user_input: str):

    # Step 1: Ask LLM which tools are needed
    prompt = build_tool_prompt(user_input)

    response = llm.generate(prompt)

    # Step 2: Clean LLM JSON
    cleaned_response = clean_json_response(response)

    # Step 3: Validate multiple tool calls
    tool_batch = ToolCallBatch.model_validate_json(
        cleaned_response
    )

    # Step 4: Execute every tool call
    tool_results = []

    for tool_call in tool_batch.tool_calls:

        result = execute_tool(tool_call)

        tool_results.append({
            "tool_call": tool_call.model_dump(),
            "result": result
        })

    # Step 5: Send all tool results back to LLM
    final_prompt = build_final_answer_prompt(
        user_input,
        tool_batch,
        tool_results
    )

    # Step 6: Generate final answer
    final_answer = llm.generate(final_prompt)

    return final_answer

if __name__ == "__main__":

    user_input = "What is 25 multiplied by 8, and what is an LLM?"

    answer = run_agent(user_input)

    print("\nFinal answer:", answer)