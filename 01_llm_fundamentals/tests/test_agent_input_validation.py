
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import pytest
from agent import Agent


class FakeLLM:
    def __init__(self):
        self.calls = 0

    def generate(self, prompt):
        self.calls += 1
        raise AssertionError("LLM should not be called")


def fake_executor(tool_call):
    raise AssertionError("Tool executor should not be called")


@pytest.mark.parametrize(
    "goal, error_type",
    [
        ("", ValueError),
        ("   ", ValueError),
        (123, TypeError),
        ("x" * 2001, ValueError),
    ],
)
def test_invalid_goal_stops_before_llm(goal, error_type):
    llm = FakeLLM()
    agent = Agent(
        llm_client=llm,
        tool_executor=fake_executor,
    )

    with pytest.raises(error_type):
        agent.run(goal)

    assert llm.calls == 0
