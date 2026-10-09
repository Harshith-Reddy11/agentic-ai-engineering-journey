
from agent import Agent


class RepeatingLLM:
    """Always requests the same calculator action."""

    def generate(self, prompt):
        return """
        {
            "action": "tool_call",
            "tool_name": "calculator",
            "arguments": {
                "a": 2,
                "b": 3,
                "operation": "add"
            },
            "final_answer": null
        }
        """


def fake_executor(tool_call):
    return {"success": True, "result": 5}


agent = Agent(
    llm_client=RepeatingLLM(),
    tool_executor=fake_executor,
    max_steps=5,
)

state = agent.run("Keep adding 2 and 3.")

print("\nTest result:")
print(state.model_dump())

assert state.status == "repeated_action"
assert state.step == 1

print("\nPASS: Repeated-action detection works.")
