
import json
import logging

from llm_client import LLMClient
from agent_state import AgentState
from schemas import AgentDecision, ToolCall
from prompts import AGENT_SYSTEM_PROMPT
from tool_executor import execute_tool
from pydantic import BaseModel


logger = logging.getLogger(__name__)


def validate_goal(goal: str) -> str:
    if not isinstance(goal, str):
        raise TypeError("Goal must be a string")

    goal = goal.strip()

    if not goal:
        raise ValueError("Goal cannot be empty")

    if len(goal) > 2000:
        raise ValueError("Goal is too long")

    return goal



class Agent:
    def __init__(self, llm_client, tool_executor, max_steps=5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps

    def decide(self, state: AgentState) -> AgentDecision:
        prompt = f"""
{AGENT_SYSTEM_PROMPT}

USER GOAL:
{state.goal}

PREVIOUS OBSERVATIONS:
{json.dumps(state.observations, indent=2)}

Decide the next action based on the goal and observations.
Return one JSON object matching the required AgentDecision schema.
"""

        response = self.llm_client.generate(prompt)

        # Handle responses wrapped in Markdown code fences.
        response = response.strip()
        if response.startswith("```"):
            lines = response.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            response = "\n".join(lines).strip()

        return AgentDecision.model_validate_json(response)

    def run(self, goal: str) -> AgentState:
        goal = validate_goal(goal)
        state = AgentState(
            goal=goal,
            max_steps=self.max_steps,
        )

        logger.info("Agent started: %s", goal)
        previous_tool_call = None

        while state.status == "running":
            if state.step >= state.max_steps:
                state.status = "max_steps"
                logger.warning("Agent reached maximum steps")
                break

            logger.info("[STEP %d] Goal: %s", state.step + 1, goal)

            try:
                decision = self.decide(state)
            except Exception as error:
                logger.error("Decision failed: %s", error)
                state.observations.append(
                    f"Decision error: {error}"
                )
                state.status = "error"
                break

            logger.info("[DECISION] %s", decision.model_dump())

            if decision.action == "final":
                if not decision.final_answer:
                    state.status = "error"
                    state.observations.append(
                        "Final decision did not contain an answer."
                    )
                    break

                state.final_answer = decision.final_answer
                state.status = "completed"
                logger.info("[RESULT] %s", state.final_answer)
                break

            if decision.action == "tool_call":
                if not decision.tool_name:
                    state.status = "error"
                    state.observations.append(
                        "Tool call did not specify a tool name."
                    )
                    break
                tool_signature = (
                    decision.tool_name,
                    json.dumps(decision.arguments, sort_keys=True)
                )
                if tool_signature == previous_tool_call:
                    state.status = "repeated_action"
                    state.observations.append(
                        f"Stopped because the same tool call was repeated: "
                        f"{decision.tool_name}"
                    )
                    logger.warning("Repeated tool call detected. Stopping agent.")
                    break
                previous_tool_call = tool_signature
                
                tool_call = ToolCall(
                    tool_name=decision.tool_name,
                    arguments=decision.arguments,
                )

                result = self.tool_executor(tool_call)

                observation = {
                    "tool": decision.tool_name,
                    "arguments": decision.arguments,
                    "result": result,
                }

                state.observations.append(
                    json.dumps(observation, default=str)
                )

                logger.info("[OBSERVATION] %s", result)

                state.step += 1

        logger.info(
            "Agent stopped with status: %s",
            state.status,
        )

        return state


if __name__ == "__main__":
    agent = Agent(
        llm_client=LLMClient(),
        tool_executor=execute_tool,
        max_steps=5,
    )
    
    result = agent.run("Calculate 25 multiplied by 18, then add 100.")

    print("\nFinal state:")
    print(result.model_dump())
