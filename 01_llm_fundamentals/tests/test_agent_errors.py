import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)
from schemas import ToolCall
from tool_executor import execute_tool


def test_unknown_tool():
    call = ToolCall(
        tool_name="delete_everything",
        arguments={}
    )

    result = execute_tool(call)

    assert result["success"] is False
    assert "Unknown tool" in result["error"]
    print("PASS: Unknown tool rejected.")


def test_invalid_arguments():
    call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": "hello",
            "b": 10,
            "operation": "add"
        }
    )

    result = execute_tool(call)

    assert result["success"] is False
    print("PASS: Invalid arguments rejected.")


def test_tool_error():
    call = ToolCall(
        tool_name="calculator",
        arguments={
            "a": 10,
            "b": 0,
            "operation": "divide"
        }
    )

    result = execute_tool(call)

    assert result["success"] is False
    assert "divide by zero" in result["error"].lower()
    print("PASS: Tool error handled safely.")


if __name__ == "__main__":
    test_unknown_tool()
    test_invalid_arguments()
    test_tool_error()
