
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import pytest
from pydantic import ValidationError
from schemas import AgentDecision


def test_valid_tool_call():
    decision = AgentDecision(
        action="tool_call",
        tool_name="calculator",
        arguments={"a": 5, "b": 5, "operation": "add"}
    )
    assert decision.action == "tool_call"


def test_valid_final_answer():
    decision = AgentDecision(
        action="final",
        final_answer="The answer is 10."
    )
    assert decision.action == "final"


def test_tool_call_requires_tool_name():
    with pytest.raises(ValidationError):
        AgentDecision(action="tool_call")


def test_tool_call_cannot_include_final_answer():
    with pytest.raises(ValidationError):
        AgentDecision(
            action="tool_call",
            tool_name="calculator",
            final_answer="10"
        )


def test_final_requires_non_empty_answer():
    with pytest.raises(ValidationError):
        AgentDecision(
            action="final",
            final_answer="   "
        )


def test_final_cannot_specify_tool():
    with pytest.raises(ValidationError):
        AgentDecision(
            action="final",
            tool_name="calculator",
            final_answer="10"
        )


def test_invalid_action_rejected():
    with pytest.raises(ValidationError):
        AgentDecision(action="delete_everything")
