import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)
from agent import Agent
from agent_state import AgentState



class FakeLLM:
    """Returns different tool calls to test the step limit."""

    def __init__(self):
        self.calls = 0

    def generate(self, prompt):
        self.calls += 1

        # Each call is different, so repetition detection
        # won't stop the agent before the step limit.
        if self.calls == 1:
            a, b = 2, 3
        else:
            a, b = 3, 4

        return f"""
        {{
            "action": "tool_call",
            "tool_name": "calculator",
            "arguments": {{
                "a": {a},
                "b": {b},
                "operation": "add"
            }},
            "final_answer": null
        }}
        """


def fake_executor(tool_call):
    return {
        "success": True,
        "result": 5
    }


agent = Agent(
    llm_client=FakeLLM(),
    tool_executor=fake_executor,
    max_steps=2,
)

state = agent.run("Keep calculating.")

print("\nTest result:")
print(state.model_dump())

assert state.status == "max_steps"
assert state.step == 2

print("\nPASS: Maximum-step protection works.")
